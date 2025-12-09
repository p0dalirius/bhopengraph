#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File name          : 03_edge_operations.py
# Author             : Remi Gascou (@podalirius_)
# Date created       : 12 Aug 2025

"""
Edge Operations Example

This example demonstrates:
- Creating different types of edges
- Adding edge properties
- Finding edges by type
- Edge traversal operations
"""

from bhopengraph.OpenGraph import OpenGraph
from bhopengraph.Node import Node
from bhopengraph.Edge import Edge
from bhopengraph.Properties import Properties

def main():
    """
    Demonstrate edge operations and different edge types.
    """
    print("Edge Operations Example")
    print("=" * 35)
    
    # Create a graph
    graph = OpenGraph(source_kind="Network")
    
    # Create nodes
    nodes = {
        "router": Node("router_001", ["Device", "Router"], Properties(name="Core Router", ip="10.0.0.1")),
        "switch1": Node("switch_001", ["Device", "Switch"], Properties(name="Access Switch 1", ip="10.0.1.1")),
        "switch2": Node("switch_002", ["Device", "Switch"], Properties(name="Access Switch 2", ip="10.0.2.1")),
        "server1": Node("server_001", ["Device", "Server"], Properties(name="Web Server", ip="10.0.1.10")),
        "server2": Node("server_002", ["Device", "Server"], Properties(name="Database Server", ip="10.0.2.10")),
        "workstation1": Node("ws_001", ["Device", "Workstation"], Properties(name="User PC 1", ip="10.0.1.100")),
        "workstation2": Node("ws_002", ["Device", "Workstation"], Properties(name="User PC 2", ip="10.0.2.100")),
    }
    
    # Add nodes to graph
    for node in nodes.values():
        graph.add_node(node)
    
    # Create edges with different types and properties
    edges = [
        # Network connections
        Edge(nodes["router"].id, nodes["switch1"].id, "ConnectedTo", 
             Properties(bandwidth="1Gbps", cable_type="fiber")),
        Edge(nodes["router"].id, nodes["switch2"].id, "ConnectedTo", 
             Properties(bandwidth="1Gbps", cable_type="fiber")),
        Edge(nodes["switch1"].id, nodes["server1"].id, "ConnectedTo", 
             Properties(bandwidth="100Mbps", cable_type="copper")),
        Edge(nodes["switch1"].id, nodes["workstation1"].id, "ConnectedTo", 
             Properties(bandwidth="100Mbps", cable_type="copper")),
        Edge(nodes["switch2"].id, nodes["server2"].id, "ConnectedTo", 
             Properties(bandwidth="100Mbps", cable_type="copper")),
        Edge(nodes["switch2"].id, nodes["workstation2"].id, "ConnectedTo", 
             Properties(bandwidth="100Mbps", cable_type="copper")),
        
        # Administrative access
        Edge(nodes["router"].id, nodes["switch1"].id, "Manages", 
             Properties(access_level="admin", protocol="SSH")),
        Edge(nodes["router"].id, nodes["switch2"].id, "Manages", 
             Properties(access_level="admin", protocol="SSH")),
        
        # Service dependencies
        Edge(nodes["server1"].id, nodes["server2"].id, "DependsOn", 
             Properties(service="database", criticality="high")),
        Edge(nodes["workstation1"].id, nodes["server1"].id, "Accesses", 
             Properties(service="web", protocol="HTTP")),
        Edge(nodes["workstation2"].id, nodes["server1"].id, "Accesses", 
             Properties(service="web", protocol="HTTP")),
    ]
    
    # Add edges to graph
    for edge in edges:
        graph.add_edge(edge)
    
    print(f"Graph created with {graph.get_node_count()} nodes and {graph.get_edge_count()} edges")
    
    # Demonstrate edge operations
    print(f"\nEdge Operations:")
    
    # Show edges by type
    for edge_type in ["ConnectedTo", "Manages", "DependsOn", "Accesses"]:
        edges_of_type = graph.get_edges_by_kind(edge_type)
        print(f"  {edge_type} edges: {len(edges_of_type)}")
        for edge in edges_of_type:
            start_node = graph.get_node_by_id(edge.start_node)
            end_node = graph.get_node_by_id(edge.end_node)
            start_name = start_node.get_property('name', edge.start_node)
            end_name = end_node.get_property('name', edge.end_node)
            print(f"    {start_name} -> {end_name}")
    
    # Show edges from specific nodes
    print(f"\nEdges from Router:")
    router_edges = graph.get_edges_from_node(nodes["router"].id)
    for edge in router_edges:
        end_node = graph.get_node_by_id(edge.end_node)
        end_name = end_node.get_property('name', edge.end_node)
        print(f"  Router --[{edge.kind}]--> {end_name}")
    
    # Show edges to specific nodes
    print(f"\nEdges to Web Server:")
    server1_edges = graph.get_edges_to_node(nodes["server1"].id)
    for edge in server1_edges:
        start_node = graph.get_node_by_id(edge.start_node)
        start_name = start_node.get_property('name', edge.start_node)
        print(f"  {start_name} --[{edge.kind}]--> Web Server")
    
    # Demonstrate edge properties
    print(f"\nEdge Properties:")
    for edge in graph.edges[:3]:  # Show first 3 edges
        start_node = graph.get_node_by_id(edge.start_node)
        end_node = graph.get_node_by_id(edge.end_node)
        start_name = start_node.get_property('name', edge.start_node)
        end_name = end_node.get_property('name', edge.end_node)
        
        print(f"  {start_name} --[{edge.kind}]--> {end_name}")
        if edge.properties:
            for key, value in edge.properties.get_all_properties().items():
                print(f"    {key}: {value}")
    
    # Find paths between workstations and database server
    print(f"\nPath Finding:")
    
    # Path from Workstation 1 to Database Server
    paths = graph.find_paths(nodes["workstation1"].id, nodes["server2"].id, max_depth=5)
    if paths:
        print(f"  Paths from Workstation 1 to Database Server:")
        for i, path in enumerate(paths):
            path_names = []
            for node_id in path:
                node = graph.get_node_by_id(node_id)
                path_names.append(node.get_property('name', node_id))
            print(f"    Path {i+1}: {' -> '.join(path_names)}")
    else:
        print(f"  No path found from Workstation 1 to Database Server")
    
    # Path from Workstation 2 to Database Server
    paths = graph.find_paths(nodes["workstation2"].id, nodes["server2"].id, max_depth=5)
    if paths:
        print(f"  Paths from Workstation 2 to Database Server:")
        for i, path in enumerate(paths):
            path_names = []
            for node_id in path:
                node = graph.get_node_by_id(node_id)
                path_names.append(node.get_property('name', node_id))
            print(f"    Path {i+1}: {' -> '.join(path_names)}")
    else:
        print(f"  No path found from Workstation 2 to Database Server")
    
    # Show network topology
    print(f"\nNetwork Topology:")
    for node_id, node in graph.nodes.items():
        name = node.get_property('name', node_id)
        print(f"  {name}:")
        
        # Show outgoing connections
        outgoing = graph.get_edges_from_node(node_id)
        for edge in outgoing:
            end_node = graph.get_node_by_id(edge.end_node)
            end_name = end_node.get_property('name', edge.end_node)
            print(f"    -> {end_name} ({edge.kind})")
    
    # Export to JSON
    graph.export_to_file("edge_operations_example.json")
    print(f"\nGraph exported to 'edge_operations_example.json'")

if __name__ == "__main__":
    main()
