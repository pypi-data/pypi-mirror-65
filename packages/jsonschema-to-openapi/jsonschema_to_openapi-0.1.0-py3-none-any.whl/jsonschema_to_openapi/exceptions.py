"""
This module contains exceptions for this package.
"""


class JsonschemaToOpenapiException(Exception):
    """
    Base exception for this package.
    """


class SchemaError(JsonschemaToOpenapiException):
    """
    Error when there is something wrong with the schema.
    """


class InvalidTypeError(SchemaError):
    """
    Exception when the type is invalid.
    """


class TooManyTypesError(SchemaError):
    """
    Error when there are too many types.
    """
