#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File name          : minimalworkingjson_example.py
# Author             : Remi Gascou (@podalirius_)
# Date created       : 12 Aug 2025

"""
Example script demonstrating how to use the OpenGraph classes
to recreate the minimal working JSON from BloodHound documentation.
"""

from bhopengraph.OpenGraph import OpenGraph
from bhopengraph.Node import Node
from bhopengraph.Edge import Edge
from bhopengraph.Properties import Properties

if __name__ == "__main__":
    """
    Create the minimal working example from BloodHound OpenGraph documentation.
    https://bloodhound.specterops.io/opengraph/schema#minimal-working-json
    """
    # Create an OpenGraph instance
    graph = OpenGraph(source_kind="Base")
    
    # Create nodes
    bob_node = Node(
        id="123",
        kinds=["Person", "Base"],
        properties=Properties(
            displayname="bob",
            property="a",
            objectid="123",
            name="BOB"
        )
    )
    
    alice_node = Node(
        id="234",
        kinds=["Person", "Base"],
        properties=Properties(
            displayname="alice",
            property="b",
            objectid="234",
            name="ALICE"
        )
    )
    
    # Add nodes to graph
    graph.addNode(bob_node)
    graph.addNode(alice_node)
    
    # Create edge: Bob knows Alice
    knows_edge = Edge(
        start_node_id=bob_node.id,      # Bob is the start
        end_node_id=alice_node.id,      # Alice is the end
        kind="Knows"
    )
    
    
    # Add edge to graph
    graph.addEdge(knows_edge)
    
    # Export to file
    graph.exportToFile("minimal_working_json.json")
