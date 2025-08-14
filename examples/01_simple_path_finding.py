#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File name          : 01_simple_path_finding.py
# Author             : Remi Gascou (@podalirius_)
# Date created       : 12 Aug 2025

"""
Simple Path Finding Example

This example demonstrates:
- Creating a small graph with nodes and edges
- Finding paths between two nodes
- Basic graph operations
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from bhopengraph.OpenGraph import OpenGraph
from bhopengraph.Node import Node
from bhopengraph.Edge import Edge
from bhopengraph.Properties import Properties

def main():
    """
    Create a simple graph and find paths between nodes.
    """
    print("Simple Path Finding Example")
    print("=" * 40)
    
    # Create a simple graph
    graph = OpenGraph(source_kind="Simple")
    
    # Create nodes
    alice = Node("alice_001", ["Person"], Properties(name="Alice", age=25))
    bob = Node("bob_002", ["Person"], Properties(name="Bob", age=30))
    charlie = Node("charlie_003", ["Person"], Properties(name="Charlie", age=35))
    diana = Node("diana_004", ["Person"], Properties(name="Diana", age=28))
    
    # Add nodes to graph
    graph.addNode(alice)
    graph.addNode(bob)
    graph.addNode(charlie)
    graph.addNode(diana)
    
    # Create edges (relationships)
    edges = [
        Edge(alice.id, bob.id, "Knows"),
        Edge(bob.id, charlie.id, "Knows"),
        Edge(charlie.id, diana.id, "Knows"),
        Edge(alice.id, diana.id, "Knows"),  # Direct connection
        Edge(bob.id, diana.id, "Knows"),    # Another path
    ]
    
    # Add edges to graph
    for edge in edges:
        graph.addEdge(edge)
    
    print(f"Graph created with {graph.getNodeCount()} nodes and {graph.getEdgeCount()} edges")
    
    # Find paths between Alice and Diana
    print(f"\nFinding paths from Alice to Diana:")
    paths = graph.findPaths(alice.id, diana.id, max_depth=5)
    
    if paths:
        print(f"Found {len(paths)} path(s):")
        for i, path in enumerate(paths):
            path_names = []
            for node_id in path:
                node = graph.getNode(node_id)
                path_names.append(node.get_property('name', node_id))
            print(f"  Path {i+1}: {' -> '.join(path_names)}")
    else:
        print("No path found")
    
    # Find paths between Bob and Diana
    print(f"\nFinding paths from Bob to Diana:")
    paths = graph.findPaths(bob.id, diana.id, max_depth=5)
    
    if paths:
        print(f"Found {len(paths)} path(s):")
        for i, path in enumerate(paths):
            path_names = []
            for node_id in path:
                node = graph.getNode(node_id)
                path_names.append(node.get_property('name', node_id))
            print(f"  Path {i+1}: {' -> '.join(path_names)}")
    else:
        print("No path found")
    
    # Show all edges
    print(f"\nAll edges in the graph:")
    for edge in graph.edges:
        start_node = graph.getNode(edge.start_node_id)
        end_node = graph.getNode(edge.end_node_id)
        start_name = start_node.get_property('name', edge.start_node_id)
        end_name = end_node.get_property('name', edge.end_node_id)
        print(f"  {start_name} --[{edge.kind}]--> {end_name}")
    
    # Export to JSON
    graph.exportToFile("simple_path_finding.json")
    print(f"\nGraph exported to 'simple_path_finding.json'")

if __name__ == "__main__":
    main()
