#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test cases for the Node class.
"""

import unittest
from bhopengraph.Node import Node
from bhopengraph.Properties import Properties


class TestNode(unittest.TestCase):
    """Test cases for the Node class."""

    def setUp(self):
        """Set up test fixtures."""
        self.node = Node("test_id", ["User"], Properties(name="Test User"))

    def test_init_with_valid_params(self):
        """Test Node initialization with valid parameters."""
        node = Node("test_id", ["User"], Properties(name="Test User"))
        self.assertEqual(node.id, "test_id")
        self.assertEqual(node.kinds, ["User"])
        self.assertIsInstance(node.properties, Properties)

    def test_init_with_empty_id_raises_error(self):
        """Test that Node initialization with empty ID raises ValueError."""
        with self.assertRaises(ValueError):
            Node("", ["User"])

    def test_init_with_none_id_raises_error(self):
        """Test that Node initialization with None ID raises ValueError."""
        with self.assertRaises(ValueError):
            Node(None, ["User"])

    def test_init_with_default_kinds(self):
        """Test Node initialization with default kinds."""
        node = Node("test_id")
        self.assertEqual(node.kinds, [])

    def test_init_with_default_properties(self):
        """Test Node initialization with default properties."""
        node = Node("test_id")
        self.assertIsInstance(node.properties, Properties)

    def test_add_kind(self):
        """Test adding a kind to a node."""
        self.node.add_kind("Admin")
        self.assertIn("Admin", self.node.kinds)
        self.assertEqual(len(self.node.kinds), 2)

    def test_add_duplicate_kind(self):
        """Test adding a duplicate kind doesn't create duplicates."""
        initial_count = len(self.node.kinds)
        self.node.add_kind("User")  # Already exists
        self.assertEqual(len(self.node.kinds), initial_count)

    def test_remove_kind(self):
        """Test removing a kind from a node."""
        self.node.add_kind("Admin")
        self.node.remove_kind("Admin")
        self.assertNotIn("Admin", self.node.kinds)

    def test_remove_nonexistent_kind(self):
        """Test removing a non-existent kind doesn't cause errors."""
        initial_kinds = self.node.kinds.copy()
        self.node.remove_kind("NonExistent")
        self.assertEqual(self.node.kinds, initial_kinds)

    def test_has_kind_true(self):
        """Test has_kind returns True for existing kind."""
        self.assertTrue(self.node.has_kind("User"))

    def test_has_kind_false(self):
        """Test has_kind returns False for non-existing kind."""
        self.assertFalse(self.node.has_kind("Admin"))

    def test_set_property(self):
        """Test setting a property on a node."""
        self.node.set_property("email", "test@example.com")
        self.assertEqual(self.node.get_property("email"), "test@example.com")

    def test_get_property_with_default(self):
        """Test getting a property with default value."""
        value = self.node.get_property("nonexistent", "default_value")
        self.assertEqual(value, "default_value")

    def test_get_property_without_default(self):
        """Test getting a non-existent property without default."""
        value = self.node.get_property("nonexistent")
        self.assertIsNone(value)

    def test_remove_property(self):
        """Test removing a property from a node."""
        self.node.set_property("temp", "value")
        self.node.remove_property("temp")
        self.assertIsNone(self.node.get_property("temp"))

    def test_to_dict(self):
        """Test converting node to dictionary."""
        node_dict = self.node.to_dict()
        expected = {
            "id": "test_id",
            "kinds": ["User"],
            "properties": {"name": "Test User"},
        }
        self.assertEqual(node_dict, expected)

    def test_to_dict_creates_copy(self):
        """Test that to_dict creates a copy of kinds."""
        node_dict = self.node.to_dict()
        self.node.kinds.append("Admin")
        self.assertNotEqual(node_dict["kinds"], self.node.kinds)

    def test_eq_same_node(self):
        """Test equality with same node."""
        node2 = Node("test_id", ["User"])
        self.assertEqual(self.node, node2)

    def test_eq_different_node(self):
        """Test equality with different node."""
        node2 = Node("different_id", ["User"])
        self.assertNotEqual(self.node, node2)

    def test_eq_different_type(self):
        """Test equality with different type."""
        self.assertNotEqual(self.node, "not a node")

    def test_hash_consistency(self):
        """Test that hash is consistent for same ID."""
        node2 = Node("test_id", ["Different"])
        self.assertEqual(hash(self.node), hash(node2))

    def test_hash_different_ids(self):
        """Test that different IDs have different hashes."""
        node2 = Node("different_id", ["User"])
        self.assertNotEqual(hash(self.node), hash(node2))

    def test_repr(self):
        """Test string representation of node."""
        repr_str = repr(self.node)
        self.assertIn("test_id", repr_str)
        self.assertIn("User", repr_str)
        self.assertIn("Properties", repr_str)


if __name__ == "__main__":
    unittest.main()
