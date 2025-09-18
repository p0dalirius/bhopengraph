#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test cases for the OpenGraph class.
"""

import json
import os
import tempfile
import unittest

from bhopengraph.Edge import Edge
from bhopengraph.Node import Node
from bhopengraph.OpenGraph import OpenGraph
from bhopengraph.Properties import Properties


class TestOpenGraph(unittest.TestCase):
    """Test cases for the OpenGraph class."""

    def setUp(self):
        """Set up test fixtures."""
        self.graph = OpenGraph("TestSource")
        self.node1 = Node("node1", ["User"], Properties(name="User 1"))
        self.node2 = Node("node2", ["Computer"], Properties(name="Computer 1"))
        self.node3 = Node("node3", ["Group"], Properties(name="Group 1"))
        self.edge1 = Edge("node1", "node2", "OWNS")
        self.edge2 = Edge("node2", "node3", "MEMBER_OF")

    def test_init_with_source_kind(self):
        """Test OpenGraph initialization with source kind."""
        graph = OpenGraph("TestSource")
        self.assertEqual(graph.source_kind, "TestSource")
        self.assertEqual(len(graph.nodes), 0)
        self.assertEqual(len(graph.edges), 0)

    def test_init_without_source_kind(self):
        """Test OpenGraph initialization without source kind."""
        graph = OpenGraph()
        self.assertIsNone(graph.source_kind)

    # Edge methods tests
    def test_add_edge_without_validation_valid(self):
        """Test adding edge without validation."""
        result = self.graph.add_edge_without_validation(self.edge1)
        self.assertTrue(result)
        self.assertEqual(len(self.graph.edges), 1)

    def test_add_edge_without_validation_invalid_type(self):
        """Test adding invalid edge type without validation."""
        result = self.graph.add_edge_without_validation("not an edge")
        self.assertFalse(result)
        self.assertEqual(len(self.graph.edges), 0)

    def test_add_edges_without_validation_valid(self):
        """Test adding multiple edges without validation."""
        edges = [self.edge1, self.edge2]
        result = self.graph.add_edges_without_validation(edges)
        self.assertTrue(result)
        self.assertEqual(len(self.graph.edges), 2)

    def test_add_edges_without_validation_invalid_list(self):
        """Test adding invalid edges list without validation."""
        result = self.graph.add_edges_without_validation("not a list")
        self.assertFalse(result)
        self.assertEqual(len(self.graph.edges), 0)

    def test_add_edge_valid(self):
        """Test adding valid edge."""
        self.graph.add_node(self.node1)
        self.graph.add_node(self.node2)
        result = self.graph.add_edge(self.edge1)
        self.assertTrue(result)
        self.assertEqual(len(self.graph.edges), 1)

    def test_add_edge_start_node_not_exists(self):
        """Test adding edge with non-existent start node."""
        self.graph.add_node(self.node2)
        result = self.graph.add_edge(self.edge1)
        self.assertFalse(result)
        self.assertEqual(len(self.graph.edges), 0)

    def test_add_edge_end_node_not_exists(self):
        """Test adding edge with non-existent end node."""
        self.graph.add_node(self.node1)
        result = self.graph.add_edge(self.edge1)
        self.assertFalse(result)
        self.assertEqual(len(self.graph.edges), 0)

    def test_add_edge_duplicate(self):
        """Test adding duplicate edge."""
        self.graph.add_node(self.node1)
        self.graph.add_node(self.node2)
        self.graph.add_edge(self.edge1)
        result = self.graph.add_edge(self.edge1)
        self.assertFalse(result)
        self.assertEqual(len(self.graph.edges), 1)

    def test_add_edges_valid(self):
        """Test adding multiple valid edges."""
        self.graph.add_node(self.node1)
        self.graph.add_node(self.node2)
        self.graph.add_node(self.node3)
        edges = [self.edge1, self.edge2]
        result = self.graph.add_edges(edges)
        self.assertTrue(result)
        self.assertEqual(len(self.graph.edges), 2)

    def test_get_edges_by_kind(self):
        """Test getting edges by kind."""
        self.graph.add_node(self.node1)
        self.graph.add_node(self.node2)
        self.graph.add_edge(self.edge1)
        edges = self.graph.get_edges_by_kind("OWNS")
        self.assertEqual(len(edges), 1)
        self.assertEqual(edges[0].kind, "OWNS")

    def test_get_edges_from_node(self):
        """Test getting edges from a specific node."""
        self.graph.add_node(self.node1)
        self.graph.add_node(self.node2)
        self.graph.add_edge(self.edge1)
        edges = self.graph.get_edges_from_node("node1")
        self.assertEqual(len(edges), 1)
        self.assertEqual(edges[0].start_node, "node1")

    def test_get_edges_to_node(self):
        """Test getting edges to a specific node."""
        self.graph.add_node(self.node1)
        self.graph.add_node(self.node2)
        self.graph.add_edge(self.edge1)
        edges = self.graph.get_edges_to_node("node2")
        self.assertEqual(len(edges), 1)
        self.assertEqual(edges[0].end_node, "node2")

    def test_get_isolated_edges(self):
        """Test getting isolated edges."""
        self.graph.add_edge_without_validation(self.edge1)
        isolated_edges = self.graph.get_isolated_edges()
        self.assertEqual(len(isolated_edges), 1)

    def test_get_isolated_edges_count(self):
        """Test getting isolated edges count."""
        self.graph.add_edge_without_validation(self.edge1)
        count = self.graph.get_isolated_edges_count()
        self.assertEqual(count, 1)

    def test_get_edge_count(self):
        """Test getting total edge count."""
        self.assertEqual(self.graph.get_edge_count(), 0)
        self.graph.add_edge_without_validation(self.edge1)
        self.assertEqual(self.graph.get_edge_count(), 1)

    # Node methods tests
    def test_add_node_without_validation_valid(self):
        """Test adding node without validation."""
        result = self.graph.add_node_without_validation(self.node1)
        self.assertTrue(result)
        self.assertEqual(len(self.graph.nodes), 1)

    def test_add_node_without_validation_invalid_type(self):
        """Test adding invalid node type without validation."""
        result = self.graph.add_node_without_validation("not a node")
        self.assertFalse(result)
        self.assertEqual(len(self.graph.nodes), 0)

    def test_add_nodes_without_validation_valid(self):
        """Test adding multiple nodes without validation."""
        nodes = [self.node1, self.node2]
        result = self.graph.add_nodes_without_validation(nodes)
        self.assertTrue(result)
        self.assertEqual(len(self.graph.nodes), 2)

    def test_add_nodes_without_validation_invalid_list(self):
        """Test adding invalid nodes list without validation."""
        result = self.graph.add_nodes_without_validation("not a list")
        self.assertFalse(result)
        self.assertEqual(len(self.graph.nodes), 0)

    def test_add_node_valid(self):
        """Test adding valid node."""
        result = self.graph.add_node(self.node1)
        self.assertTrue(result)
        self.assertEqual(len(self.graph.nodes), 1)
        self.assertIn("TestSource", self.node1.kinds)

    def test_add_node_duplicate_id(self):
        """Test adding node with duplicate ID."""
        self.graph.add_node(self.node1)
        node_duplicate = Node("node1", ["Admin"])
        result = self.graph.add_node(node_duplicate)
        self.assertFalse(result)
        self.assertEqual(len(self.graph.nodes), 1)

    def test_add_node_without_source_kind(self):
        """Test adding node without source kind."""
        graph = OpenGraph()
        result = graph.add_node(self.node1)
        self.assertTrue(result)
        self.assertEqual(len(graph.nodes), 1)

    def test_add_nodes_valid(self):
        """Test adding multiple valid nodes."""
        nodes = [self.node1, self.node2]
        result = self.graph.add_nodes(nodes)
        self.assertTrue(result)
        self.assertEqual(len(self.graph.nodes), 2)

    def test_remove_node_by_id_valid(self):
        """Test removing node by ID."""
        self.graph.add_node(self.node1)
        result = self.graph.remove_node_by_id("node1")
        self.assertTrue(result)
        self.assertEqual(len(self.graph.nodes), 0)

    def test_remove_node_by_id_not_exists(self):
        """Test removing non-existent node by ID."""
        result = self.graph.remove_node_by_id("nonexistent")
        self.assertFalse(result)

    def test_get_node_by_id_exists(self):
        """Test getting existing node by ID."""
        self.graph.add_node(self.node1)
        node = self.graph.get_node_by_id("node1")
        self.assertEqual(node.id, "node1")

    def test_get_node_by_id_not_exists(self):
        """Test getting non-existent node by ID."""
        node = self.graph.get_node_by_id("nonexistent")
        self.assertIsNone(node)

    def test_get_nodes_by_kind(self):
        """Test getting nodes by kind."""
        self.graph.add_node(self.node1)
        self.graph.add_node(self.node2)
        nodes = self.graph.get_nodes_by_kind("User")
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0].id, "node1")

    def test_get_node_count(self):
        """Test getting total node count."""
        self.assertEqual(self.graph.get_node_count(), 0)
        self.graph.add_node(self.node1)
        self.assertEqual(self.graph.get_node_count(), 1)

    def test_get_isolated_nodes(self):
        """Test getting isolated nodes."""
        self.graph.add_node(self.node1)
        isolated_nodes = self.graph.get_isolated_nodes()
        self.assertEqual(len(isolated_nodes), 1)

    def test_get_isolated_nodes_count(self):
        """Test getting isolated nodes count."""
        self.graph.add_node(self.node1)
        count = self.graph.get_isolated_nodes_count()
        self.assertEqual(count, 1)

    # Path methods tests
    def test_find_paths_same_node(self):
        """Test finding paths from node to itself."""
        self.graph.add_node(self.node1)
        paths = self.graph.find_paths("node1", "node1")
        self.assertEqual(paths, [["node1"]])

    def test_find_paths_direct_connection(self):
        """Test finding paths with direct connection."""
        self.graph.add_node(self.node1)
        self.graph.add_node(self.node2)
        self.graph.add_edge(self.edge1)
        paths = self.graph.find_paths("node1", "node2")
        self.assertEqual(paths, [["node1", "node2"]])

    def test_find_paths_no_connection(self):
        """Test finding paths with no connection."""
        self.graph.add_node(self.node1)
        self.graph.add_node(self.node2)
        paths = self.graph.find_paths("node1", "node2")
        self.assertEqual(paths, [])

    def test_find_paths_with_max_depth(self):
        """Test finding paths with max depth limit."""
        self.graph.add_node(self.node1)
        self.graph.add_node(self.node2)
        self.graph.add_node(self.node3)
        self.graph.add_edge(self.edge1)
        self.graph.add_edge(self.edge2)
        paths = self.graph.find_paths("node1", "node3", max_depth=1)
        self.assertEqual(paths, [])

    def test_find_paths_node_not_exists(self):
        """Test finding paths with non-existent nodes."""
        paths = self.graph.find_paths("nonexistent1", "nonexistent2")
        self.assertEqual(paths, [])

    def test_get_connected_components_empty(self):
        """Test getting connected components of empty graph."""
        components = self.graph.get_connected_components()
        self.assertEqual(components, [])

    def test_get_connected_components_single_node(self):
        """Test getting connected components with single node."""
        self.graph.add_node(self.node1)
        components = self.graph.get_connected_components()
        self.assertEqual(len(components), 1)
        self.assertEqual(len(components[0]), 1)

    def test_get_connected_components_connected(self):
        """Test getting connected components with connected nodes."""
        self.graph.add_node(self.node1)
        self.graph.add_node(self.node2)
        self.graph.add_edge(self.edge1)
        components = self.graph.get_connected_components()
        self.assertEqual(len(components), 1)
        self.assertEqual(len(components[0]), 2)

    # Validation and export methods tests
    def test_validate_graph_empty(self):
        """Test validating empty graph."""
        is_valid, errors = self.graph.validate_graph()
        self.assertTrue(is_valid)
        self.assertEqual(errors, [])

    def test_validate_graph_with_isolated_edge(self):
        """Test validating graph with isolated edge."""
        self.graph.add_edge_without_validation(self.edge1)
        is_valid, errors = self.graph.validate_graph()
        self.assertFalse(is_valid)
        self.assertEqual(len(errors), 2)  # Both start and end nodes missing
        self.assertTrue(any("Start node 'node1' does not exist" in error for error in errors))
        self.assertTrue(any("End node 'node2' does not exist" in error for error in errors))

    def test_validate_graph_with_isolated_node(self):
        """Test validating graph with isolated node."""
        self.graph.add_node(self.node1)
        is_valid, errors = self.graph.validate_graph()
        self.assertFalse(is_valid)
        self.assertEqual(len(errors), 1)  # Isolated node
        self.assertTrue(any("Node 'node1' is isolated" in error for error in errors))

    def test_validate_graph_with_invalid_node(self):
        """Test validating graph with invalid node."""
        # Create a node with invalid data by directly modifying it
        invalid_node = Node("invalid_node", ["User"])
        invalid_node.id = 123  # Make it non-string
        self.graph.add_node_without_validation(invalid_node)
        
        is_valid, errors = self.graph.validate_graph()
        self.assertFalse(is_valid)
        self.assertTrue(any("Node '123': Node ID must be a string" in error for error in errors))

    def test_validate_graph_with_invalid_edge(self):
        """Test validating graph with invalid edge."""
        # Create an edge with invalid data by directly modifying it
        invalid_edge = Edge("node1", "node2", "OWNS")
        invalid_edge.start_match_by = "invalid"  # Make it invalid
        self.graph.add_node(self.node1)
        self.graph.add_node(self.node2)
        self.graph.add_edge_without_validation(invalid_edge)
        
        is_valid, errors = self.graph.validate_graph()
        self.assertFalse(is_valid)
        self.assertTrue(any("Start match_by must be either 'id' or 'name'" in error for error in errors))

    def test_validate_graph_with_valid_graph(self):
        """Test validating a completely valid graph."""
        self.graph.add_node(self.node1)
        self.graph.add_node(self.node2)
        self.graph.add_edge(self.edge1)
        
        is_valid, errors = self.graph.validate_graph()
        self.assertTrue(is_valid)
        self.assertEqual(errors, [])

    def test_export_json_with_metadata(self):
        """Test exporting graph to JSON with metadata."""
        self.graph.add_node(self.node1)
        json_str = self.graph.export_json(include_metadata=True)
        self.assertIn("TestSource", json_str)
        self.assertIn("node1", json_str)

    def test_export_json_without_metadata(self):
        """Test exporting graph to JSON without metadata."""
        self.graph.add_node(self.node1)
        json_str = self.graph.export_json(include_metadata=False)
        self.assertNotIn("metadata", json_str)
        self.assertIn("node1", json_str)

    def test_export_to_file_success(self):
        """Test exporting graph to file successfully."""
        self.graph.add_node(self.node1)
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json") as f:
            filename = f.name

        try:
            result = self.graph.export_to_file(filename)
            self.assertTrue(result)
            self.assertTrue(os.path.exists(filename))

            # Verify file contents
            with open(filename, "r") as f:
                content = f.read()
                self.assertIn("node1", content)
        finally:
            os.unlink(filename)

    def test_export_to_file_failure(self):
        """Test exporting graph to file with failure."""
        # Try to write to a directory (should fail)
        result = self.graph.export_to_file("/tmp/")
        self.assertFalse(result)

    # Import methods tests
    def test_import_from_dict_valid(self):
        """Test importing graph from valid dictionary."""
        # Create test data
        test_data = {
            "graph": {
                "nodes": [
                    {
                        "id": "test_node1",
                        "kinds": ["User"],
                        "properties": {"name": "Test User 1"},
                    },
                    {
                        "id": "test_node2",
                        "kinds": ["Computer"],
                        "properties": {"name": "Test Computer 1"},
                    },
                ],
                "edges": [
                    {
                        "kind": "OWNS",
                        "start": {"value": "test_node1", "match_by": "id"},
                        "end": {"value": "test_node2", "match_by": "id"},
                    }
                ],
            },
            "metadata": {"source_kind": "TestImport"},
        }

        # Clear existing graph and import
        self.graph.clear()
        result = self.graph.import_from_dict(test_data)

        self.assertTrue(result)
        self.assertEqual(self.graph.source_kind, "TestImport")
        self.assertEqual(len(self.graph.nodes), 2)
        self.assertEqual(len(self.graph.edges), 1)

        # Verify nodes were imported correctly
        node1 = self.graph.get_node_by_id("test_node1")
        node2 = self.graph.get_node_by_id("test_node2")
        self.assertIsNotNone(node1)
        self.assertIsNotNone(node2)
        self.assertEqual(node1.get_property("name"), "Test User 1")
        self.assertEqual(node2.get_property("name"), "Test Computer 1")

        # Verify edges were imported correctly
        edges = self.graph.get_edges_from_node("test_node1")
        self.assertEqual(len(edges), 1)
        self.assertEqual(edges[0].kind, "OWNS")
        self.assertEqual(edges[0].end_node, "test_node2")

    def test_import_from_dict_invalid_structure(self):
        """Test importing graph from invalid dictionary structure."""
        invalid_data = {"invalid_key": "invalid_value"}

        self.graph.clear()
        result = self.graph.import_from_dict(invalid_data)

        self.assertFalse(result)
        self.assertEqual(self.graph.get_node_count(), 0)
        self.assertEqual(self.graph.get_edge_count(), 0)

    def test_import_from_dict_missing_graph_key(self):
        """Test importing graph from dictionary missing 'graph' key."""
        invalid_data = {"metadata": {"source_kind": "Test"}}

        self.graph.clear()
        result = self.graph.import_from_dict(invalid_data)

        self.assertFalse(result)
        self.assertEqual(self.graph.get_node_count(), 0)
        self.assertEqual(self.graph.get_edge_count(), 0)

    def test_import_from_dict_with_nodes_only(self):
        """Test importing graph with only nodes (no edges)."""
        test_data = {
            "graph": {
                "nodes": [
                    {
                        "id": "test_node1",
                        "kinds": ["User"],
                        "properties": {"name": "Test User 1"},
                    }
                ]
            }
        }

        self.graph.clear()
        result = self.graph.import_from_dict(test_data)

        self.assertTrue(result)
        self.assertEqual(self.graph.get_node_count(), 1)
        self.assertEqual(self.graph.get_edge_count(), 0)

    def test_import_from_dict_with_edges_only(self):
        """Test importing graph with only edges (no nodes)."""
        test_data = {
            "graph": {
                "edges": [
                    {
                        "kind": "OWNS",
                        "start": {"value": "test_node1", "match_by": "id"},
                        "end": {"value": "test_node2", "match_by": "id"},
                    }
                ]
            }
        }

        self.graph.clear()
        result = self.graph.import_from_dict(test_data)

        self.assertTrue(result)
        self.assertEqual(self.graph.get_node_count(), 0)
        self.assertEqual(self.graph.get_edge_count(), 1)
        self.assertEqual(self.graph.get_isolated_edges_count(), 1)

    def test_import_from_dict_with_metadata(self):
        """Test importing graph with metadata."""
        test_data = {
            "graph": {"nodes": []},
            "metadata": {"source_kind": "NewSourceKind"},
        }

        self.graph.clear()
        result = self.graph.import_from_dict(test_data)

        self.assertTrue(result)
        self.assertEqual(self.graph.source_kind, "NewSourceKind")

    def test_import_from_dict_without_metadata(self):
        """Test importing graph without metadata."""
        test_data = {"graph": {"nodes": []}}

        self.graph.clear()
        self.graph.source_kind = None  # Clear the source_kind from setUp
        result = self.graph.import_from_dict(test_data)

        self.assertTrue(result)
        self.assertIsNone(self.graph.source_kind)

    def test_import_from_dict_malformed_node_data(self):
        """Test importing graph with malformed node data."""
        test_data = {
            "graph": {
                "nodes": [
                    {
                        "id": "test_node1",
                        "kinds": ["User"],
                        "properties": {"name": "Test User 1"},
                    },
                    {"invalid_key": "invalid_value"},  # Malformed node
                ]
            }
        }

        self.graph.clear()
        result = self.graph.import_from_dict(test_data)

        # Should still succeed but only import valid nodes
        self.assertTrue(result)
        self.assertEqual(len(self.graph.nodes), 1)  # Only one valid node imported

    def test_import_from_dict_malformed_edge_data(self):
        """Test importing graph with malformed edge data."""
        test_data = {
            "graph": {
                "nodes": [
                    {
                        "id": "test_node1",
                        "kinds": ["User"],
                        "properties": {"name": "Test User 1"},
                    }
                ],
                "edges": [
                    {
                        "kind": "OWNS",
                        "start": {"value": "test_node1", "match_by": "id"},
                        "end": {"value": "test_node2", "match_by": "id"},
                    },
                    {"invalid_key": "invalid_value"},  # Malformed edge
                ],
            }
        }

        self.graph.clear()
        result = self.graph.import_from_dict(test_data)

        # Should still succeed but only import valid edges
        self.assertTrue(result)
        self.assertEqual(len(self.graph.edges), 1)  # Only one valid edge imported

    def test_import_from_json_valid(self):
        """Test importing graph from valid JSON string."""
        json_data = """{
            "graph": {
                "nodes": [
                    {
                        "id": "json_node1",
                        "kinds": ["User"],
                        "properties": {"name": "JSON User 1"}
                    }
                ],
                "edges": [
                    {
                        "kind": "MEMBER_OF",
                        "start": {
                            "value": "json_node1",
                            "match_by": "id"
                        },
                        "end": {
                            "value": "json_node2",
                            "match_by": "id"
                        }
                    }
                ]
            },
            "metadata": {
                "source_kind": "JSONImport"
            }
        }"""

        self.graph.clear()
        result = self.graph.import_from_json(json_data)

        self.assertTrue(result)
        self.assertEqual(self.graph.source_kind, "JSONImport")
        self.assertEqual(self.graph.get_node_count(), 1)
        self.assertEqual(self.graph.get_edge_count(), 1)

    def test_import_from_json_invalid_json(self):
        """Test importing graph from invalid JSON string."""
        invalid_json = '{"invalid": json}'

        self.graph.clear()
        # This should fail due to JSON parsing error
        with self.assertRaises(json.JSONDecodeError):
            self.graph.import_from_json(invalid_json)

    def test_import_from_file_success(self):
        """Test importing graph from file successfully."""
        # Create a temporary file with test data
        test_data = {
            "graph": {
                "nodes": [
                    {
                        "id": "file_node1",
                        "kinds": ["User"],
                        "properties": {"name": "File User 1"},
                    }
                ],
                "edges": [
                    {
                        "kind": "OWNS",
                        "start": {"value": "file_node1", "match_by": "id"},
                        "end": {"value": "file_node2", "match_by": "id"},
                    }
                ],
            },
            "metadata": {"source_kind": "FileImport"},
        }

        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json") as f:
            filename = f.name
            f.write(json.dumps(test_data))

        try:
            self.graph.clear()
            result = self.graph.import_from_file(filename)

            self.assertTrue(result)
            self.assertEqual(self.graph.source_kind, "FileImport")
            self.assertEqual(self.graph.get_node_count(), 1)
            self.assertEqual(self.graph.get_edge_count(), 1)
        finally:
            os.unlink(filename)

    def test_import_from_file_not_exists(self):
        """Test importing graph from non-existent file."""
        result = self.graph.import_from_file("/nonexistent/file.json")
        self.assertFalse(result)

    def test_import_from_file_invalid_json(self):
        """Test importing graph from file with invalid JSON."""
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json") as f:
            filename = f.name
            f.write('{"invalid": json}')

        try:
            self.graph.clear()
            result = self.graph.import_from_file(filename)
            self.assertFalse(result)
        finally:
            os.unlink(filename)

    def test_import_from_file_directory(self):
        """Test importing graph from directory (should fail)."""
        result = self.graph.import_from_file("/tmp/")
        self.assertFalse(result)

    def test_import_preserves_existing_data(self):
        """Test that import doesn't clear existing data by default."""
        # Add some existing data
        self.graph.add_node(self.node1)
        self.graph.add_edge_without_validation(self.edge1)

        # Import new data
        test_data = {
            "graph": {
                "nodes": [
                    {
                        "id": "new_node1",
                        "kinds": ["User"],
                        "properties": {"name": "New User 1"},
                    }
                ]
            }
        }

        result = self.graph.import_from_dict(test_data)

        self.assertTrue(result)
        # Should have both old and new data
        self.assertEqual(self.graph.get_node_count(), 2)
        self.assertEqual(self.graph.get_edge_count(), 1)

        # Verify both nodes exist
        self.assertIsNotNone(self.graph.get_node_by_id("node1"))
        self.assertIsNotNone(self.graph.get_node_by_id("new_node1"))

    def test_import_overwrites_source_kind(self):
        """Test that import overwrites existing source_kind."""
        # Set initial source_kind
        self.graph.source_kind = "InitialSource"

        # Import with new source_kind
        test_data = {"graph": {"nodes": []}, "metadata": {"source_kind": "NewSource"}}

        result = self.graph.import_from_dict(test_data)

        self.assertTrue(result)
        self.assertEqual(self.graph.source_kind, "NewSource")

    # Other methods tests
    def test_clear(self):
        """Test clearing the graph."""
        self.graph.add_node(self.node1)
        self.graph.add_edge_without_validation(self.edge1)
        self.graph.clear()
        self.assertEqual(self.graph.get_node_count(), 0)
        self.assertEqual(self.graph.get_edge_count(), 0)

    def test_len(self):
        """Test length of graph."""
        self.assertEqual(self.graph.get_node_count(), 0)
        self.graph.add_node(self.node1)
        self.assertEqual(self.graph.get_node_count(), 1)
        self.graph.add_edge_without_validation(self.edge1)
        self.assertEqual(self.graph.get_edge_count(), 1)

    def test_repr(self):
        """Test string representation of graph."""
        repr_str = repr(self.graph)
        self.assertIn("OpenGraph", repr_str)
        self.assertIn("TestSource", repr_str)


if __name__ == "__main__":
    unittest.main()
