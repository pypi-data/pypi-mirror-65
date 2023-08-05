"""
Converts a JSON schema to an OpenAPI specification 3.0.
"""

from copy import deepcopy
import json

from . import exceptions


def _validate_type(type_):
    """
    Validates the "type" property.
    The type can be a string or an array of strings.
    """

    def validate_type(type_):
        valid_types = [
            "null",
            "boolean",
            "object",
            "array",
            "number",
            "string",
            "integer",
        ]
        if type_ not in valid_types:
            raise exceptions.InvalidTypeError(
                f"Type '{type_}' is not valid. "
                f"Valid types are {', '.join(valid_types)}."
            )

    if isinstance(type_, list):
        for item in type_:
            validate_type(item)
    else:
        validate_type(type_)


def _strip_illegal_keywords(schema):
    """
    Strips illegal keywords from the schema.
    """
    illegal_keywords = ["$schema", "$id", "id"]
    return {key: value for key, value in schema.items() if key not in illegal_keywords}


def _convert_types(schema):
    """
    Converts the "type" property. Turns `type="null"` into `nullable=True`.
    """
    type_ = schema.get("type")
    if not type_:
        return schema

    _validate_type(type_)

    if isinstance(type_, list):
        if (len(type_) > 2) or (len(type_) >= 2 and "null" not in type_):
            raise exceptions.TooManyTypesError(
                f"Type of '{type_}' is too confusing for OpenAPI to understand. "
                f"Found in {json.dumps(schema)}."
            )
    else:
        type_ = [type_]

    del schema["type"]

    if "null" in type_:
        schema["nullable"] = True
    else:
        schema["nullable"] = False

    not_null_type = [t for t in type_ if t != "null"][0]
    if not_null_type:
        schema["type"] = not_null_type

    return schema


def _rewrite_constants(schema):
    """
    Rewrites a "constant" into an "enum" with only one value.
    """
    constants = schema.get("const")
    if constants:
        schema["enum"] = [constants]
        del schema["const"]
    return schema


def _convert_dependencies(schema):
    """
    Converts the dependencies property by appending a condition to the "allOf"
    property.
    """

    def _convert_dep_property(key, dep_properties):
        return {
            "oneOf": [
                {"not": {"required": [key]}},
                {"required": [key] + dep_properties},
            ]
        }

    dependencies = schema.get("dependencies")
    if not dependencies:
        return schema
    all_of = schema.get("allOf", [])
    all_of.extend(
        [_convert_dep_property(key, value) for key, value in dependencies.items()]
    )
    return {
        "allOf": all_of,
        **{
            key: value
            for key, value in schema.items()
            if key not in ("dependencies", "allOf")
        },
    }


def _rewrite_if_then_else(schema):
    """
    Rewrites the "if", "then" and "else" properties by converting it into a "oneOf"
    property.
    """
    if_ = schema.get("if")
    then_ = schema.get("then")
    else_ = schema.get("else", {})
    if not (if_ and then_):
        return schema
    schema["oneOf"] = [{"allOf": [if_, then_]}, {"allOf": [{"not": if_}, else_]}]
    del schema["if"]
    del schema["then"]
    del schema["else"]
    return schema


def _rewrite_exclusive_min_max(schema):
    """
    Rewrites the "exclusiveMaximum" and "exclusiveMinimum" properties by setting the
    "maximum" and "minimum" values and setting the "exclusiveX" value to `True`.
    """
    exclusive_maximum = schema.get("exclusiveMaximum")
    if isinstance(exclusive_maximum, (int, float)):
        schema["maximum"] = exclusive_maximum
        schema["exclusiveMaximum"] = True
    exclusive_minimum = schema.get("exclusiveMinimum")
    if isinstance(exclusive_minimum, (int, float)):
        schema["minimum"] = exclusive_minimum
        schema["exclusiveMinimum"] = True
    return schema


def _convert_properties(schema):
    """
    Converts the "patternProperty" into the "x-patternProperty".
    Always explicitly sets the "additionalProperties" property.
    Only applies to schemas with `type="object"`.
    """
    if schema.get("type") != "object":
        return schema
    pattern_properties = schema.get("patternProperties")
    if pattern_properties:
        del schema["patternProperties"]
        schema["x-patternProperties"] = pattern_properties
    additonal_properties = schema.get("additionalProperties")
    if additonal_properties is None:
        schema["additionalProperties"] = True
    return schema


def _convert_any_of_null(schema):
    """
    If the "anyOf" property contains `{"type": "null"}`, set `nullable=True` and
    remove that condition from the "anyOf".
    """
    nullable_condition = {"type": "null"}
    any_of = schema.get("anyOf")
    if not any_of:
        return schema
    if any(condition == nullable_condition for condition in any_of):
        schema["nullable"] = True
        schema["anyOf"] = [
            condition for condition in any_of if condition != nullable_condition
        ]
    return schema


def _avoid_x_ofs(schema):
    """
    If an "anyOf", "oneOf" or "allOf" property only contains one condition, set that
    condition on the root of the schema and remove the "XOf" property.
    """

    x_of_keys = ["anyOf", "oneOf", "allOf"]

    def __avoid_x_ofs(schema, x_of_key):
        x_of = schema.get(x_of_key)
        if x_of and len(x_of) == 1:
            for key, value in x_of[0].items():
                schema[key] = value
            del schema[x_of_key]
        return schema

    for x_of_key in x_of_keys:
        schema = __avoid_x_ofs(schema, x_of_key)

    return schema


def _convert(schema):
    """
    Converts a (sub) schema.
    """
    schema = _strip_illegal_keywords(schema)
    schema = _convert_types(schema)
    schema = _rewrite_constants(schema)
    schema = _convert_dependencies(schema)
    schema = _rewrite_if_then_else(schema)
    schema = _rewrite_exclusive_min_max(schema)
    schema = _convert_properties(schema)
    schema = _convert_any_of_null(schema)
    schema = _avoid_x_ofs(schema)

    return schema


def convert(schema):
    """
    Converts a JSON schema to an OpenAPI specification 3.0.

    Args:
        schema (dict): The JSON schema.

    Returns:
        dict: The OpenAPIv3 specification.
    """

    if isinstance(schema, list):
        return [convert(item) for item in schema]

    if isinstance(schema, dict):
        schema = _convert(deepcopy(schema))

        properties = schema.get("properties")
        if properties:
            schema["properties"] = {
                key: convert(value) for key, value in properties.items()
            }

        definitions = schema.get("definitions")
        if definitions:
            schema["definitions"] = {
                key: convert(value) for key, value in definitions.items()
            }

    return schema
