#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test cases for the Edge class.
"""

import unittest

from bhopengraph.Edge import (
    MATCH_BY_ID,
    MATCH_BY_NAME,
    MATCH_BY_PROPERTY,
    Edge,
    Endpoint,
    PropertyMatcher,
)
from bhopengraph.Properties import Properties


class TestEdge(unittest.TestCase):
    """Test cases for the Edge class."""

    def setUp(self):
        """Set up test fixtures."""
        self.edge = Edge("start_node", "end_node", "OWNS", Properties(weight=1))

    def test_init_with_valid_params(self):
        """Test Edge initialization with valid parameters."""
        edge = Edge("start_node", "end_node", "OWNS", Properties(weight=1))
        self.assertEqual(edge.start_node, "start_node")
        self.assertEqual(edge.end_node, "end_node")
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

    def test_get_start_node(self):
        """Test getting start node ID."""
        self.assertEqual(self.edge.get_start_node(), "start_node")

    def test_get_end_node(self):
        """Test getting end node ID."""
        self.assertEqual(self.edge.get_end_node(), "end_node")

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


class TestEdgeKindValidation(unittest.TestCase):
    """Test cases for edge kind validation (regex + reserved prefix)."""

    def test_valid_kinds(self):
        """Test that schema-compliant kinds are accepted."""
        for kind in ["Knows", "CONNECTS_TO", "Okta_ResetPassword", "a1_B2"]:
            with self.subTest(kind=kind):
                edge = Edge("a", "b", kind)
                self.assertEqual(edge.kind, kind)

    def test_invalid_kinds_raise(self):
        """Test that kinds with illegal characters or reserved prefix raise."""
        invalid = [
            "Has Access",  # space
            "Reset-Password",  # hyphen
            "Owns!",  # punctuation
            "tag_custom",  # reserved tag_ prefix
            "TAG_Custom",  # reserved prefix, uppercase
            "Tag_Custom",  # reserved prefix, mixed case
        ]
        for kind in invalid:
            with self.subTest(kind=kind):
                with self.assertRaises(ValueError):
                    Edge("a", "b", kind)


class TestPropertyMatcher(unittest.TestCase):
    """Test cases for the PropertyMatcher class."""

    def test_to_dict(self):
        """Test serialization of a property matcher."""
        matcher = PropertyMatcher(key="username", value="alice.smith")
        self.assertEqual(
            matcher.to_dict(),
            {"key": "username", "operator": "equals", "value": "alice.smith"},
        )

    def test_validate_requires_key(self):
        """Test that a matcher without a key is invalid."""
        is_valid, _ = PropertyMatcher(key="", value="x").validate()
        self.assertFalse(is_valid)

    def test_equality(self):
        """Test matcher equality and hashing."""
        a = PropertyMatcher("k", "v")
        b = PropertyMatcher("k", "v")
        self.assertEqual(a, b)
        self.assertEqual(hash(a), hash(b))


class TestEndpoint(unittest.TestCase):
    """Test cases for the Endpoint class and match_by strategies."""

    def test_by_id(self):
        """Test an id-matched endpoint serializes to value + match_by."""
        ep = Endpoint.by_id("server-1")
        self.assertEqual(ep.to_dict(), {"match_by": "id", "value": "server-1"})

    def test_by_name_with_kind(self):
        """Test a name-matched endpoint includes the kind filter."""
        ep = Endpoint.by_name("alice", "User")
        self.assertEqual(
            ep.to_dict(), {"match_by": "name", "value": "alice", "kind": "User"}
        )
        self.assertNotIn("property_matchers", ep.to_dict())

    def test_by_property(self):
        """Test a property-matched endpoint serializes property_matchers."""
        matchers = [
            PropertyMatcher("username", "alice.smith"),
            PropertyMatcher("active", True),
        ]
        ep = Endpoint.by_property(matchers, "User")
        d = ep.to_dict()
        self.assertEqual(d["match_by"], "property")
        self.assertEqual(d["kind"], "User")
        self.assertNotIn("value", d)
        self.assertEqual(len(d["property_matchers"]), 2)
        self.assertEqual(
            d["property_matchers"][0],
            {"key": "username", "operator": "equals", "value": "alice.smith"},
        )

    def test_validate_id_requires_value(self):
        """Test that an id endpoint with no value is invalid."""
        is_valid, _ = Endpoint.by_id("").validate()
        self.assertFalse(is_valid)

    def test_validate_property_requires_matcher(self):
        """Test that a property endpoint with no matchers is invalid."""
        is_valid, _ = Endpoint.by_property([], "User").validate()
        self.assertFalse(is_valid)

    def test_validate_property_matcher_requires_key(self):
        """Test that a property matcher with an empty key is invalid."""
        ep = Endpoint.by_property([PropertyMatcher("", "x")], "")
        is_valid, _ = ep.validate()
        self.assertFalse(is_valid)

    def test_constants(self):
        """Test the exported match_by constants."""
        self.assertEqual(MATCH_BY_ID, "id")
        self.assertEqual(MATCH_BY_NAME, "name")
        self.assertEqual(MATCH_BY_PROPERTY, "property")


class TestEdgeWithEndpoints(unittest.TestCase):
    """Test cases for Edge.with_endpoints and round-tripping."""

    def test_match_by_name(self):
        """Test building an edge whose endpoints match by name."""
        edge = Edge.with_endpoints(
            Endpoint.by_name("alice", "User"),
            Endpoint.by_name("file-server-1", "Server"),
            "HasAccess",
        )
        d = edge.to_dict()
        self.assertEqual(d["start"]["match_by"], "name")
        self.assertEqual(d["start"]["value"], "alice")
        self.assertEqual(d["start"]["kind"], "User")

    def test_match_by_property(self):
        """Test building an edge with a property-matched start endpoint."""
        matchers = [PropertyMatcher("username", "alice.smith")]
        edge = Edge.with_endpoints(
            Endpoint.by_property(matchers, "User"),
            Endpoint.by_id("server-1"),
            "CustomRelationship",
        )
        d = edge.to_dict()
        self.assertEqual(d["start"]["match_by"], "property")
        self.assertNotIn("value", d["start"])
        self.assertEqual(d["end"], {"match_by": "id", "value": "server-1"})

    def test_from_dict_property_matchers(self):
        """Test that from_dict reconstructs a property-matched endpoint."""
        edge_data = {
            "kind": "CustomRelationship",
            "start": {
                "match_by": "property",
                "kind": "User",
                "property_matchers": [
                    {"key": "username", "operator": "equals", "value": "alice.smith"}
                ],
            },
            "end": {"match_by": "id", "value": "server-1"},
        }
        edge = Edge.from_dict(edge_data)
        self.assertIsNotNone(edge)
        self.assertEqual(edge.start.match_by, "property")
        self.assertEqual(len(edge.start.property_matchers), 1)
        self.assertEqual(edge.start.property_matchers[0].key, "username")
        # Round-trips back to the same shape.
        self.assertEqual(edge.to_dict()["start"], edge_data["start"])

    def test_equal_across_match_strategies(self):
        """Test that edges differing only in match strategy are not equal."""
        by_id = Edge("a", "b", "K")
        by_name = Edge.with_endpoints(
            Endpoint.by_name("a", ""), Endpoint.by_id("b"), "K"
        )
        self.assertNotEqual(by_id, by_name)

    def test_invalid_property_endpoint_raises(self):
        """Test that an edge with an invalid property endpoint raises."""
        with self.assertRaises(ValueError):
            Edge.with_endpoints(
                Endpoint.by_property([], "User"), Endpoint.by_id("b"), "K"
            )


if __name__ == "__main__":
    unittest.main()
