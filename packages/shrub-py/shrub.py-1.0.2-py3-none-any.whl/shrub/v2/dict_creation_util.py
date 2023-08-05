"""Utilities for working with dictionaries."""
from typing import Any, Dict, Optional


def add_if_exists(obj: Dict[str, Any], key_name: str, key_value: Optional[Any]) -> Dict[str, Any]:
    """
    Add the value to the given dictionary if it is not None.

    :param obj: Dictionary to add to.
    :param key_name: Name of key to add.
    :param key_value: Value to add.
    :return: Updated dictionary.
    """
    if key_value:
        obj[key_name] = key_value

    return obj


def add_existing_from_dict(obj: Dict[str, Any], values: Dict[str, Optional[Any]]) -> Dict[str, Any]:
    """
    For each value, add the value to the given dictionary if it is not None.

    :param obj: Dictionary to add to.
    :param values: Dictionary of values to add.
    :return: Updated dictionary.
    """
    for k, v in values.items():
        add_if_exists(obj, k, v)

    return obj
