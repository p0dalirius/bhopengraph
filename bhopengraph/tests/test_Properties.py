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
        self.assertTrue(self.props.is_valid_property_value("test"))

    def test_is_valid_property_value_int(self):
        """Test that integer values are valid."""
        self.assertTrue(self.props.is_valid_property_value(42))

    def test_is_valid_property_value_float(self):
        """Test that float values are valid."""
        self.assertTrue(self.props.is_valid_property_value(3.14))

    def test_is_valid_property_value_bool(self):
        """Test that boolean values are valid."""
        self.assertTrue(self.props.is_valid_property_value(True))

    def test_is_valid_property_value_none(self):
        """Test that None values are valid."""
        self.assertTrue(self.props.is_valid_property_value(None))

    def test_is_valid_property_value_list(self):
        """Test that list values are valid."""
        self.assertTrue(self.props.is_valid_property_value([1, 2, 3]))

    def test_is_valid_property_value_dict_false(self):
        """Test that dictionary values are invalid."""
        self.assertFalse(self.props.is_valid_property_value({"key": "value"}))

    def test_is_valid_property_value_function_false(self):
        """Test that function values are invalid."""
        self.assertFalse(self.props.is_valid_property_value(lambda x: x))

    def test_set_property_comprehensive_types(self):
        """Test setting properties with various Python types."""
        # Valid primitive types
        self.props.set_property("test", "string")
        self.assertEqual(self.props.get_property("test"), "string")
        
        self.props.set_property("test", 42)
        self.assertEqual(self.props.get_property("test"), 42)
        
        self.props.set_property("test", 3.14)
        self.assertEqual(self.props.get_property("test"), 3.14)
        
        self.props.set_property("test", True)
        self.assertEqual(self.props.get_property("test"), True)
        
        self.props.set_property("test", None)
        self.assertIsNone(self.props.get_property("test"))
        
        # Valid homogeneous arrays
        self.props.set_property("test", [])
        self.assertEqual(self.props.get_property("test"), [])
        
        self.props.set_property("test", ["a", "b", "c"])
        self.assertEqual(self.props.get_property("test"), ["a", "b", "c"])
        
        self.props.set_property("test", [1, 2, 3])
        self.assertEqual(self.props.get_property("test"), [1, 2, 3])
        
        self.props.set_property("test", [1.1, 2.2, 3.3])
        self.assertEqual(self.props.get_property("test"), [1.1, 2.2, 3.3])
        
        self.props.set_property("test", [True, False, True])
        self.assertEqual(self.props.get_property("test"), [True, False, True])

    def test_set_property_invalid_types_raise_error(self):
        """Test that setting invalid property types raises ValueError."""
        invalid_types = [
            {"dict": "not allowed"},
            {"nested": {"dict": "not allowed"}},
            set([1, 2, 3]),
            frozenset([1, 2, 3]),
            tuple([1, 2, 3]),
            range(10),
            lambda x: x,
            object(),
            type,
            int,
            str,
            list,
            dict,
            set,
            frozenset,
            tuple,
            range,
            lambda: None,
            complex(1, 2),
            bytes([1, 2, 3]),
            bytearray([1, 2, 3]),
            memoryview(bytes([1, 2, 3])),
        ]
        
        for invalid_type in invalid_types:
            with self.subTest(invalid_type=type(invalid_type).__name__):
                with self.assertRaises(ValueError):
                    self.props.set_property("test", invalid_type)

    def test_set_property_invalid_arrays_raise_error(self):
        """Test that setting invalid arrays raises ValueError."""
        invalid_arrays = [
            [{"dict": "not allowed"}],
            [["nested", "list"]],
            [1, "mixed", "types"],
            [1, 2.0, "mixed"],
            [True, 1, "mixed"],
            [None, 1, "mixed"],
            [1, [2, 3]],  # nested list
            [1, {"key": "value"}],  # mixed with dict
            [lambda x: x],  # function in list
            [object()],  # object in list
            [set([1, 2])],  # set in list
            [frozenset([1, 2])],  # frozenset in list
            [tuple([1, 2])],  # tuple in list
            [range(10)],  # range in list
            [complex(1, 2)],  # complex in list
            [bytes([1, 2, 3])],  # bytes in list
            [bytearray([1, 2, 3])],  # bytearray in list
            [memoryview(bytes([1, 2, 3]))],  # memoryview in list
        ]
        
        for invalid_array in invalid_arrays:
            with self.subTest(invalid_array=invalid_array):
                with self.assertRaises(ValueError):
                    self.props.set_property("test", invalid_array)

    def test_is_valid_property_value_comprehensive_types(self):
        """Test is_valid_property_value with comprehensive Python types."""
        # Valid types
        valid_types = [
            None,
            "string",
            "",
            "unicode_string_ñáéíóú",
            "string with spaces",
            "string\nwith\nnewlines",
            "string\twith\ttabs",
            "string with special chars !@#$%^&*()",
            0,
            1,
            -1,
            42,
            -42,
            999999999999999999999999999999,
            -999999999999999999999999999999,
            0.0,
            1.0,
            -1.0,
            3.14159,
            -3.14159,
            1e10,
            -1e10,
            1e-10,
            -1e-10,
            float('inf'),
            float('-inf'),
            float('nan'),
            True,
            False,
            [],
            [1, 2, 3],
            [1.1, 2.2, 3.3],
            ["a", "b", "c"],
            [True, False, True],
            [1, 1, 1],  # homogeneous ints
            [1.0, 1.0, 1.0],  # homogeneous floats
            ["a", "a", "a"],  # homogeneous strings
            [True, True, True],  # homogeneous bools
        ]
        
        for valid_type in valid_types:
            with self.subTest(valid_type=repr(valid_type)):
                self.assertTrue(self.props.is_valid_property_value(valid_type),
                              f"Expected {repr(valid_type)} to be valid")

    def test_is_valid_property_value_invalid_types(self):
        """Test is_valid_property_value with invalid Python types."""
        invalid_types = [
            {"dict": "not allowed"},
            {"nested": {"dict": "not allowed"}},
            {"empty": {}},
            set([1, 2, 3]),
            frozenset([1, 2, 3]),
            tuple([1, 2, 3]),
            tuple(),
            range(10),
            range(0),
            lambda x: x,
            lambda: None,
            object(),
            type,
            int,
            str,
            list,
            dict,
            set,
            frozenset,
            tuple,
            range,
            complex(1, 2),
            complex(0, 0),
            complex(1.5, 2.5),
            bytes([1, 2, 3]),
            bytes(),
            bytearray([1, 2, 3]),
            bytearray(),
            memoryview(bytes([1, 2, 3])),
            memoryview(bytes()),
            slice(1, 10, 2),
            slice(None),
            slice(1, None),
            slice(None, 10),
            slice(None, None, 2),
        ]
        
        for invalid_type in invalid_types:
            with self.subTest(invalid_type=type(invalid_type).__name__):
                self.assertFalse(self.props.is_valid_property_value(invalid_type),
                               f"Expected {type(invalid_type).__name__} to be invalid")

    def test_is_valid_property_value_invalid_arrays(self):
        """Test is_valid_property_value with invalid arrays."""
        invalid_arrays = [
            [{"dict": "not allowed"}],
            [["nested", "list"]],
            [1, "mixed", "types"],
            [1, 2.0, "mixed"],
            [True, 1, "mixed"],
            [None, 1, "mixed"],
            [1, [2, 3]],  # nested list
            [1, {"key": "value"}],  # mixed with dict
            [lambda x: x],  # function in list
            [object()],  # object in list
            [set([1, 2])],  # set in list
            [frozenset([1, 2])],  # frozenset in list
            [tuple([1, 2])],  # tuple in list
            [range(10)],  # range in list
            [complex(1, 2)],  # complex in list
            [bytes([1, 2, 3])],  # bytes in list
            [bytearray([1, 2, 3])],  # bytearray in list
            [memoryview(bytes([1, 2, 3]))],  # memoryview in list
            [slice(1, 10, 2)],  # slice in list
            [1, 2, 3, [4, 5]],  # mixed with nested list
            [1, 2, 3, {"key": "value"}],  # mixed with dict
            [1, 2, 3, lambda x: x],  # mixed with function
            [1, 2, 3, object()],  # mixed with object
            [1, 2, 3, set([4, 5])],  # mixed with set
            [1, 2, 3, frozenset([4, 5])],  # mixed with frozenset
            [1, 2, 3, tuple([4, 5])],  # mixed with tuple
            [1, 2, 3, range(10)],  # mixed with range
            [1, 2, 3, complex(4, 5)],  # mixed with complex
            [1, 2, 3, bytes([4, 5])],  # mixed with bytes
            [1, 2, 3, bytearray([4, 5])],  # mixed with bytearray
            [1, 2, 3, memoryview(bytes([4, 5]))],  # mixed with memoryview
            [1, 2, 3, slice(4, 10, 2)],  # mixed with slice
        ]
        
        for invalid_array in invalid_arrays:
            with self.subTest(invalid_array=invalid_array):
                self.assertFalse(self.props.is_valid_property_value(invalid_array),
                               f"Expected {repr(invalid_array)} to be invalid")

    def test_set_property_edge_cases(self):
        """Test setting properties with edge cases."""
        # Test with very long strings
        long_string = "a" * 10000
        self.props.set_property("test", long_string)
        self.assertEqual(self.props.get_property("test"), long_string)
        
        # Test with very large numbers
        large_int = 2**100
        self.props.set_property("test", large_int)
        self.assertEqual(self.props.get_property("test"), large_int)
        
        # Test with very small/large floats
        small_float = 1e-100
        self.props.set_property("test", small_float)
        self.assertEqual(self.props.get_property("test"), small_float)
        
        large_float = 1e100
        self.props.set_property("test", large_float)
        self.assertEqual(self.props.get_property("test"), large_float)
        
        # Test with special float values
        self.props.set_property("test", float('inf'))
        self.assertEqual(self.props.get_property("test"), float('inf'))
        
        self.props.set_property("test", float('-inf'))
        self.assertEqual(self.props.get_property("test"), float('-inf'))
        
        # Note: NaN comparison is tricky, so we test it separately
        self.props.set_property("test", float('nan'))
        self.assertTrue(self.props.get_property("test") != self.props.get_property("test"))  # NaN != NaN
        
        # Test with empty string
        self.props.set_property("test", "")
        self.assertEqual(self.props.get_property("test"), "")
        
        # Test with zero values
        self.props.set_property("test", 0)
        self.assertEqual(self.props.get_property("test"), 0)
        
        self.props.set_property("test", 0.0)
        self.assertEqual(self.props.get_property("test"), 0.0)
        
        # Test with single item arrays
        self.props.set_property("test", [1])
        self.assertEqual(self.props.get_property("test"), [1])
        
        self.props.set_property("test", ["single"])
        self.assertEqual(self.props.get_property("test"), ["single"])
        
        self.props.set_property("test", [True])
        self.assertEqual(self.props.get_property("test"), [True])
        

    def test_validate_comprehensive_properties(self):
        """Test validate method with comprehensive property sets."""
        # Test with all valid properties
        valid_props = Properties(
            string_prop="test",
            int_prop=42,
            float_prop=3.14,
            bool_prop=True,
            none_prop=None,
            empty_list_prop=[],
            string_list_prop=["a", "b", "c"],
            int_list_prop=[1, 2, 3],
            float_list_prop=[1.1, 2.2, 3.3],
            bool_list_prop=[True, False, True],
        )
        
        is_valid, errors = valid_props.validate()
        self.assertTrue(is_valid, f"Expected valid properties to pass validation, but got errors: {errors}")
        self.assertEqual(errors, [])

    def test_validate_invalid_properties(self):
        """Test validate method with invalid properties."""
        # Create properties with invalid values by directly manipulating _properties
        invalid_props = Properties()
        invalid_props._properties = {
            "valid_string": "test",
            "invalid_dict": {"key": "value"},
            "invalid_mixed_array": [1, "mixed", True],
            "invalid_nested_array": [[1, 2], [3, 4]],
            "invalid_function": lambda x: x,
            "invalid_set": set([1, 2, 3])
        }
        
        is_valid, errors = invalid_props.validate()
        self.assertFalse(is_valid, "Expected invalid properties to fail validation")
        self.assertGreater(len(errors), 0, "Expected validation errors")
        
        # Check that specific errors are present
        error_messages = " ".join(errors)
        self.assertIn("invalid_dict", error_messages)
        self.assertIn("invalid_mixed_array", error_messages)
        self.assertIn("invalid_nested_array", error_messages)
        self.assertIn("invalid_function", error_messages)
        self.assertIn("invalid_set", error_messages)


if __name__ == "__main__":
    unittest.main()
