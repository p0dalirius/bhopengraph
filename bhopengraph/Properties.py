#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File name          : Properties.py
# Author             : Remi Gascou (@podalirius_)
# Date created       : 12 Aug 2025

# https://bloodhound.specterops.io/opengraph/developer/nodes
PROPERTIES_SCHEMA = {
    "type": ["object", "null"],
    "description": "A key-value map of node attributes. Values must not be objects. If a value is an array, it must contain only primitive types (e.g., strings, numbers, booleans) and must be homogeneous (all items must be of the same type).",
    "additionalProperties": {
        "type": ["string", "number", "boolean", "array"],
        "items": {"not": {"type": "object"}},
    },
}


def primitive_category(value) -> str:
    """
    Classify a value into one of the OpenGraph primitive categories.

    The BloodHound OpenGraph schema recognizes three primitive categories for
    property values: "string", "number", and "boolean". This helper returns the
    matching category, or an empty string when the value is None or not a
    primitive (e.g. an object, list, or callable).

    Note: ``bool`` is checked before ``int`` because in Python ``bool`` is a
    subclass of ``int``; without this order ``True``/``False`` would be
    misclassified as numbers.

    Source: https://bloodhound.specterops.io/opengraph/developer/nodes

    Args:
      - value: The value to classify

    Returns:
      - str: "string", "number", "boolean", or "" if not a primitive
    """
    if isinstance(value, bool):
        return "boolean"
    if isinstance(value, (int, float)):
        return "number"
    if isinstance(value, str):
        return "string"
    return ""


class Properties(object):
    """
    Properties class for storing arbitrary key-value pairs for nodes and edges.
    Follows BloodHound OpenGraph schema requirements where properties must be primitive types.
    """

    def __init__(self, **kwargs):
        """
        Initialize Properties with optional key-value pairs.

        Args:
          - **kwargs: Key-value pairs to initialize properties
        """
        self._properties = {}
        for key, value in kwargs.items():
            self.set_property(key, value)

    def set_property(self, key: str, value):
        """
        Set a property value. Only primitive types are allowed.

        Args:
          - key (str): Property name
          - value: Property value (must be a primitive type: str, int, float,
            bool, or a homogeneous list of those). None is not a valid value.
        """
        if self.is_valid_property_value(value):
            self._properties[key] = value
        else:
            raise ValueError(
                f"Property value must be a primitive type (str, int, float, bool) "
                f"or a homogeneous list of primitives, got {type(value)}"
            )

    def get_property(self, key: str, default=None):
        """
        Get a property value.

        Args:
          - key (str): Property name
          - default: Default value if key doesn't exist

        Returns:
          - Property value or default
        """
        return self._properties.get(key, default)

    def remove_property(self, key: str):
        """
        Remove a property.

        Args:
          - key (str): Property name to remove
        """
        if key in self._properties:
            del self._properties[key]

    def has_property(self, key: str) -> bool:
        """
        Check if a property exists.

        Args:
          - key (str): Property name to check

        Returns:
          - bool: True if property exists, False otherwise
        """
        return key in self._properties

    def get_all_properties(self) -> dict:
        """
        Get all properties as a dictionary.

        Returns:
          - dict: Copy of all properties
        """
        return self._properties.copy()

    def clear(self):
        """Clear all properties."""
        self._properties.clear()

    def validate(self) -> tuple[bool, list[str]]:
        """
        Validate all properties according to OpenGraph schema rules.

        Returns:
          - tuple[bool, list[str]]: (is_valid, list_of_errors)
        """
        errors = []

        for key, value in self._properties.items():
            if not self.is_valid_property_value(value):
                errors.append(
                    f"Property '{key}' has invalid value type '{type(value)}'; "
                    f"expected a primitive (str, int, float, bool) or a homogeneous list of primitives"
                )

        return len(errors) == 0, errors

    def is_valid_property_value(self, value) -> bool:
        """
        Validate a single property value according to OpenGraph schema rules.

        The BloodHound OpenGraph schema restricts a property value to a single
        primitive (string, number, or boolean) or a homogeneous array of
        primitives. None, nested objects, arrays of objects, and arrays mixing
        primitive categories are not valid.

        Note: ``bool`` and the numeric types are treated as distinct categories,
        so a list such as ``[1, True]`` is rejected as non-homogeneous even
        though ``bool`` is a subclass of ``int`` in Python.

        Source: https://bloodhound.specterops.io/opengraph/developer/nodes

        Args:
          - value: The property value to validate

        Returns:
          - bool: True if valid, False otherwise
        """
        # None is not a valid property value per the OpenGraph schema.
        if value is None:
            return False

        # Lists must be homogeneous sequences of primitives.
        if isinstance(value, list):
            category = ""
            for item in value:
                item_category = primitive_category(item)
                if item_category == "":
                    return False
                if category == "":
                    category = item_category
                elif item_category != category:
                    return False
            # An empty list is valid.
            return True

        # Single values must be a primitive (string, number, or boolean).
        return primitive_category(value) != ""

    def to_dict(self) -> dict:
        """
        Convert properties to dictionary for JSON serialization.

        Returns:
          - dict: Properties as dictionary
        """
        return self._properties.copy()

    def __len__(self) -> int:
        return len(self._properties)

    def __contains__(self, key: str) -> bool:
        return key in self._properties

    def __getitem__(self, key: str):
        return self._properties[key]

    def __setitem__(self, key: str, value):
        self.set_property(key, value)

    def __delitem__(self, key: str):
        self.remove_property(key)

    def items(self):
        """
        Return a view of the properties as (key, value) pairs.

        Returns:
          - dict_items: View of properties as key-value pairs
        """
        return self._properties.items()

    def keys(self):
        """
        Return a view of the property keys.

        Returns:
          - dict_keys: View of property keys
        """
        return self._properties.keys()

    def __repr__(self) -> str:
        return f"Properties({self._properties})"
