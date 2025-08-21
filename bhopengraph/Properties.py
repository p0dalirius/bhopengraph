#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File name          : Properties.py
# Author             : Remi Gascou (@podalirius_)
# Date created       : 12 Aug 2025


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
          - value: Property value (must be primitive type: str, int, float, bool, None, list)
        """
        if self._is_valid_property_value(value):
            self._properties[key] = value
        else:
            raise ValueError(
                f"Property value must be a primitive type (str, int, float, bool, None, list), got {type(value)}"
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

    def _is_valid_property_value(self, value) -> bool:
        """
        Check if a value is a valid property type.

        Args:
          - value: Value to check

        Returns:
          - bool: True if value is valid, False otherwise
        """
        return value is None or isinstance(value, (str, int, float, bool, list))

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

    def __repr__(self) -> str:
        return f"Properties({self._properties})"
