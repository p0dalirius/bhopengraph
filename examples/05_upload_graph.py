#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File name          : 05_upload_graph.py

"""
Example script demonstrating how to build a graph and upload it to BloodHound.

Usage:
    python 05_upload_graph.py \
        --url https://your-bloodhound-instance.example.com \
        --token-id <TOKEN_ID> \
        --token-key '<TOKEN_KEY>'
"""

import argparse

from bhopengraph import BloodHoundClient, Edge, Node, OpenGraph, Properties


def build_example_graph() -> OpenGraph:
    """Build a small example graph with users, servers, and groups."""
    graph = OpenGraph(source_kind="Base")

    # Add users
    graph.add_node(
        Node(
            "user-001",
            kinds=["Person", "Base"],
            properties=Properties(
                displayname="alice",
                name="ALICE",
                objectid="user-001",
                email="alice@example.com",
                department="Engineering",
            ),
        )
    )
    graph.add_node(
        Node(
            "user-002",
            kinds=["Person", "Base"],
            properties=Properties(
                displayname="bob",
                name="BOB",
                objectid="user-002",
                email="bob@example.com",
                department="DevOps",
            ),
        )
    )

    # Add servers
    graph.add_node(
        Node(
            "server-001",
            kinds=["Server", "Base"],
            properties=Properties(
                displayname="web-server-01",
                name="WEB-SERVER-01",
                objectid="server-001",
                os="Ubuntu 22.04",
            ),
        )
    )
    graph.add_node(
        Node(
            "server-002",
            kinds=["Server", "Base"],
            properties=Properties(
                displayname="db-server-01",
                name="DB-SERVER-01",
                objectid="server-002",
                os="Ubuntu 22.04",
            ),
        )
    )

    # Add a group
    graph.add_node(
        Node(
            "group-001",
            kinds=["Group", "Base"],
            properties=Properties(
                displayname="Server Admins",
                name="SERVER-ADMINS",
                objectid="group-001",
            ),
        )
    )

    # Add relationships
    graph.add_edge(Edge("user-001", "group-001", "MemberOf"))
    graph.add_edge(Edge("user-002", "group-001", "MemberOf"))
    graph.add_edge(Edge("group-001", "server-001", "AdminTo"))
    graph.add_edge(Edge("group-001", "server-002", "AdminTo"))
    graph.add_edge(Edge("user-001", "server-001", "HasSession"))
    graph.add_edge(Edge("server-001", "server-002", "ConnectedTo"))

    return graph


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Build an example graph and upload it to BloodHound."
    )
    parser.add_argument("--url", required=True, help="BloodHound base URL")
    parser.add_argument("--token-id", required=True, help="API token ID")
    parser.add_argument("--token-key", required=True, help="API token key")
    args = parser.parse_args()

    graph = build_example_graph()
    print(
        f"Built graph: {graph.get_node_count()} nodes, {graph.get_edge_count()} edges"
    )

    client = BloodHoundClient(args.url, args.token_id, args.token_key)
    job_id = graph.upload(client)
    print(f"Upload complete, job ID: {job_id}")
