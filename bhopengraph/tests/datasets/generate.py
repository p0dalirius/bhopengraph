#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File name          : generate.py
# Author             : Remi Gascou (@podalirius_)
# Date created       : 22 Aug 2025

import os
import random
import string
import time
import uuid

from bhopengraph import OpenGraph
from bhopengraph.Edge import Edge
from bhopengraph.Node import Node
from bhopengraph.Properties import Properties


def generate_random_name():
    """
    Generate a random name.
    """
    return "".join(random.choices(string.ascii_letters + string.digits, k=10))


def generate_opengraph_dataset(
    number_of_nodes,
    number_of_edges,
    number_of_node_kinds=10,
    number_of_edge_kinds=10,
    percentage_of_isolated_nodes=0.0,
    percentage_of_isolated_edges=0.0,
):
    """
    Generate a dataset of OpenGraph objects.
    """

    if percentage_of_isolated_nodes > 100.0 or percentage_of_isolated_nodes < 0.0:
        raise ValueError("percentage_of_isolated_nodes must be between 0.0 and 100.0")

    if percentage_of_isolated_edges > 100.0 or percentage_of_isolated_edges < 0.0:
        raise ValueError("percentage_of_isolated_edges must be between 0.0 and 100.0")

    # Create a new OpenGraph instance
    graph = OpenGraph()
    graph.source_kind = f"n{number_of_nodes}_e{number_of_edges}_pin{percentage_of_isolated_nodes}_pie{percentage_of_isolated_edges}"

    # Calculate the number of isolated nodes and edges
    isolated_nodes_count = int(number_of_nodes * (percentage_of_isolated_nodes / 100.0))
    connected_nodes_count = number_of_nodes - isolated_nodes_count

    isolated_edges_count = int(number_of_edges * (percentage_of_isolated_edges / 100.0))
    connected_edges_count = number_of_edges - isolated_edges_count

    # Generate node types and kinds for variety
    node_kinds = [generate_random_name() for _ in range(number_of_node_kinds)]
    edge_kinds = [generate_random_name() for _ in range(number_of_edge_kinds)]

    # Generate all nodes first
    all_nodes = []

    # Generate connected nodes
    for i in range(connected_nodes_count):
        node_id = str(uuid.uuid4())
        node_kind = random.choice(node_kinds)
        node = Node(id=node_id, kinds=[node_kind], properties=Properties())
        all_nodes.append(node)
        graph.add_node(node)

    # Generate isolated nodes
    for i in range(isolated_nodes_count):
        node_id = str(uuid.uuid4())
        node_kind = random.choice(node_kinds)
        node = Node(id=node_id, kinds=[node_kind], properties=Properties())
        all_nodes.append(node)
        graph.add_node(node)

    # Generate connected edges (edges that reference existing nodes)
    for i in range(connected_edges_count):
        if len(all_nodes) >= 2:
            source_node = random.choice(all_nodes)
            target_node = random.choice(all_nodes)

            # Avoid self-loops
            while source_node.id == target_node.id and len(all_nodes) > 1:
                target_node = random.choice(all_nodes)

            edge_kind = random.choice(edge_kinds)
            edge = Edge(
                start_node=source_node.id,
                start_match_by="id",
                end_node=target_node.id,
                end_match_by="id",
                kind=edge_kind,
                properties=Properties(),
            )
            graph.add_edge(edge)

    # Generate isolated edges (edges that reference non-existent nodes)
    for i in range(isolated_edges_count):
        # Create fake node IDs that don't exist in the graph
        match random.randint(1, 3):
            case 1:
                source_id = str(uuid.uuid4())
                target_id = str(uuid.uuid4())
            case 2:
                source_id = random.choice(all_nodes).id
                target_id = str(uuid.uuid4())
            case 3:
                source_id = str(uuid.uuid4())
                target_id = random.choice(all_nodes).id

        edge_kind = random.choice(edge_kinds)
        edge = Edge(
            start_node=source_id,
            start_match_by="id",
            end_node=target_id,
            end_match_by="id",
            kind=edge_kind,
            properties=Properties(),
        )
        graph.add_edge(edge)

    graph.export_to_file(
        os.path.join(os.path.dirname(__file__), f"dataset_{graph.source_kind}.json")
    )

    return graph


def benchmark_validate_graph(graph, number_of_iterations=10):
    """
    Benchmark the validate_graph method.
    """
    total_time = 0
    for i in range(number_of_iterations):
        start_time = time.perf_counter()
        graph.validate_graph()
        end_time = time.perf_counter()
        total_time += (end_time - start_time) * 1000

    return round(total_time / number_of_iterations, 2)


if __name__ == "__main__":

    for testcase in [
        (10000, 10000, 0.0, 0.0),
        (10000, 10000, 0.0, 100.0),
        (10000, 10000, 25.0, 75.0),
        (10000, 10000, 50.0, 50.0),
        (10000, 10000, 75.0, 25.0),
        (10000, 10000, 100.0, 0.0),
        (10000, 10000, 100.0, 100.0),
        (100000, 100000, 0.0, 0.0),
        (100000, 100000, 0.0, 100.0),
        (100000, 100000, 25.0, 75.0),
        (100000, 100000, 50.0, 50.0),
        (100000, 100000, 75.0, 25.0),
        (100000, 100000, 100.0, 0.0),
        (100000, 100000, 100.0, 100.0),
    ]:
        graph = generate_opengraph_dataset(
            number_of_nodes=testcase[0],
            number_of_edges=testcase[1],
            number_of_node_kinds=10,
            number_of_edge_kinds=10,
            percentage_of_isolated_nodes=testcase[2],
            percentage_of_isolated_edges=testcase[3],
        )
        print(
            "Testcase: %-45s | Validation time: %s ms"
            % (testcase, benchmark_validate_graph(graph))
        )
