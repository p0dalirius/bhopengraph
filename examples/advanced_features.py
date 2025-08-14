#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File name          : example_advanced_features.py
# Author             : Remi Gascou (@podalirius_)
# Date created       : 12 Aug 2025

"""
Advanced example demonstrating BloodHound OpenGraph best practices
and attack path modeling capabilities.

This example shows how to create a realistic attack graph that follows
BloodHound's requirements for path finding between non-adjacent nodes.
"""

from bhopengraph.OpenGraph import OpenGraph
from bhopengraph.Node import Node
from bhopengraph.Edge import Edge
from bhopengraph.Properties import Properties

def create_attack_graph_example():
    """
    Create an attack graph example following BloodHound best practices.
    
    This demonstrates:
    - Proper edge directionality for attack paths
    - Multi-hop privilege escalation
    - Realistic Active Directory-like relationships
    """
    graph = OpenGraph(source_kind="ADBase")
    
    # Create nodes representing different entity types
    nodes = {
        # Users
        "john_doe": Node("S-1-5-21-1234567890-1234567890-1234567890-1001", 
                        ["User", "ADBase"], 
                        Properties(name="John Doe", samaccountname="jdoe", 
                                 displayname="John Doe", enabled=True)),
        
        "jane_smith": Node("S-1-5-21-1234567890-1234567890-1234567890-1002", 
                          ["User", "ADBase"], 
                          Properties(name="Jane Smith", samaccountname="jsmith", 
                                   displayname="Jane Smith", enabled=True)),
        
        "admin_user": Node("S-1-5-21-1234567890-1234567890-1234567890-1003", 
                          ["User", "ADBase"], 
                          Properties(name="Admin User", samaccountname="admin", 
                                   displayname="Administrator", enabled=True)),
        
        # Groups
        "domain_users": Node("S-1-5-21-1234567890-1234567890-1234567890-513", 
                            ["Group", "ADBase"], 
                            Properties(name="Domain Users", samaccountname="Domain Users", 
                                     description="All domain users")),
        
        "helpdesk_group": Node("S-1-5-21-1234567890-1234567890-1234567890-1101", 
                              ["Group", "ADBase"], 
                              Properties(name="HelpDesk", samaccountname="HelpDesk", 
                                       description="Help desk technicians")),
        
        "admin_group": Node("S-1-5-21-1234567890-1234567890-1234567890-512", 
                           ["Group", "ADBase"], 
                           Properties(name="Domain Admins", samaccountname="Domain Admins", 
                                    description="Domain administrators")),
        
        # Computers
        "workstation1": Node("S-1-5-21-1234567890-1234567890-1234567890-2001", 
                            ["Computer", "ADBase"], 
                            Properties(name="WORKSTATION-01", samaccountname="WORKSTATION-01$", 
                                     operatingsystem="Windows 10 Pro")),
        
        "workstation2": Node("S-1-5-21-1234567890-1234567890-1234567890-2002", 
                            ["Computer", "ADBase"], 
                            Properties(name="WORKSTATION-02", samaccountname="WORKSTATION-02$", 
                                     operatingsystem="Windows 10 Pro")),
        
        "server1": Node("S-1-5-21-1234567890-1234567890-1234567890-3001", 
                       ["Computer", "ADBase"], 
                       Properties(name="SERVER-01", samaccountname="SERVER-01$", 
                                operatingsystem="Windows Server 2019")),
        
        # Domain
        "domain": Node("S-1-5-21-1234567890-1234567890-1234567890", 
                      ["Domain", "ADBase"], 
                      Properties(name="CONTOSO.LOCAL", samaccountname="CONTOSO", 
                               description="Contoso Corporation Domain"))
    }
    
    # Add all nodes to the graph
    for node in nodes.values():
        graph.addNode(node)
    
    # Create edges following BloodHound best practices
    # Edge direction represents the direction of access/attack
    
    edges = [
        # User memberships (User -> Group)
        Edge(nodes["john_doe"].id, nodes["domain_users"].id, "MemberOf"),
        Edge(nodes["jane_smith"].id, nodes["domain_users"].id, "MemberOf"),
        Edge(nodes["admin_user"].id, nodes["domain_users"].id, "MemberOf"),
        Edge(nodes["jane_smith"].id, nodes["helpdesk_group"].id, "MemberOf"),
        Edge(nodes["admin_user"].id, nodes["admin_group"].id, "MemberOf"),
        
        # Group memberships (Group -> Group)
        Edge(nodes["helpdesk_group"].id, nodes["domain_users"].id, "MemberOf"),
        
        # Computer access (User -> Computer)
        Edge(nodes["john_doe"].id, nodes["workstation1"].id, "CanLogon"),
        Edge(nodes["jane_smith"].id, nodes["workstation2"].id, "CanLogon"),
        Edge(nodes["admin_user"].id, nodes["workstation1"].id, "CanLogon"),
        Edge(nodes["admin_user"].id, nodes["workstation2"].id, "CanLogon"),
        Edge(nodes["admin_user"].id, nodes["server1"].id, "CanLogon"),
        
        # Admin access (User/Group -> Computer)
        Edge(nodes["admin_user"].id, nodes["workstation1"].id, "AdminTo"),
        Edge(nodes["admin_user"].id, nodes["workstation2"].id, "AdminTo"),
        Edge(nodes["admin_user"].id, nodes["server1"].id, "AdminTo"),
        Edge(nodes["helpdesk_group"].id, nodes["workstation1"].id, "AdminTo"),
        Edge(nodes["helpdesk_group"].id, nodes["workstation2"].id, "AdminTo"),
        
        # Domain relationships
        Edge(nodes["admin_group"].id, nodes["domain"].id, "GenericAll"),
        Edge(nodes["helpdesk_group"].id, nodes["domain"].id, "GenericRead"),
        
        # Computer relationships
        Edge(nodes["workstation1"].id, nodes["domain"].id, "MemberOf"),
        Edge(nodes["workstation2"].id, nodes["domain"].id, "MemberOf"),
        Edge(nodes["server1"].id, nodes["domain"].id, "MemberOf")
    ]
    
    # Add all edges to the graph
    for edge in edges:
        graph.addEdge(edge)
    
    return graph

