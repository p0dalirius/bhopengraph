#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test cases for the Edge class.
"""

import unittest

from bhopengraph.Edge import Edge
from bhopengraph.Properties import Properties


class TestEdge(unittest.TestCase):
    """Test cases for the Edge class."""

    def setUp(self):
        """Set up test fixtures."""
        self.edge = Edge("start_node", "end_node", "OWNS", Properties(weight=1))

    def test_init_with_valid_params(self):
        """Test Edge initialization with valid parameters."""
        edge = Edge("start_node", "end_node", "OWNS", Properties(weight=1))
        self.assertEqual(edge.start_node_id, "start_node")
        self.assertEqual(edge.end_node_id, "end_node")
        self.assertEqual(edge.kind, "OWNS")
        self.assertIsInstance(edge.properties, Properties)

    def test_init_with_empty_start_node_raises_error(self):
        """Test that Edge initialization with empty start node raises ValueError."""
        with self.assertRaises(ValueError):
            Edge("", "end_node", "OWNS")

    def test_init_with_none_start_node_raises_error(self):
        """Test that Edge initialization with None start node raises ValueError."""
        with self.assertRaises(ValueError):
            Edge(None, "end_node", "OWNS")

    def test_init_with_empty_end_node_raises_error(self):
        """Test that Edge initialization with empty end node raises ValueError."""
        with self.assertRaises(ValueError):
            Edge("start_node", "", "OWNS")

    def test_init_with_none_end_node_raises_error(self):
        """Test that Edge initialization with None end node raises ValueError."""
        with self.assertRaises(ValueError):
            Edge("start_node", None, "OWNS")

    def test_init_with_empty_kind_raises_error(self):
        """Test that Edge initialization with empty kind raises ValueError."""
        with self.assertRaises(ValueError):
            Edge("start_node", "end_node", "")

    def test_init_with_none_kind_raises_error(self):
        """Test that Edge initialization with None kind raises ValueError."""
        with self.assertRaises(ValueError):
            Edge("start_node", "end_node", None)

    def test_init_with_default_properties(self):
        """Test Edge initialization with default properties."""
        edge = Edge("start_node", "end_node", "OWNS")
        self.assertIsInstance(edge.properties, Properties)

    def test_set_property(self):
        """Test setting a property on an edge."""
        self.edge.set_property("color", "red")
        self.assertEqual(self.edge.get_property("color"), "red")

    def test_get_property_with_default(self):
        """Test getting a property with default value."""
        value = self.edge.get_property("nonexistent", "default_value")
        self.assertEqual(value, "default_value")

    def test_get_property_without_default(self):
        """Test getting a non-existent property without default."""
        value = self.edge.get_property("nonexistent")
        self.assertIsNone(value)

    def test_remove_property(self):
        """Test removing a property from an edge."""
        self.edge.set_property("temp", "value")
        self.edge.remove_property("temp")
        self.assertIsNone(self.edge.get_property("temp"))

    def test_to_dict_with_properties(self):
        """Test converting edge to dictionary with properties."""
        edge_dict = self.edge.to_dict()
        expected = {
            "kind": "OWNS",
            "start": {"value": "start_node", "match_by": "id"},
            "end": {"value": "end_node", "match_by": "id"},
            "properties": {"weight": 1},
        }
        self.assertEqual(edge_dict, expected)

    def test_to_dict_without_properties(self):
        """Test converting edge to dictionary without properties."""
        edge = Edge("start_node", "end_node", "OWNS")
        edge_dict = edge.to_dict()
        expected = {
            "kind": "OWNS",
            "start": {"value": "start_node", "match_by": "id"},
            "end": {"value": "end_node", "match_by": "id"},
        }
        self.assertEqual(edge_dict, expected)

    def test_to_dict_empty_properties(self):
        """Test converting edge to dictionary with empty properties."""
        edge = Edge("start_node", "end_node", "OWNS", Properties())
        edge_dict = edge.to_dict()
        expected = {
            "kind": "OWNS",
            "start": {"value": "start_node", "match_by": "id"},
            "end": {"value": "end_node", "match_by": "id"},
        }
        self.assertEqual(edge_dict, expected)

    def test_get_start_node_id(self):
        """Test getting start node ID."""
        self.assertEqual(self.edge.get_start_node_id(), "start_node")

    def test_get_end_node_id(self):
        """Test getting end node ID."""
        self.assertEqual(self.edge.get_end_node_id(), "end_node")

    def test_get_kind(self):
        """Test getting edge kind."""
        self.assertEqual(self.edge.get_kind(), "OWNS")

    def test_eq_same_edge(self):
        """Test equality with same edge."""
        edge2 = Edge("start_node", "end_node", "OWNS")
        self.assertEqual(self.edge, edge2)

    def test_eq_different_start_node(self):
        """Test equality with different start node."""
        edge2 = Edge("different_start", "end_node", "OWNS")
        self.assertNotEqual(self.edge, edge2)

    def test_eq_different_end_node(self):
        """Test equality with different end node."""
        edge2 = Edge("start_node", "different_end", "OWNS")
        self.assertNotEqual(self.edge, edge2)

    def test_eq_different_kind(self):
        """Test equality with different kind."""
        edge2 = Edge("start_node", "end_node", "DIFFERENT")
        self.assertNotEqual(self.edge, edge2)

    def test_eq_different_type(self):
        """Test equality with different type."""
        self.assertNotEqual(self.edge, "not an edge")

    def test_hash_consistency(self):
        """Test that hash is consistent for same edge properties."""
        edge2 = Edge("start_node", "end_node", "OWNS")
        self.assertEqual(hash(self.edge), hash(edge2))

    def test_hash_different_edges(self):
        """Test that different edges have different hashes."""
        edge2 = Edge("different_start", "end_node", "OWNS")
        self.assertNotEqual(hash(self.edge), hash(edge2))

    def test_repr(self):
        """Test string representation of edge."""
        repr_str = repr(self.edge)
        self.assertIn("start_node", repr_str)
        self.assertIn("end_node", repr_str)
        self.assertIn("OWNS", repr_str)
        self.assertIn("Properties", repr_str)


if __name__ == "__main__":
    unittest.main()
