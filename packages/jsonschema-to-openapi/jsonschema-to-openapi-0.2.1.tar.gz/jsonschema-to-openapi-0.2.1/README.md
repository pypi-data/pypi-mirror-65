# jsonschema-to-openapi

Converts a JSON schema to an OpenAPI specification version 3.0.

## Installation

```
pip install jsonschema-to-openapi
```

## Usage

#### CLI

```shell
jsonschema-to-openapi my_json_schema.json my_open_api_spec.json
```

### Package

```python
>>> from jsonschema_to_openapi.convert import convert

>>> schema = {} # Your json schema as dictionary.

>>> convert(schema)
{} # Your OpenAPI specification as dictionary.
```

## Caveats and Limitations

* If you have a [complex schema](https://json-schema.org/understanding-json-schema/structuring.html), where you extend a base schema with the `$ref` operator, you will need to put all base schemas under a "definitions" key in root.
* Abitrarily nested `xOf`s cannot be resolved yet. The program won't fail and will procude valid OpenAPI specification, but the result will still contain nested `xOf` operators. 
    * Input:

        ```json
        {
          "anyOf": [{"$ref": "#/definitions/my_object"}, { "anyOf": [{"type": "null"}] }],
          "definitions": {
              "my_object": {"type": "string"}
          }
        }
        ```
    * Output:

        ```json
        {
            "anyOf": [
                {
                    "$ref": "#/definitions/my_object"
                },
                {
                    "anyOf": [
                        {
                            "type": "null"
                        }
                    ]
                }
            ],
            "definitions": {
                "my_object": {
                    "nullable": false,
                    "type": "string"
                }
            }
        }
        ```

## Changelog

Please take a look at the [CHANGELOG.md](CHANGELOG.md) for notable changes to jsonschema-to-openapi.

## License

See the [LICENSE](LICENSE) for details.

## Development

We welcome new contributions to this project!

### Source Code

You can check the latest source code with the command:

```
git clone git@gitlab.com:InstaffoOpenSource/DataScience/jsonschema-to-openapi.git
```

### Linting

After cloning and installing the dependencies, you can lint the project by executing:

```
make lint
```

### Testing

After cloning and installing the dependencies, you can test the project by executing:

```
make test
```

## Help and Support

### Authors

- Jan-Benedikt Jagusch <jan@instaffo.de>

## Acknowledgements

- This project started as a Python port of [json-schema-to-openapi-schema](https://github.com/wework/json-schema-to-openapi-schema).