def demonstrate_attack_paths(graph):
    """
    Demonstrate various attack paths in the graph.
    """
    print("\n" + "="*60)
    print("ATTACK PATH ANALYSIS")
    print("="*60)
    
    # Example 1: Can John Doe become a domain admin?
    print("\n1. Attack Path: John Doe -> Domain Admin")
    john_doe_id = None
    admin_group_id = None
    
    # Find the actual IDs
    for node_id, node in graph.nodes.items():
        if node.get_property('name') == 'John Doe':
            john_doe_id = node_id
        elif node.get_property('name') == 'Domain Admins':
            admin_group_id = node_id
    
    if john_doe_id and admin_group_id:
        paths = graph.findPaths(john_doe_id, admin_group_id, max_depth=5)
        if paths:
            print(f"   Found {len(paths)} possible paths:")
            for i, path in enumerate(paths[:3]):  # Show first 3 paths
                path_names = []
                for nid in path:
                    node = graph.getNode(nid)
                    if node:
                        path_names.append(node.get_property('name', nid))
                    else:
                        path_names.append(nid)
                print(f"   Path {i+1}: {' -> '.join(path_names)}")
        else:
            print("   No direct path found (Good security posture!)")
    else:
        print("   Could not find required nodes")
    
    # Example 2: Can Jane Smith access Server-01?
    print("\n2. Attack Path: Jane Smith -> Server-01")
    jane_smith_id = None
    server1_id = None
    
    # Find the actual IDs
    for node_id, node in graph.nodes.items():
        if node.get_property('name') == 'Jane Smith':
            jane_smith_id = node_id
        elif node.get_property('name') == 'SERVER-01':
            server1_id = node_id
    
    if jane_smith_id and server1_id:
        paths = graph.findPaths(jane_smith_id, server1_id, max_depth=5)
        if paths:
            print(f"   Found {len(paths)} possible paths:")
            for i, path in enumerate(paths[:3]):
                path_names = []
                for nid in path:
                    node = graph.getNode(nid)
                    if node:
                        path_names.append(node.get_property('name', nid))
                    else:
                        path_names.append(nid)
                print(f"   Path {i+1}: {' -> '.join(path_names)}")
        else:
            print("   No direct path found (Good access control!)")
    else:
        print("   Could not find required nodes")
    
    # Example 3: What can John Doe access through group memberships?
    print("\n3. John Doe's Group Memberships:")
    if john_doe_id:
        john_edges = graph.getEdgesFromNode(john_doe_id)
        for edge in john_edges:
            if edge.kind == "MemberOf":
                target_node = graph.getNode(edge.end_node_id)
                if target_node:
                    print(f"   - Member of: {target_node.get_property('name', edge.end_node_id)}")
                else:
                    print(f"   - Member of: {edge.end_node_id}")
    
    # Example 4: Who has admin access to Workstation-01?
    print("\n4. Admin Access to Workstation-01:")
    workstation1_id = None
    for node_id, node in graph.nodes.items():
        if node.get_property('name') == 'WORKSTATION-01':
            workstation1_id = node_id
            break
    
    if workstation1_id:
        workstation1_edges = graph.getEdgesToNode(workstation1_id)
        for edge in workstation1_edges:
            if edge.kind == "AdminTo":
                source_node = graph.getNode(edge.start_node_id)
                if source_node:
                    print(f"   - {source_node.get_property('name', edge.start_node_id)} (User)")
                else:
                    print(f"   - {edge.start_node_id} (User)")
    
    # Example 5: Find all paths from regular users to domain admin
    print("\n5. All Paths from Regular Users to Domain Admin:")
    regular_users = []
    for node_id, node in graph.nodes.items():
        if node.has_kind("User") and node.get_property('name') in ['John Doe', 'Jane Smith']:
            regular_users.append(node_id)
    
    for user_id in regular_users:
        user_node = graph.getNode(user_id)
        if user_node and admin_group_id:
            paths = graph.findPaths(user_id, admin_group_id, max_depth=6)
            if paths:
                user_name = user_node.get_property('name', user_id)
                print(f"   {user_name}: {len(paths)} paths found")
            else:
                user_name = user_node.get_property('name', user_id)
                print(f"   {user_name}: No path found (Secure!)")

