#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File name          : __main__.py
# Author             : Remi Gascou (@podalirius_)
# Date created       : 21 Aug 2025

from bhopengraph import OpenGraph
import argparse
import json
import os
from bhopengraph.utils import b_filesize
from bhopengraph.Logger import Logger

"""
Main module for BloodHound OpenGraph.

This module provides the main entry point for the BloodHound OpenGraph package.
"""

def parseArgs():
    parser = argparse.ArgumentParser(description="")

    parser.add_argument("--debug", dest="debug", action="store_true", default=False, help="Debug mode.")

    # Creating the "battle" subparser ==============================================================================================================
    mode_info = argparse.ArgumentParser(add_help=False)
    mode_info.add_argument("--file", dest="file", required=True, default=None, help="OpenGraph JSON file to process")

    # Adding the subparsers to the base parser
    subparsers = parser.add_subparsers(help="Mode", dest="mode", required=True)
    mode_info_parser = subparsers.add_parser("info", parents=[mode_info], help="Info mode")

    return parser.parse_args()


def main():
    options = parseArgs()

    logger = Logger(options.debug)

    if options.mode == "info":
        if os.path.exists(options.file):
            with open(options.file, "r") as f:
                logger.log(f"[+] Loading graph from {options.file} (size %s)" % b_filesize(os.path.getsize(options.file)))
                graph = OpenGraph()
                graph.importFromFile(options.file)
                logger.log(f"  └── Graph successfully loaded")

                # Get the graph information
                logger.log(f"[+] Getting graph information")
                logger.log(f"  ├── Getting node count")
                nodeCount = graph.getNodeCount()
                isolatedNodesCount = graph.getIsolatedNodesCount()
                connectedNodesCount = nodeCount - isolatedNodesCount
                logger.log(f"  └── Getting edge count")
                edgeCount = graph.getEdgeCount()
                isolatedEdgesCount = graph.getIsolatedEdgesCount()
                connectedEdgesCount = edgeCount - isolatedEdgesCount

                # Print the graph information
                logger.log(f"[+] Graph information:")
                logger.log(f"  ├── Metadata:")
                logger.log(f"  │   └── Source kind: {graph.source_kind}")
                logger.log(f"  ├── Total nodes: {nodeCount}")
                logger.log(f"  │   ├── Connected nodes: {connectedNodesCount}")
                logger.log(f"  │   └── Isolated nodes: {isolatedNodesCount}")
                logger.log(f"  ├── Total edges: {edgeCount}")
                logger.log(f"  │   ├── Connected edges: {connectedEdgesCount}")
                logger.log(f"  │   └── Isolated edges: {isolatedEdgesCount}")
                logger.log(f"  └──")

                logger.log(f"[+] Graph validation:")
                validationErrors = graph.validateGraph()
                if len(validationErrors) > 0:
                    logger.log(f"  ├── ❌ Validation errors: ({len(validationErrors)})")
                    k = 0
                    for error in validationErrors:
                        k += 1
                        if k == len(validationErrors):
                            logger.log(f"  │   └── {error}")
                        else:
                            logger.log(f"  │   ├── {error}")
                else:
                    logger.log(f"  │   └── ✅ No validation errors")
                logger.log(f"  └──")

        else:
            logger.error(f"[!] File {options.file} does not exist")
            return


if __name__ == "__main__":
    main()