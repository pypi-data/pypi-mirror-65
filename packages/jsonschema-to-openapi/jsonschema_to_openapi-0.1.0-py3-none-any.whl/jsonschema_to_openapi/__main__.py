"""
Allow package to be executable through `python -m jsonschema_to_openapi`.
"""
from .cli import main


if __name__ == "__main__":
    main()
