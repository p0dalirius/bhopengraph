Quickstart
==========

This guide will help you get started with bhopengraph quickly. We'll create a simple graph with a few nodes and edges to demonstrate the basic functionality.

Basic Example
------------

Here's a minimal example that creates a simple graph with two nodes and one edge:

.. code-block:: python

   from bhopengraph.OpenGraph import OpenGraph
   from bhopengraph.Node import Node
   from bhopengraph.Edge import Edge
   from bhopengraph.Properties import Properties

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
       start_node_id=alice_node.id,
       end_node_id=bob_node.id,
       kind="Knows"
   )

   # Add edge to graph
   graph.addEdge(knows_edge)

   # Export to file
   graph.exportToFile("minimal_example.json")

This creates a JSON file that follows the BloodHound OpenGraph schema.

Key Concepts
-----------

**OpenGraph**: The main container that holds all nodes and edges.

**Node**: Represents an entity in your graph (like a person, computer, or group).

**Edge**: Represents a relationship between two nodes.

**Properties**: Contains metadata about nodes or edges.

Working with Nodes
-----------------

Nodes can have multiple types (kinds) and various properties:

.. code-block:: python

   # Create a computer node
   computer_node = Node(
       id="COMP001",
       kinds=["Computer", "Base"],
       properties=Properties(
           displayname="DESKTOP-COMP001",
           name="DESKTOP-COMP001",
           objectid="S-1-5-21-1234567890-1234567890-1234567890-1001",
           operatingsystem="Windows 10",
           primarygroup="DOMAIN COMPUTERS"
       )
   )

Working with Edges
-----------------

Edges define relationships between nodes:

.. code-block:: python

   # Create an "AdminTo" relationship
   admin_edge = Edge(
       start_node_id="USER001",
       end_node_id="COMP001",
       kind="AdminTo"
   )

   # Create a "MemberOf" relationship
   member_edge = Edge(
       start_node_id="USER001",
       end_node_id="ADMINS",
       kind="MemberOf"
   )

Exporting Your Graph
-------------------

You can export your graph in different formats:

.. code-block:: python

   # Export as JSON (default)
   graph.exportToFile("my_graph.json")

   # Export with custom formatting
   graph.exportToFile("my_graph.json", indent=2)

   # Get the JSON string directly
   json_string = graph.toJson()

Next Steps
----------

* Check out the :doc:`examples/index` for more complex examples
* Read the :doc:`api/index` for detailed API documentation
* Learn about :doc:`advanced_features` for more advanced usage

The examples in the :doc:`examples/index` section provide more detailed scenarios and use cases.
