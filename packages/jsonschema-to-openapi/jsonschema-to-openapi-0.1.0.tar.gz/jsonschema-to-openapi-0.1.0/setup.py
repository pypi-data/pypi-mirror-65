# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jsonschema_to_openapi', 'jsonschema_to_openapi.utils']

package_data = \
{'': ['*']}

install_requires = \
['jsonschema>=3.2.0,<4.0.0']

entry_points = \
{'console_scripts': ['jsonschema-to-openapi = jsonschema_to_openapi.cli:main']}

setup_kwargs = {
    'name': 'jsonschema-to-openapi',
    'version': '0.1.0',
    'description': 'Converts a JSON schema to an OpenAPI specification version 3.0.',
    'long_description': '# jsonschema-to-openapi\n\nConverts a JSON schema to an OpenAPI specification version 3.0.\n\n## Installation\n\n```\npip install jsonschema-to-openapi\n```\n\n## Usage\n\n#### CLI\n\n```shell\njsonschema-to-openapi my_json_schema.json my_open_api_spec.json\n```\n\n### Package\n\n```python\n>>> from jsonschema_to_openapi.convert import convert\n\n>>> schema = {} # Your json schema as dictionary.\n\n>>> convert(schema)\n{} # Your OpenAPI specification as dictionary.\n```\n\n## Caveats and Limitations\n\n* If you have a [complex schema](https://json-schema.org/understanding-json-schema/structuring.html), where you extend a base schema with the `$ref` operator, you will need to put all base schemas under a "definitions" key in root.\n* Abitrarily nested `xOf`s cannot be resolved yet. The program won\'t fail and will procude valid OpenAPI specification, but the result will still contain nested `xOf` operators. \n    * Input:\n\n        ```json\n        {\n          "anyOf": [{"$ref": "#/definitions/my_object"}, { "anyOf": [{"type": "null"}] }],\n          "definitions": {\n              "my_object": {"type": "string"}\n          }\n        }\n        ```\n    * Output:\n\n        ```json\n        {\n            "anyOf": [\n                {\n                    "$ref": "#/definitions/my_object"\n                },\n                {\n                    "anyOf": [\n                        {\n                            "type": "null"\n                        }\n                    ]\n                }\n            ],\n            "definitions": {\n                "my_object": {\n                    "nullable": false,\n                    "type": "string"\n                }\n            }\n        }\n        ```\n\n## Changelog\n\nPlease take a look at the [CHANGELOG.md](CHANGELOG.md) for notable changes to jsonschema-to-openapi.\n\n## License\n\nSee the [LICENSE](LICENSE) for details.\n\n## Development\n\nWe welcome new contributions to this project!\n\n### Source Code\n\nYou can check the latest source code with the command:\n\n```\ngit clone git@gitlab.com:InstaffoOpenSource/DataScience/jsonschema-to-openapi.git\n```\n\n### Linting\n\nAfter cloning and installing the dependencies, you can lint the project by executing:\n\n```\nmake lint\n```\n\n### Testing\n\nAfter cloning and installing the dependencies, you can test the project by executing:\n\n```\nmake test\n```\n\n## Help and Support\n\n### Authors\n\n- Jan-Benedikt Jagusch <jan@instaffo.de>\n\n## Acknowledgements\n\n- This project started as a Python port of [json-schema-to-openapi-schema](https://github.com/wework/json-schema-to-openapi-schema).\n',
    'author': 'Instaffo GmbH',
    'author_email': 'info@instaffo.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://instaffo.com',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
