#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File name          : OpenGraph.py
# Author             : Remi Gascou (@podalirius_)
# Date created       : 12 Aug 2025

import json
from typing import Dict, List, Optional, Set

from bhopengraph.Edge import Edge
from bhopengraph.Node import Node


class OpenGraph(object):
    """
    OpenGraph class for managing a graph structure compatible with BloodHound OpenGraph.

    Follows BloodHound OpenGraph schema requirements and best practices.

    Sources:

    - https://bloodhound.specterops.io/opengraph/schema#opengraph

    - https://bloodhound.specterops.io/opengraph/schema#minimal-working-json
    
    - https://bloodhound.specterops.io/opengraph/best-practices
    """

    def __init__(self, source_kind: str = None):
        """
        Initialize an OpenGraph.

        Args:
          - source_kind (str): Optional source kind for all nodes in the graph
        """
        self.nodes: Dict[str, Node] = {}
        self.edges: List[Edge] = []

        self.source_kind = source_kind

    # Edges methods

    def add_edge(self, edge: Edge) -> bool:
        """
        Add an edge to the graph if it doesn't already exist and if the start and end nodes exist.

        Args:
          - edge (Edge): Edge to add

        Returns:
          - bool: True if edge was added, False if start or end node doesn't exist
        """
        if edge.start_node not in self.nodes:
            return False
        if edge.end_node not in self.nodes:
            return False

        for existing_edge in self.edges:
            if (
                existing_edge.start_node == edge.start_node
                and existing_edge.end_node == edge.end_node
                and existing_edge.kind == edge.kind
            ):
                return False

        self.edges.append(edge)
        return True

    def add_edges(self, edges: List[Edge]) -> bool:
        """
        Add a list of edges to the graph.

        Returns:
            - bool: True if all edges were added successfully, False if any failed
        """
        success = True
        for edge in edges:
            if not self.add_edge(edge):
                success = False
        return success

    def add_edge_without_validation(self, edge: Edge) -> bool:
        """
        Add an edge to the graph.

        Args:
          - edge (Edge): Edge to add

        Returns:
          - bool: True if edge was added, False if edge is invalid
        """
        if not isinstance(edge, Edge):
            return False

        self.edges.append(edge)
        return True

    def add_edges_without_validation(self, edges: List[Edge]) -> bool:
        """
        Add a list of edges to the graph without validation.

        Args:
            - edges (List[Edge]): List of edges to add

        Returns:
            - bool: True if edges were added successfully
        """
        if not isinstance(edges, list):
            return False

        for edge in edges:
            self.add_edge_without_validation(edge)
        return True

    def get_edges_by_kind(self, kind: str) -> List[Edge]:
        """
        Get all edges of a specific kind.

        Args:
          - kind (str): Kind/type to filter by

        Returns:
          - List[Edge]: List of edges with the specified kind
        """
        return [edge for edge in self.edges if edge.kind == kind]

    def get_edges_from_node(self, node_id: str) -> List[Edge]:
        """
        Get all edges starting from a specific node.

        Args:
          - node_id (str): ID of the source node

        Returns:
          - List[Edge]: List of edges starting from the specified node
        """
        return [edge for edge in self.edges if edge.start_node == node_id]

    def get_edges_to_node(self, node_id: str) -> List[Edge]:
        """
        Get all edges ending at a specific node.

        Args:
          - node_id (str): ID of the destination node

        Returns:
          - List[Edge]: List of edges ending at the specified node
        """
        return [edge for edge in self.edges if edge.end_node == node_id]

    def get_isolated_edges(self) -> List[Edge]:
        """
        Get all edges that have no start or end node.
        These are edges that are not connected to any other nodes in the graph.

        Returns:
            - List[Edge]: List of edges with no start or end node
        """
        return [
            edge
            for edge in self.edges
            if edge.start_node not in self.nodes or edge.end_node not in self.nodes
        ]

    def get_isolated_edges_count(self) -> int:
        """
        Get the total number of Isolated edges in the graph.
        These are edges that are not connected to any other nodes in the graph.

        Returns:
            - int: Number of Isolated edges
        """
        return len(self.get_isolated_edges())

    def get_edge_count(self) -> int:
        """
        Get the total number of edges in the graph.

        Returns:
          - int: Number of edges
        """
        return len(self.edges)

    # Nodes methods

    def add_node(self, node: Node) -> bool:
        """
        Add a node to the graph.

        Args:
          - node (Node): Node to add

        Returns:
          - bool: True if node was added, False if node with same ID already exists
        """
        if node.id in self.nodes:
            return False

        # Add source_kind to node kinds if specified
        if self.source_kind and self.source_kind not in node.kinds:
            node.add_kind(self.source_kind)

        self.nodes[node.id] = node
        return True

    def add_nodes(self, nodes: List[Node]) -> bool:
        """
        Add a list of nodes to the graph.
        """
        for node in nodes:
            self.add_node(node)
        return True

    def add_node_without_validation(self, node: Node) -> bool:
        """
        Add a node to the graph without validation.

        Args:
            - node (Node): Node to add

        Returns:
            - bool: True if node was added, False if node is invalid
        """
        if not isinstance(node, Node):
            return False

        self.nodes[node.id] = node
        return True

    def add_nodes_without_validation(self, nodes: List[Node]) -> bool:
        """
        Add a list of nodes to the graph without validation.

        Args:
            - nodes (List[Node]): List of nodes to add

        Returns:
            - bool: True if nodes were added successfully
        """
        if not isinstance(nodes, list):
            return False

        for node in nodes:
            self.add_node_without_validation(node)
        return True

    def get_node_by_id(self, id: str) -> Optional[Node]:
        """
        Get a node by ID.

        Args:
          - id (str): ID of the node to retrieve

        Returns:
          - Node: The node if found, None otherwise
        """
        return self.nodes.get(id)

    def get_nodes_by_kind(self, kind: str) -> List[Node]:
        """
        Get all nodes of a specific kind.

        Args:
          - kind (str): Kind/type to filter by

        Returns:
          - List[Node]: List of nodes with the specified kind
        """
        return [node for node in self.nodes.values() if node.has_kind(kind)]

    def get_node_count(self) -> int:
        """
        Get the total number of nodes in the graph.

        Returns:
          - int: Number of nodes
        """
        return len(self.nodes.keys())

    def get_isolated_nodes(self) -> List[Node]:
        """
        Get all nodes that have no edges.
                These are nodes that are not connected to any other nodes in the graph.

        Returns:
          - List[Node]: List of nodes with no edges
        """
        return [
            node
            for node in self.nodes.values()
            if not self.get_edges_from_node(node.id)
            and not self.get_edges_to_node(node.id)
        ]

    def get_isolated_nodes_count(self) -> int:
        """
        Get the total number of Isolated nodes in the graph.
        These are nodes that are not connected to any other nodes in the graph.

        Returns:
            - int: Number of Isolated nodes
        """
        return len(self.get_isolated_nodes())

    def remove_node_by_id(self, id: str) -> bool:
        """
        Remove a node and all its associated edges from the graph.

        Args:
          - id (str): ID of the node to remove

        Returns:
          - bool: True if node was removed, False if node doesn't exist
        """
        if id not in self.nodes:
            return False

        # Remove the node
        del self.nodes[id]

        # Remove all edges that reference this node
        self.edges = [
            edge for edge in self.edges if edge.start_node != id and edge.end_node != id
        ]

        return True

    # Paths methods

    def find_paths(
        self, start_id: str, end_id: str, max_depth: int = 10
    ) -> List[List[str]]:
        """
        Find all paths between two nodes using BFS.

        Args:
          - start_id (str): Starting node ID
          - end_id (str): Target node ID
          - max_depth (int): Maximum path length to search

        Returns:
          - List[List[str]]: List of paths, where each path is a list of node IDs
        """
        if start_id not in self.nodes or end_id not in self.nodes:
            return []

        if start_id == end_id:
            return [[start_id]]

        paths = []
        queue = [(start_id, [start_id])]

        while queue and len(queue[0][1]) <= max_depth:
            current_id, path = queue.pop(0)
            current_depth = len(path)

            # Only explore if we haven't reached max depth
            if current_depth >= max_depth:
                continue

            for edge in self.get_edges_from_node(current_id):
                next_id = edge.end_node
                # Check if next_id is not already in the current path (prevents cycles)
                if next_id not in path:
                    new_path = path + [next_id]
                    if next_id == end_id:
                        paths.append(new_path)
                    else:
                        queue.append((next_id, new_path))

        return paths

    def get_connected_components(self) -> List[Set[str]]:
        """
        Find all connected components in the graph.

        Returns:
          - List[Set[str]]: List of connected component sets
        """
        visited = set()
        components = []

        for node_id in self.nodes:
            if node_id not in visited:
                component = set()
                stack = [node_id]

                while stack:
                    current = stack.pop()
                    if current not in visited:
                        visited.add(current)
                        component.add(current)

                        # Add all adjacent nodes
                        for edge in self.get_edges_from_node(current):
                            if edge.end_node not in visited:
                                stack.append(edge.end_node)
                        for edge in self.get_edges_to_node(current):
                            if edge.start_node not in visited:
                                stack.append(edge.start_node)

                components.append(component)

        return components

    def validate_graph(self) -> tuple[bool, list[str]]:
        """
        Validate the graph for common issues including node and edge validation.

        Validates:
        - All nodes using their individual validate() methods
        - All edges using their individual validate() methods  
        - Graph structure issues (isolated nodes/edges)

        Returns:
          - tuple[bool, list[str]]: (is_valid, list_of_errors)
        """
        errors = []

        # Validate all nodes
        for node_id, node in self.nodes.items():
            is_node_valid, node_errors = node.validate()
            if not is_node_valid:
                for error in node_errors:
                    errors.append(f"Node '{node_id}': {error}")

        # Validate all edges
        for i, edge in enumerate(self.edges):
            is_edge_valid, edge_errors = edge.validate()
            if not is_edge_valid:
                for error in edge_errors:
                    errors.append(f"Edge {i} ({edge.start_node}->{edge.end_node}): {error}")

        # Check for graph structure issues
        # Pre-compute edge mappings for O(1) lookups
        start_node_edges = {}
        end_node_edges = {}

        # Build edge mappings and check for isolated edges
        for i, edge in enumerate(self.edges):
            # Check for isolated edges (edges referencing non-existent nodes)
            if edge.start_node not in self.nodes:
                errors.append(f"Edge {i} ({edge.start_node}->{edge.end_node}): Start node '{edge.start_node}' does not exist")
            else:
                # Build start node mapping
                if edge.start_node not in start_node_edges:
                    start_node_edges[edge.start_node] = []
                start_node_edges[edge.start_node].append(edge)

            if edge.end_node not in self.nodes:
                errors.append(f"Edge {i} ({edge.start_node}->{edge.end_node}): End node '{edge.end_node}' does not exist")
            else:
                # Build end node mapping
                if edge.end_node not in end_node_edges:
                    end_node_edges[edge.end_node] = []
                end_node_edges[edge.end_node].append(edge)

        # Check for isolated nodes using pre-computed mappings
        for node_id in self.nodes:
            # O(1) lookup instead of O(m) scan
            has_outgoing = node_id in start_node_edges
            has_incoming = node_id in end_node_edges

            if not has_outgoing and not has_incoming:
                errors.append(f"Node '{node_id}' is isolated (no incoming or outgoing edges)")

        return len(errors) == 0, errors

    # Export methods

    def export_json(
        self, include_metadata: bool = True, indent: None | int = None
    ) -> str:
        """
        Export the graph to JSON format compatible with BloodHound OpenGraph.

        Args:
          - include_metadata (bool): Whether to include metadata in the export

        Returns:
          - str: JSON string representation of the graph
        """
        graph_data = {
            "graph": {
                "nodes": [node.to_dict() for node in self.nodes.values()],
                "edges": [edge.to_dict() for edge in self.edges],
            }
        }

        if include_metadata and self.source_kind:
            graph_data["metadata"] = {"source_kind": self.source_kind}

        return json.dumps(graph_data, indent=indent)

    def export_to_file(
        self, filename: str, include_metadata: bool = True, indent: None | int = None
    ) -> bool:
        """
        Export the graph to a JSON file.

        Args:
          - filename (str): Name of the file to write
          - include_metadata (bool): Whether to include metadata in the export

        Returns:
          - bool: True if export was successful, False otherwise
        """
        try:
            json_data = self.export_json(include_metadata, indent)
            with open(filename, "w") as f:
                f.write(json_data)
            return True
        except (IOError, OSError, TypeError):
            return False

    def export_to_dict(self) -> Dict:
        """
        Export the graph to a dictionary.
        """

        return {
            "graph": {
                "nodes": [node.to_dict() for node in self.nodes.values()],
                "edges": [edge.to_dict() for edge in self.edges],
            },
            "metadata": {
                "source_kind": (self.source_kind if self.source_kind else None)
            },
        }

    # Import methods

    def import_from_json(self, json_data: str) -> bool:
        """
        Load graph data from a JSON string.
        """
        return self.import_from_dict(json.loads(json_data))

    def import_from_file(self, filename: str) -> bool:
        """
        Load graph data from a JSON file.

        Args:
          - filename (str): Name of the file to read

        Returns:
          - bool: True if load was successful, False otherwise
        """
        try:
            with open(filename, "r") as f:
                data = json.load(f)
            return self.import_from_dict(data)
        except (IOError, OSError, json.JSONDecodeError):
            return False

    def import_from_dict(self, data: Dict) -> bool:
        """
        Load graph data from a dictionary (typically from JSON).

        Args:
          - data (Dict): Dictionary containing graph data

        Returns:
          - bool: True if load was successful, False otherwise
        """
        try:
            if "graph" not in data:
                return False

            graph_data = data["graph"]

            # Load nodes
            if "nodes" in graph_data:
                for node_data in graph_data["nodes"]:
                    node = Node.from_dict(node_data)
                    if node:
                        self.nodes[node.id] = node

            # Load edges
            if "edges" in graph_data:
                for edge_data in graph_data["edges"]:
                    edge = Edge.from_dict(edge_data)
                    if edge:
                        self.edges.append(edge)

            # Load metadata
            if "metadata" in data and "source_kind" in data["metadata"]:
                self.source_kind = data["metadata"]["source_kind"]

            return True
        except (KeyError, TypeError, ValueError):
            return False

    # Other methods

    def clear(self) -> None:
        """
        Clear all nodes and edges from the graph.
        """
        self.nodes.clear()
        self.edges.clear()

    def __len__(self) -> int:
        """
        Return the total number of nodes and edges.

        Returns:
            - int: Total number of nodes and edges
        """
        return len(self.nodes) + len(self.edges)

    def __repr__(self) -> str:
        return f"OpenGraph(nodes={len(self.nodes)}, edges={len(self.edges)}, source_kind='{self.source_kind}')"
