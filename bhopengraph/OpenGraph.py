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

    def addEdgeWithoutValidation(self, edge: Edge) -> bool:
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

    def addEdgesWithoutValidation(self, edges: List[Edge]) -> bool:
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
            self.addEdgeWithoutValidation(edge)
        return True

    def addEdges(self, edges: List[Edge]) -> bool:
        """
        Add a list of edges to the graph.

        Returns:
            - bool: True if all edges were added successfully, False if any failed
        """
        success = True
        for edge in edges:
            if not self.addEdge(edge):
                success = False
        return success

    def addEdge(self, edge: Edge) -> bool:
        """
        Add an edge to the graph if it doesn't already exist and if the start and end nodes exist.

        Args:
          - edge (Edge): Edge to add

        Returns:
          - bool: True if edge was added, False if start or end node doesn't exist
        """
        if edge.start_node_id not in self.nodes:
            return False
        if edge.end_node_id not in self.nodes:
            return False

        for existing_edge in self.edges:
            if (
                existing_edge.start_node_id == edge.start_node_id
                and existing_edge.end_node_id == edge.end_node_id
                and existing_edge.kind == edge.kind
            ):
                return False

        self.edges.append(edge)
        return True

    def getEdgesByKind(self, kind: str) -> List[Edge]:
        """
        Get all edges of a specific kind.

        Args:
          - kind (str): Kind/type to filter by

        Returns:
          - List[Edge]: List of edges with the specified kind
        """
        return [edge for edge in self.edges if edge.kind == kind]

    def getEdgesFromNode(self, id: str) -> List[Edge]:
        """
        Get all edges starting from a specific node.

        Args:
          - id (str): ID of the source node

        Returns:
          - List[Edge]: List of edges starting from the specified node
        """
        return [edge for edge in self.edges if edge.start_node_id == id]

    def getEdgesToNode(self, id: str) -> List[Edge]:
        """
        Get all edges ending at a specific node.

        Args:
          - id (str): ID of the destination node

        Returns:
          - List[Edge]: List of edges ending at the specified node
        """
        return [edge for edge in self.edges if edge.end_node_id == id]

    def getIsolatedEdges(self) -> List[Edge]:
        """
        Get all edges that have no start or end node.
        These are edges that are not connected to any other nodes in the graph.

        Returns:
            - List[Edge]: List of edges with no start or end node
        """
        return [
            edge
            for edge in self.edges
            if edge.start_node_id not in self.nodes
            or edge.end_node_id not in self.nodes
        ]

    def getIsolatedEdgesCount(self) -> int:
        """
        Get the total number of Isolated edges in the graph.
        These are edges that are not connected to any other nodes in the graph.

        Returns:
            - int: Number of Isolated edges
        """
        return len(self.getIsolatedEdges())

    def getEdgeCount(self) -> int:
        """
        Get the total number of edges in the graph.

        Returns:
          - int: Number of edges
        """
        return len(self.edges)

    # Nodes methods

    def addNodeWithoutValidation(self, node: Node) -> bool:
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

    def addNodesWithoutValidation(self, nodes: List[Node]) -> bool:
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
            self.addNodeWithoutValidation(node)
        return True

    def addNodes(self, nodes: List[Node]) -> bool:
        """
        Add a list of nodes to the graph.
        """
        for node in nodes:
            self.addNode(node)
        return True

    def addNode(self, node: Node) -> bool:
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

    def removeNodes(self, nodes: List[Node]) -> bool:
        """
        Remove a list of nodes from the graph.

        Returns:
            - bool: True if all nodes were removed successfully, False if any failed
        """
        success = True
        for node in nodes:
            if not self.removeNode(node):
                success = False
        return success

    def removeNode(self, node: Node) -> bool:
        """
        Remove a node from the graph.
        """
        return self.removeNodeById(node.id)

    def removeNodeById(self, id: str) -> bool:
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
            edge
            for edge in self.edges
            if edge.start_node_id != id and edge.end_node_id != id
        ]

        return True

    def getNodeById(self, id: str) -> Optional[Node]:
        """
        Get a node by ID.

        Args:
          - id (str): ID of the node to retrieve

        Returns:
          - Node: The node if found, None otherwise
        """
        return self.nodes.get(id)

    def getNodesByKind(self, kind: str) -> List[Node]:
        """
        Get all nodes of a specific kind.

        Args:
          - kind (str): Kind/type to filter by

        Returns:
          - List[Node]: List of nodes with the specified kind
        """
        return [node for node in self.nodes.values() if node.has_kind(kind)]

    def getNodeCount(self) -> int:
        """
        Get the total number of nodes in the graph.

        Returns:
          - int: Number of nodes
        """
        return len(self.nodes)

    def getIsolatedNodes(self) -> List[Node]:
        """
        Get all nodes that have no edges.
                These are nodes that are not connected to any other nodes in the graph.

        Returns:
          - List[Node]: List of nodes with no edges
        """
        return [
            node
            for node in self.nodes.values()
            if not self.getEdgesFromNode(node.id) and not self.getEdgesToNode(node.id)
        ]

    def getIsolatedNodesCount(self) -> int:
        """
        Get the total number of Isolated nodes in the graph.
        These are nodes that are not connected to any other nodes in the graph.

        Returns:
            - int: Number of Isolated nodes
        """
        return len(self.getIsolatedNodes())

    # Paths methods

    def findPaths(
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

            for edge in self.getEdgesFromNode(current_id):
                next_id = edge.end_node_id
                # Check if next_id is not already in the current path (prevents cycles)
                if next_id not in path:
                    new_path = path + [next_id]
                    if next_id == end_id:
                        paths.append(new_path)
                    else:
                        queue.append((next_id, new_path))

        return paths

    def getConnectedComponents(self) -> List[Set[str]]:
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
                        for edge in self.getEdgesFromNode(current):
                            if edge.end_node_id not in visited:
                                stack.append(edge.end_node_id)
                        for edge in self.getEdgesToNode(current):
                            if edge.start_node_id not in visited:
                                stack.append(edge.start_node_id)

                components.append(component)

        return components

    def validateGraph(self) -> List[str]:
        """
        Validate the graph for common issues.

        Returns:
          - List[str]: List of validation error messages
        """
        errors = []

        # Check for Isolated edges
        for edge in self.edges:
            if edge.start_node_id not in self.nodes:
                errors.append(
                    f"Edge {edge.kind} references non-existent start node: {edge.start_node_id}"
                )
            if edge.end_node_id not in self.nodes:
                errors.append(
                    f"Edge {edge.kind} references non-existent end node: {edge.end_node_id}"
                )

        # Check for nodes without edges
        isolated_nodes = []
        for node_id in self.nodes:
            if not self.getEdgesFromNode(node_id) and not self.getEdgesToNode(node_id):
                isolated_nodes.append(node_id)

        if isolated_nodes:
            errors.append(
                f"Found {len(isolated_nodes)} isolated nodes: {isolated_nodes}"
            )

        return errors

    def exportJSON(self, include_metadata: bool = True) -> str:
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

        return json.dumps(graph_data, indent=2)

    def exportToFile(self, filename: str, include_metadata: bool = True) -> bool:
        """
        Export the graph to a JSON file.

        Args:
          - filename (str): Name of the file to write
          - include_metadata (bool): Whether to include metadata in the export

        Returns:
          - bool: True if export was successful, False otherwise
        """
        try:
            json_data = self.exportJSON(include_metadata)
            with open(filename, "w") as f:
                f.write(json_data)
            return True
        except (IOError, OSError, TypeError):
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
