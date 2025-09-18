#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File name          : __main__.py
# Author             : Remi Gascou (@podalirius_)
# Date created       : 21 Aug 2025

import argparse
import json
import os

from bhopengraph import OpenGraph
from bhopengraph.Logger import Logger
from bhopengraph.utils import filesize_string

"""
Main module for BloodHound OpenGraph.

This module provides the main entry point for the BloodHound OpenGraph package.
"""


def parseArgs():
    parser = argparse.ArgumentParser(description="")

    parser.add_argument(
        "--debug", dest="debug", action="store_true", default=False, help="Debug mode."
    )

    # Creating the "info" subparser ==============================================================================================================
    mode_info = argparse.ArgumentParser(add_help=False)
    mode_info.add_argument(
        "--file",
        dest="file",
        required=True,
        default=None,
        help="OpenGraph JSON file to process",
    )
    mode_info.add_argument(
        "--json",
        dest="json",
        action="store_true",
        default=False,
        help="Output info in JSON format",
    )

    # Creating the "validate" subparser ==============================================================================================================
    mode_validate = argparse.ArgumentParser(add_help=False)
    mode_validate.add_argument(
        "--file",
        dest="file",
        required=True,
        default=None,
        help="OpenGraph JSON file to process",
    )
    mode_validate.add_argument(
        "--json",
        dest="json",
        action="store_true",
        default=False,
        help="Output validation errors in JSON format",
    )

    # Mode paths
    mode_showpaths = argparse.ArgumentParser(add_help=False)
    mode_showpaths.add_argument(
        "--file",
        dest="file",
        required=True,
        default=None,
        help="OpenGraph JSON file to process",
    )
    mode_showpaths.add_argument(
        "--start-node-kind",
        dest="start_node_kind",
        required=True,
        default=None,
        help="Start node kind, This will be used to find the start node in the graph. This is required to find the start node in the graph",
    )
    mode_showpaths.add_argument(
        "--start-node-id",
        dest="start_node_id",
        required=True,
        default=None,
        help="Start node ID, This will be used to find the start node in the graph. This is required to find the start node in the graph",
    )
    mode_showpaths.add_argument(
        "--end-node-id",
        dest="end_node_id",
        required=True,
        default=None,
        help="End node ID, This will be used to find the end node in the graph. This is required to find the end node in the graph",
    )
    mode_showpaths.add_argument(
        "--max-depth",
        dest="max_depth",
        type=int,
        default=10,
        help="Maximum path depth to search (default: 10)",
    )

    # Adding the subparsers to the base parser
    subparsers = parser.add_subparsers(help="Mode", dest="mode", required=True)
    subparsers.add_parser("info", parents=[mode_info], help="Info mode")
    subparsers.add_parser("validate", parents=[mode_validate], help="Validate mode")
    subparsers.add_parser("showpaths", parents=[mode_showpaths], help="Show paths mode")
    
    return parser.parse_args()


