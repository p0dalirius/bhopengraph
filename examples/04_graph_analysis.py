#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File name          : 04_graph_analysis.py
# Author             : Remi Gascou (@podalirius_)
# Date created       : 12 Aug 2025

"""
Graph Analysis Example

This example demonstrates:
- Graph validation
- Connected components analysis
- Node and edge statistics
- Graph integrity checks
"""

from bhopengraph.OpenGraph import OpenGraph
from bhopengraph.Node import Node
from bhopengraph.Edge import Edge
from bhopengraph.Properties import Properties

def main():
    """
    Demonstrate graph analysis and validation capabilities.
    """
    print("Graph Analysis Example")
    print("=" * 35)
    
    # Create a graph with some intentional issues to demonstrate validation
    graph = OpenGraph(source_kind="Analysis")
    
    # Create nodes
    nodes = {
        "user1": Node("user_001", ["User"], Properties(name="Alice", role="analyst")),
        "user2": Node("user_002", ["User"], Properties(name="Bob", role="developer")),
        "user3": Node("user_003", ["User"], Properties(name="Charlie", role="admin")),
        "group1": Node("group_001", ["Group"], Properties(name="Developers", type="security")),
        "group2": Node("group_002", ["Group"], Properties(name="Admins", type="security")),
        "server1": Node("server_001", ["Server"], Properties(name="Web Server", os="Linux")),
        "server2": Node("server_002", ["Server"], Properties(name="DB Server", os="Windows")),
        "isolated": Node("isolated_001", ["User"], Properties(name="Isolated User", role="guest")),
    }
    
    # Add nodes to graph
    for node in nodes.values():
        graph.addNode(node)
    
    # Create edges (some will create isolated components)
    edges = [
        # Connected component 1: Users and Groups
        Edge(nodes["user1"].id, nodes["group1"].id, "MemberOf"),
        Edge(nodes["user2"].id, nodes["group1"].id, "MemberOf"),
        Edge(nodes["user3"].id, nodes["group2"].id, "MemberOf"),
        
        # Connected component 2: Servers
        Edge(nodes["server1"].id, nodes["server2"].id, "ConnectedTo"),
        Edge(nodes["group1"].id, nodes["server1"].id, "CanAccess"),
        Edge(nodes["group2"].id, nodes["server2"].id, "AdminTo"),
        
        # Isolated node (no edges)
        # nodes["isolated"] has no edges
    ]
    
    # Add edges to graph
    for edge in edges:
        graph.addEdge(edge)
    
    print(f"Graph created with {graph.getNodeCount()} nodes and {graph.getEdgeCount()} edges")
    
    # Demonstrate graph analysis
    print(f"\n" + "="*50)
    print("GRAPH ANALYSIS")
    print("="*50)
    
    # 1. Basic statistics
    print(f"\n1. Basic Statistics:")
    print(f"   Total nodes: {graph.getNodeCount()}")
    print(f"   Total edges: {graph.getEdgeCount()}")
    print(f"   Graph size: {len(graph)}")
    
    # 2. Node type distribution
    print(f"\n2. Node Type Distribution:")
    for kind in ["User", "Group", "Server"]:
        nodes_of_kind = graph.getNodesByKind(kind)
        print(f"   {kind}: {len(nodes_of_kind)}")
        for node in nodes_of_kind:
            name = node.get_property('name', node.id)
            print(f"     - {name}")
    
    # 3. Edge type distribution
    print(f"\n3. Edge Type Distribution:")
    edge_types = {}
    for edge in graph.edges:
        edge_types[edge.kind] = edge_types.get(edge.kind, 0) + 1
    
    for edge_type, count in sorted(edge_types.items()):
        print(f"   {edge_type}: {count}")
    
    # 4. Connected components analysis
    print(f"\n4. Connected Components Analysis:")
    components = graph.getConnectedComponents()
    print(f"   Number of components: {len(components)}")
    
    for i, component in enumerate(components):
        print(f"   Component {i+1}: {len(component)} nodes")
        if len(component) <= 5:  # Show small components
            node_names = []
            for node_id in component:
                node = graph.getNode(node_id)
                if node:
                    node_names.append(node.get_property('name', node_id))
                else:
                    node_names.append(node_id)
            print(f"     Nodes: {', '.join(node_names)}")
    
    # 5. Node connectivity analysis
    print(f"\n5. Node Connectivity Analysis:")
    for node_id, node in graph.nodes.items():
        name = node.get_property('name', node_id)
        incoming_edges = len(graph.getEdgesToNode(node_id))
        outgoing_edges = len(graph.getEdgesFromNode(node_id))
        total_edges = incoming_edges + outgoing_edges
        
        print(f"   {name}:")
        print(f"     Incoming edges: {incoming_edges}")
        print(f"     Outgoing edges: {outgoing_edges}")
        print(f"     Total edges: {total_edges}")
        
        if total_edges == 0:
            print(f"     ⚠️  ISOLATED NODE")
    
    # 6. Graph validation
    print(f"\n6. Graph Validation:")
    errors = graph.validateGraph()
    
    if errors:
        total_issues = sum(len(error_list) for error_list in errors.values())
        print(f"   ⚠️  Found {total_issues} validation issues:")
        for error_type, error_list in errors.items():
            if error_type == "isolated_edges":
                print(f"     - {len(error_list)} orphaned edges:")
                for error in error_list:
                    print(f"       * Edge {error['edge_id']} references missing {error['issue']}: {error['node_id']}")
            elif error_type == "isolated_nodes":
                print(f"     - {len(error_list)} isolated nodes: {', '.join(error_list)}")
    else:
        print(f"   ✅ No validation issues found")
    
    # 7. Path analysis between components
    print(f"\n7. Path Analysis Between Components:")
    
    # Try to find paths between different components
    if len(components) > 1:
        print(f"   Testing connectivity between components...")
        
        # Get nodes from different components
        comp1_nodes = list(components[0])
        comp2_nodes = list(components[1])
        
        if comp1_nodes and comp2_nodes:
            start_node = comp1_nodes[0]
            end_node = comp2_nodes[0]
            
            start_name = graph.getNode(start_node).get_property('name', start_node)
            end_name = graph.getNode(end_node).get_property('name', end_node)
            
            print(f"   Testing path from {start_name} to {end_name}:")
            paths = graph.findPaths(start_node, end_node, max_depth=10)
            
            if paths:
                print(f"     Found {len(paths)} path(s)")
                for i, path in enumerate(paths[:2]):  # Show first 2 paths
                    path_names = []
                    for nid in path:
                        node = graph.getNode(nid)
                        if node:
                            path_names.append(node.get_property('name', nid))
                        else:
                            path_names.append(nid)
                    print(f"     Path {i+1}: {' -> '.join(path_names)}")
            else:
                print(f"     No path found (components are disconnected)")
    
    # 8. Graph density analysis
    print(f"\n8. Graph Density Analysis:")
    max_possible_edges = graph.getNodeCount() * (graph.getNodeCount() - 1)
    actual_edges = graph.getEdgeCount()
    density = actual_edges / max_possible_edges if max_possible_edges > 0 else 0
    
    print(f"   Maximum possible edges: {max_possible_edges}")
    print(f"   Actual edges: {actual_edges}")
    print(f"   Graph density: {density:.2%}")
    
    if density < 0.1:
        print(f"   📊 Sparse graph (low connectivity)")
    elif density < 0.5:
        print(f"   📊 Moderate density graph")
    else:
        print(f"   📊 Dense graph (high connectivity)")
    
    # Export to JSON
    graph.exportToFile("graph_analysis_example.json")
    print(f"\nGraph exported to 'graph_analysis_example.json'")
    
    # Summary
    print(f"\n" + "="*50)
    print("SUMMARY")
    print("="*50)
    print(f"✅ Graph analysis completed successfully")
    print(f"📊 Found {len(components)} connected components")
    print(f"🔍 Identified {len(errors)} validation issues")
    print(f"📈 Graph density: {density:.2%}")
    print(f"💾 Results exported to JSON file")

if __name__ == "__main__":
    main()
