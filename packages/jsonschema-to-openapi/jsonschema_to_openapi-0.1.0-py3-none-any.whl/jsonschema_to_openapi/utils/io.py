"""
This module contains functions for reading and writing.
"""

import json


def read_json(filepath):
    """
    Reads a jsonfile from a filepath.

    Args:
        filepath (str): The filepath.

    Returns:
        dict: The json.
    """
    with open(filepath, encoding="utf-8") as file_pointer:
        return json.load(file_pointer)


def write_json(obj, filepath):
    """
    Writes an object as .json into a filepath.

    Args:
        obj (dict): The object.
        filepath (str): The filepath.
    """
    with open(filepath, "w", encoding="utf-8") as file_pointer:
        json.dump(obj, file_pointer, sort_keys=True, indent=4)