def main():
    options = parseArgs()

    logger = Logger(options.debug)

    if options.mode == "info":
        if os.path.exists(options.file):
            logger.log(
                f"[+] Loading OpenGraph data from {options.file} (size %s)"
                % filesize_string(os.path.getsize(options.file))
            )
            graph = OpenGraph()
            graph.import_from_file(options.file)
            logger.log("  └── OpenGraph successfully loaded")

            # Get the graph information
            logger.log("[+] Computing OpenGraph information")
            logger.log("  ├── Computing node count (total and isolated) ...")
            nodeCount = graph.get_node_count()
            isolatedNodesCount = graph.get_isolated_nodes_count()
            connectedNodesCount = nodeCount - isolatedNodesCount
            logger.log("  └── Computing edge count (total and isolated) ...")
            edgeCount = graph.get_edge_count()
            isolatedEdgesCount = graph.get_isolated_edges_count()
            connectedEdgesCount = edgeCount - isolatedEdgesCount

            # Print the OpenGraph information
            logger.log("[+] OpenGraph information:")
            logger.log("  ├── Metadata:")
            logger.log(f"  │   └── Source kind: {graph.source_kind}")
            logger.log(f"  ├── Total nodes: {nodeCount}")
            logger.log(
                f"  │   ├── Connected nodes : \x1b[96m{connectedNodesCount}\x1b[0m (\x1b[92m{connectedNodesCount / nodeCount * 100:.2f}%\x1b[0m)"
            )
            logger.log(
                f"  │   └── Isolated nodes  : \x1b[96m{isolatedNodesCount}\x1b[0m (\x1b[91m{isolatedNodesCount / nodeCount * 100:.2f}%\x1b[0m)"
            )
            logger.log(f"  ├── Total edges: {edgeCount}")
            logger.log(
                f"  │   ├── Connected edges : \x1b[96m{connectedEdgesCount}\x1b[0m (\x1b[92m{connectedEdgesCount / edgeCount * 100:.2f}%\x1b[0m)"
            )
            logger.log(
                f"  │   └── Isolated edges  : \x1b[96m{isolatedEdgesCount}\x1b[0m (\x1b[91m{isolatedEdgesCount / edgeCount * 100:.2f}%\x1b[0m)"
            )
            logger.log("  └──")

            logger.log("[+] OpenGraph validation ...")
            is_valid, validation_errors = graph.validate_graph()
            if not is_valid:
                total_errors = len(validation_errors)
                logger.log(f"  ├── ❌ Validation errors: ({total_errors})")

                k = 0
                for error in validation_errors:
                    k += 1
                    if k == len(validation_errors):
                        logger.log(f"  │   └── {error}")
                    else:
                        logger.log(f"  │   ├── {error}")
                logger.log("  └──")
            else:
                logger.log("  │   └── ✅ No validation errors")
            logger.log("  └──")

        else:
            logger.error(f"File {options.file} does not exist")
            return

    elif options.mode == "validate":
        if os.path.exists(options.file):
            logger.debug(
                f"[+] Loading OpenGraph data from {options.file} (size %s)"
                % filesize_string(os.path.getsize(options.file))
            )
            graph = OpenGraph()
            graph.import_from_file(options.file)
            logger.debug("  └── OpenGraph successfully loaded")

            # Validate the graph
            logger.log("[+] OpenGraph validation ...")
            is_valid, validation_errors = graph.validate_graph()

            if options.json:
                result = {
                    "valid": is_valid,
                    "errors": validation_errors
                }
                print(json.dumps(result, indent=4))
            else:
                if not is_valid:
                    total_errors = len(validation_errors)
                    logger.log(f"  └── ❌ Validation errors: ({total_errors})")

                    k = 0
                    for error in validation_errors:
                        k += 1
                        if k == len(validation_errors):
                            logger.log(f"  │   └── {error}")
                        else:
                            logger.log(f"  │   ├── {error}")
                    logger.log("  └──")
                else:
                    logger.log("  │   └── ✅ No validation errors")
                    logger.log("  └──")

        else:
            if options.json:
                print(
                    json.dumps(
                        {"error": f"File {options.file} does not exist"}, indent=4
                    )
                )
            else:
                logger.error(f"File {options.file} does not exist")
            return

    elif options.mode == "showpaths":
        if os.path.exists(options.file):
            logger.debug(
                f"[+] Loading OpenGraph data from {options.file} (size %s)"
                % filesize_string(os.path.getsize(options.file))
            )
            graph = OpenGraph()
            graph.import_from_file(options.file)
            logger.debug("  └── OpenGraph successfully loaded")

            # Find paths
            logger.debug("[+] Finding paths ...")
            paths = graph.find_paths(options.start_node_id, options.end_node_id, options.max_depth)

            if options.json:
                print(json.dumps(paths, indent=4))
            else:
                logger.debug(f"  └── Paths: {paths}")


if __name__ == "__main__":
    main()
