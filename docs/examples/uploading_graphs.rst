Uploading Graphs
================

This example demonstrates how to build a graph and upload it to a BloodHound instance.

Building and Uploading a Graph
------------------------------

.. code-block:: python

   from bhopengraph import OpenGraph, BloodHoundClient, Node, Edge, Properties

   # Build a graph
   graph = OpenGraph(source_kind="Base")

   # Add users
   graph.add_node(Node("user-001", kinds=["Person", "Base"],
       properties=Properties(displayname="alice", name="ALICE", objectid="user-001")))
   graph.add_node(Node("user-002", kinds=["Person", "Base"],
       properties=Properties(displayname="bob", name="BOB", objectid="user-002")))

   # Add a server
   graph.add_node(Node("server-001", kinds=["Server", "Base"],
       properties=Properties(displayname="web-server-01", name="WEB-SERVER-01", objectid="server-001")))

   # Add a group
   graph.add_node(Node("group-001", kinds=["Group", "Base"],
       properties=Properties(displayname="Server Admins", name="SERVER-ADMINS", objectid="group-001")))

   # Add relationships
   graph.add_edge(Edge("user-001", "group-001", "MemberOf"))
   graph.add_edge(Edge("user-002", "group-001", "MemberOf"))
   graph.add_edge(Edge("group-001", "server-001", "AdminTo"))
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

Uploading a JSON File
---------------------

You can also upload a pre-existing JSON file. An example file is provided at
``examples/example_upload.json``.

.. code-block:: python

   from bhopengraph import BloodHoundClient

   client = BloodHoundClient(
       base_url="https://your-bloodhound-instance.example.com",
       token_id="<TOKEN_ID>",
       token_key="<TOKEN_KEY>"
   )

   job_id = client.upload_graph_from_file("examples/example_upload.json")
   print(f"Upload complete, job ID: {job_id}")

Upload Protocol
---------------

The upload uses BloodHound's three-step file-upload ingest API:

1. ``POST /api/v2/file-upload/start`` — creates an upload job and returns a job ID
2. ``POST /api/v2/file-upload/{id}`` — sends the JSON payload with an ``X-File-Upload-Name`` header
3. ``POST /api/v2/file-upload/{id}/end`` — finalises the job

The ``/end`` call is always made, even if the upload step fails, to ensure the
server-side job is properly cleaned up.
