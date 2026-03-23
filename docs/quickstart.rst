Quickstart
==========

This guide will help you get started with bhopengraph quickly. We'll create a simple graph with a few nodes and edges to demonstrate the basic functionality.

Basic Example
------------

Here's a minimal example that creates a simple graph with two nodes and one edge:

.. code-block:: python

   from bhopengraph import OpenGraph, Node, Edge, Properties

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
   graph.add_node(bob_node)
   graph.add_node(alice_node)

   # Create edge: Bob knows Alice
   knows_edge = Edge(
       start_node=alice_node.id,
       end_node=bob_node.id,
       kind="Knows"
   )

   # Add edge to graph
   graph.add_edge(knows_edge)

   # Export to file
   graph.export_to_file("minimal_example.json")

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
       start_node="USER001",
       end_node="COMP001",
       kind="AdminTo"
   )

   # Create a "MemberOf" relationship
   member_edge = Edge(
       start_node="USER001",
       end_node="ADMINS",
       kind="MemberOf"
   )

Exporting Your Graph
-------------------

You can export your graph in different formats:

.. code-block:: python

   # Export as JSON file
   graph.export_to_file("my_graph.json")

   # Export with custom formatting
   graph.export_to_file("my_graph.json", indent=2)

   # Get the JSON string directly
   json_string = graph.export_json()

   # Get as a Python dictionary
   graph_dict = graph.export_to_dict()

Uploading to BloodHound
-----------------------

bhopengraph can upload graphs directly to a BloodHound instance using the
`file-upload ingest API <https://bloodhound.specterops.io/opengraph/api>`_.
Authentication uses HMAC-signed requests with a token ID and token key pair
generated in the BloodHound UI.

**Upload a graph built in Python:**

.. code-block:: python

   from bhopengraph import OpenGraph, BloodHoundClient, Node, Edge, Properties

   # Build a graph
   graph = OpenGraph(source_kind="Base")
   graph.add_node(Node("user-001", kinds=["Person", "Base"],
       properties=Properties(displayname="alice", name="ALICE", objectid="user-001")))
   graph.add_node(Node("server-001", kinds=["Server", "Base"],
       properties=Properties(displayname="web-server", name="WEB-SERVER", objectid="server-001")))
   graph.add_edge(Edge("user-001", "server-001", "HasSession"))

   # Create an authenticated client
   client = BloodHoundClient(
       base_url="https://your-bloodhound-instance.example.com",
       token_id="<TOKEN_ID>",
       token_key="<TOKEN_KEY>"
   )

   # Upload the graph
   job_id = graph.upload(client)
   print(f"Upload complete, job ID: {job_id}")

**Upload a JSON file from disk:**

.. code-block:: python

   from bhopengraph import BloodHoundClient

   client = BloodHoundClient(
       base_url="https://your-bloodhound-instance.example.com",
       token_id="<TOKEN_ID>",
       token_key="<TOKEN_KEY>"
   )

   job_id = client.upload_graph_from_file("my_graph.json")

**Upload from the command line:**

.. code-block:: bash

   python -m bhopengraph upload-graph \
     --url https://your-bloodhound-instance.example.com \
     --token-id <TOKEN_ID> \
     --token-key '<TOKEN_KEY>' \
     --file my_graph.json

Running Cypher Queries
----------------------

You can execute Cypher queries directly against a BloodHound instance and get
raw JSON results:

.. code-block:: python

   from bhopengraph import BloodHoundClient

   client = BloodHoundClient(
       base_url="https://your-bloodhound-instance.example.com",
       token_id="<TOKEN_ID>",
       token_key="<TOKEN_KEY>"
   )

   # Run a Cypher query and get raw JSON results
   result = client.cypher_query("MATCH (n:User) RETURN n LIMIT 10")
   print(result)

   # Query relationships
   result = client.cypher_query(
       "MATCH (u:User)-[r:AdminTo]->(c:Computer) RETURN u, r, c"
   )

   # Exclude properties for lighter responses
   result = client.cypher_query("MATCH (n) RETURN n LIMIT 5", include_properties=False)

Managing Schema Extensions
--------------------------

The ``BloodHoundClient`` can also manage schema extensions and source kinds:

.. code-block:: python

   # List extensions
   extensions = client.list_extensions()

   # Create or update an extension
   client.upsert_schema_extension({
       "schema": {
           "name": "my-extension",
           "display_name": "My Extension",
           "version": "1.0.0",
           "namespace": "my-ext"
       },
       "node_kinds": [...],
       "relationship_kinds": [...],
       "environments": [...],
       "relationship_findings": [...]
   })

   # Delete an extension
   client.delete_extension(extension_id=1)

   # List and clear source kinds
   source_kinds = client.list_source_kinds()
   client.delete_source_kind_data(source_kind_ids=[3])

Next Steps
----------

* Check out the :doc:`examples/index` for more complex examples
* Read the :doc:`api/index` for detailed API documentation

The examples in the :doc:`examples/index` section provide more detailed scenarios and use cases.