def demonstrate_graph_analysis(graph):
    """
    Demonstrate graph analysis capabilities.
    """
    print("\n" + "="*60)
    print("GRAPH ANALYSIS")
    print("="*60)
    
    # Connected components
    components = graph.getConnectedComponents()
    print(f"\nConnected Components: {len(components)}")
    for i, component in enumerate(components):
        print(f"  Component {i+1}: {len(component)} nodes")
        if len(component) <= 5:  # Show small components
            node_names = [graph.getNode(nid).get_property('name', nid) for nid in component]
            print(f"    Nodes: {', '.join(node_names)}")
    
    # Node type distribution
    print(f"\nNode Type Distribution:")
    for kind in ["User", "Group", "Computer", "Domain"]:
        nodes = graph.getNodesByKind(kind)
        print(f"  {kind}: {len(nodes)}")
    
    # Edge type distribution
    print(f"\nEdge Type Distribution:")
    edge_types = {}
    for edge in graph.edges:
        edge_types[edge.kind] = edge_types.get(edge.kind, 0) + 1
    
    for edge_type, count in sorted(edge_types.items()):
        print(f"  {edge_type}: {count}")
    
    # Graph validation
    print(f"\nGraph Validation:")
    errors = graph.validateGraph()
    if errors:
        print("  Issues found:")
        for error in errors:
            print(f"    - {error}")
    else:
        print("  No validation issues found")

def main():
    """
    Main function demonstrating advanced OpenGraph features.
    """
    print("BloodHound OpenGraph Advanced Features Example")
    print("=" * 60)
    
    # Create the attack graph
    print("\nCreating attack graph example...")
    graph = create_attack_graph_example()
    
    print(f"Graph created successfully!")
    print(f"  Nodes: {graph.getNodeCount()}")
    print(f"  Edges: {graph.getEdgeCount()}")
    
    # Demonstrate attack paths
    demonstrate_attack_paths(graph)
    
    # Demonstrate graph analysis
    demonstrate_graph_analysis(graph)
    
    # Export the graph
    print(f"\n" + "="*60)
    print("EXPORTING GRAPH")
    print("="*60)
    
    graph.exportToFile("attack_graph_example.json")
    print("Graph exported to 'attack_graph_example.json'")
    
    # Show a sample of the JSON output
    print("\nSample JSON output (first 500 chars):")
    json_output = graph.exportJSON()
    print(json_output[:500] + "..." if len(json_output) > 500 else json_output)

if __name__ == "__main__":
    main()
