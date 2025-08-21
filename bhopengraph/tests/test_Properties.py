#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test cases for the Properties class.
"""

import unittest

from bhopengraph.Properties import Properties


class TestProperties(unittest.TestCase):
    """Test cases for the Properties class."""

    def setUp(self):
        """Set up test fixtures."""
        self.props = Properties(name="Test", count=42, active=True)

    def test_init_with_kwargs(self):
        """Test Properties initialization with keyword arguments."""
        props = Properties(name="Test", count=42)
        self.assertEqual(props.get_property("name"), "Test")
        self.assertEqual(props.get_property("count"), 42)

    def test_init_without_args(self):
        """Test Properties initialization without arguments."""
        props = Properties()
        self.assertEqual(len(props), 0)

    def test_set_property_string(self):
        """Test setting a string property."""
        self.props.set_property("description", "A test description")
        self.assertEqual(self.props.get_property("description"), "A test description")

    def test_set_property_int(self):
        """Test setting an integer property."""
        self.props.set_property("age", 25)
        self.assertEqual(self.props.get_property("age"), 25)

    def test_set_property_float(self):
        """Test setting a float property."""
        self.props.set_property("score", 95.5)
        self.assertEqual(self.props.get_property("score"), 95.5)

    def test_set_property_bool(self):
        """Test setting a boolean property."""
        self.props.set_property("enabled", False)
        self.assertEqual(self.props.get_property("enabled"), False)

    def test_set_property_none(self):
        """Test setting a None property."""
        self.props.set_property("optional", None)
        self.assertIsNone(self.props.get_property("optional"))

    def test_set_property_list(self):
        """Test setting a list property."""
        self.props.set_property("tags", ["tag1", "tag2"])
        self.assertEqual(self.props.get_property("tags"), ["tag1", "tag2"])

    def test_set_property_invalid_type_raises_error(self):
        """Test that setting invalid property type raises ValueError."""
        with self.assertRaises(ValueError):
            self.props.set_property("invalid", {"dict": "not allowed"})

    def test_set_property_invalid_type_function_raises_error(self):
        """Test that setting function as property raises ValueError."""
        with self.assertRaises(ValueError):
            self.props.set_property("invalid", lambda x: x)

    def test_get_property_existing(self):
        """Test getting an existing property."""
        self.assertEqual(self.props.get_property("name"), "Test")

    def test_get_property_nonexistent_with_default(self):
        """Test getting a non-existent property with default value."""
        value = self.props.get_property("nonexistent", "default")
        self.assertEqual(value, "default")

    def test_get_property_nonexistent_without_default(self):
        """Test getting a non-existent property without default."""
        value = self.props.get_property("nonexistent")
        self.assertIsNone(value)

    def test_remove_property_existing(self):
        """Test removing an existing property."""
        self.props.remove_property("name")
        self.assertIsNone(self.props.get_property("name"))

    def test_remove_property_nonexistent(self):
        """Test removing a non-existent property doesn't cause errors."""
        initial_count = len(self.props)
        self.props.remove_property("nonexistent")
        self.assertEqual(len(self.props), initial_count)

    def test_has_property_true(self):
        """Test has_property returns True for existing property."""
        self.assertTrue(self.props.has_property("name"))

    def test_has_property_false(self):
        """Test has_property returns False for non-existing property."""
        self.assertFalse(self.props.has_property("nonexistent"))

    def test_get_all_properties(self):
        """Test getting all properties as a dictionary."""
        all_props = self.props.get_all_properties()
        expected = {"name": "Test", "count": 42, "active": True}
        self.assertEqual(all_props, expected)

    def test_get_all_properties_creates_copy(self):
        """Test that get_all_properties creates a copy."""
        all_props = self.props.get_all_properties()
        self.props.set_property("new", "value")
        self.assertNotIn("new", all_props)

    def test_clear(self):
        """Test clearing all properties."""
        self.props.clear()
        self.assertEqual(len(self.props), 0)
        self.assertIsNone(self.props.get_property("name"))

    def test_len(self):
        """Test length of properties."""
        self.assertEqual(len(self.props), 3)

    def test_contains_true(self):
        """Test contains operator returns True for existing property."""
        self.assertIn("name", self.props)

    def test_contains_false(self):
        """Test contains operator returns False for non-existing property."""
        self.assertNotIn("nonexistent", self.props)

    def test_getitem_existing(self):
        """Test getting item with bracket notation."""
        self.assertEqual(self.props["name"], "Test")

    def test_getitem_nonexistent_raises_error(self):
        """Test that getting non-existent item raises KeyError."""
        with self.assertRaises(KeyError):
            _ = self.props["nonexistent"]

    def test_setitem_valid(self):
        """Test setting item with bracket notation."""
        self.props["new_property"] = "new_value"
        self.assertEqual(self.props.get_property("new_property"), "new_value")

    def test_setitem_invalid_type_raises_error(self):
        """Test that setting invalid type with bracket notation raises ValueError."""
        with self.assertRaises(ValueError):
            self.props["invalid"] = {"dict": "not allowed"}

    def test_delitem_existing(self):
        """Test deleting item with bracket notation."""
        del self.props["name"]
        self.assertNotIn("name", self.props)

    def test_delitem_nonexistent_no_error(self):
        """Test that deleting non-existent item doesn't raise KeyError."""
        # The Properties class doesn't raise KeyError for non-existent keys
        # It just does nothing, which is the expected behavior
        initial_count = len(self.props)
        del self.props["nonexistent"]
        self.assertEqual(len(self.props), initial_count)

    def test_to_dict(self):
        """Test converting properties to dictionary."""
        props_dict = self.props.to_dict()
        expected = {"name": "Test", "count": 42, "active": True}
        self.assertEqual(props_dict, expected)

    def test_to_dict_creates_copy(self):
        """Test that to_dict creates a copy."""
        props_dict = self.props.to_dict()
        self.props.set_property("new", "value")
        self.assertNotIn("new", props_dict)

    def test_repr(self):
        """Test string representation of properties."""
        repr_str = repr(self.props)
        self.assertIn("Properties", repr_str)
        self.assertIn("name", repr_str)
        self.assertIn("Test", repr_str)

    def test_is_valid_property_value_string(self):
        """Test that string values are valid."""
        self.assertTrue(self.props._is_valid_property_value("test"))

    def test_is_valid_property_value_int(self):
        """Test that integer values are valid."""
        self.assertTrue(self.props._is_valid_property_value(42))

    def test_is_valid_property_value_float(self):
        """Test that float values are valid."""
        self.assertTrue(self.props._is_valid_property_value(3.14))

    def test_is_valid_property_value_bool(self):
        """Test that boolean values are valid."""
        self.assertTrue(self.props._is_valid_property_value(True))

    def test_is_valid_property_value_none(self):
        """Test that None values are valid."""
        self.assertTrue(self.props._is_valid_property_value(None))

    def test_is_valid_property_value_list(self):
        """Test that list values are valid."""
        self.assertTrue(self.props._is_valid_property_value([1, 2, 3]))

    def test_is_valid_property_value_dict_false(self):
        """Test that dictionary values are invalid."""
        self.assertFalse(self.props._is_valid_property_value({"key": "value"}))

    def test_is_valid_property_value_function_false(self):
        """Test that function values are invalid."""
        self.assertFalse(self.props._is_valid_property_value(lambda x: x))


if __name__ == "__main__":
    unittest.main()
