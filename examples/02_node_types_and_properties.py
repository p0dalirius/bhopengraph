#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File name          : 02_node_types_and_properties.py
# Author             : Remi Gascou (@podalirius_)
# Date created       : 12 Aug 2025

"""
Node Types and Properties Example

This example demonstrates:
- Creating different types of nodes
- Using various property types
- Adding and removing node properties
- Working with node kinds
"""

from bhopengraph.OpenGraph import OpenGraph
from bhopengraph.Node import Node
from bhopengraph.Properties import Properties

def main():
    """
    Demonstrate different node types and properties.
    """
    print("Node Types and Properties Example")
    print("=" * 45)
    
    # Create a graph
    graph = OpenGraph(source_kind="Demo")
    
    # Create different types of nodes with various properties
    
    # Person node
    person = Node(
        "person_001", 
        ["Person", "Employee"], 
        Properties(
            name="John Smith",
            age=32,
            department="Engineering",
            salary=75000.0,
            is_active=True,
            skills="Python,JavaScript,Docker"
        )
    )
    
    # Computer node
    computer = Node(
        "computer_001",
        ["Computer", "Workstation"],
        Properties(
            hostname="WS-JSMITH-01",
            os="Windows 11",
            ip_address="192.168.1.100",
            memory_gb=16,
            is_encrypted=True,
            last_patch="2024-01-15"
        )
    )
    
    # Application node
    application = Node(
        "app_001",
        ["Application", "WebApp"],
        Properties(
            name="Customer Portal",
            version="2.1.0",
            port=8080,
            is_production=True,
            dependencies="PostgreSQL,Redis",  # Changed from list to string
            last_deploy="2024-01-20"
        )
    )
    
    # Database node
    database = Node(
        "db_001",
        ["Database", "PostgreSQL"],
        Properties(
            name="CustomerDB",
            version="14.5",
            size_gb=25.5,
            is_clustered=False,
            backup_frequency="daily",
            retention_days=30
        )
    )
    
    # Add nodes to graph
    graph.addNode(person)
    graph.addNode(computer)
    graph.addNode(application)
    graph.addNode(database)
    
    print(f"Graph created with {graph.getNodeCount()} nodes")
    
    # Demonstrate node operations
    print(f"\nNode Operations:")
    
    # Show all nodes by type
    for kind in ["Person", "Computer", "Application", "Database"]:
        nodes = graph.getNodesByKind(kind)
        print(f"  {kind} nodes: {len(nodes)}")
        for node in nodes:
            name = node.get_property('name', node.id)
            print(f"    - {name}")
    
    # Demonstrate property operations
    print(f"\nProperty Operations:")
    
    # Get a specific node
    john = graph.getNode("person_001")
    if john:
        print(f"  John's current properties:")
        for key, value in john.properties.get_all_properties().items():
            print(f"    {key}: {value}")
        
        # Add a new property
        john.set_property("location", "New York")
        print(f"  Added location property: {john.get_property('location')}")
        
        # Update an existing property
        john.set_property("age", 33)
        print(f"  Updated age: {john.get_property('age')}")
        
        # Remove a property
        john.remove_property("skills")
        print(f"  Removed skills property")
        
        # Check if property exists
        print(f"  Has location: {john.properties.has_property('location')}")
        print(f"  Has skills: {john.properties.has_property('skills')}")
    
    # Demonstrate kind operations
    print(f"\nKind Operations:")
    
    # Add a new kind
    john.add_kind("Manager")
    print(f"  Added 'Manager' kind to John")
    
    # Check kinds
    print(f"  John's kinds: {john.kinds}")
    print(f"  Is John a Manager? {john.has_kind('Manager')}")
    print(f"  Is John a Director? {john.has_kind('Director')}")
    
    # Remove a kind
    john.remove_kind("Employee")
    print(f"  Removed 'Employee' kind from John")
    print(f"  John's kinds after removal: {john.kinds}")
    
    # Show final node state
    print(f"\nFinal Node States:")
    for node_id, node in graph.nodes.items():
        name = node.get_property('name', node_id)
        kinds = ', '.join(node.kinds)
        print(f"  {name}: {kinds}")
    
    # Export to JSON
    graph.exportToFile("node_types_example.json")
    print(f"\nGraph exported to 'node_types_example.json'")

if __name__ == "__main__":
    main()
