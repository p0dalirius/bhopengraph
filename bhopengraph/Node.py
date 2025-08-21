#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File name          : Node.py
# Author             : Remi Gascou (@podalirius_)
# Date created       : 12 Aug 2025

from bhopengraph.Properties import Properties


class Node(object):
    """
    Node class representing a node in the OpenGraph.

    Follows BloodHound OpenGraph schema requirements with unique IDs, kinds, and properties.

    Sources:
    - https://bloodhound.specterops.io/opengraph/schema#nodes
    - https://bloodhound.specterops.io/opengraph/schema#minimal-working-json
    """

    def __init__(self, id: str, kinds: list = None, properties: Properties = None):
        """
        Initialize a Node.

        Args:
          - id (str): Universally unique identifier for the node
          - kinds (list): List of node types/classes
          - properties (Properties): Node properties
        """
        if not id:
            raise ValueError("Node ID cannot be empty")

        self.id = id
        self.kinds = kinds or []
        self.properties = properties or Properties()

    def add_kind(self, kind: str):
        """
        Add a kind/type to the node.

        Args:
          - kind (str): Kind/type to add
        """
        if kind not in self.kinds:
            self.kinds.append(kind)

    def remove_kind(self, kind: str):
        """
        Remove a kind/type from the node.

        Args:
          - kind (str): Kind/type to remove
        """
        if kind in self.kinds:
            self.kinds.remove(kind)

    def has_kind(self, kind: str) -> bool:
        """
        Check if node has a specific kind/type.

        Args:
          - kind (str): Kind/type to check

        Returns:
          - bool: True if node has the kind, False otherwise
        """
        return kind in self.kinds

    def set_property(self, key: str, value):
        """
        Set a property on the node.

        Args:
          - key (str): Property name
          - value: Property value
        """
        self.properties[key] = value

    def get_property(self, key: str, default=None):
        """
        Get a property from the node.

        Args:
          - key (str): Property name
          - default: Default value if property doesn't exist

        Returns:
          - Property value or default
        """
        return self.properties.get_property(key, default)

    def remove_property(self, key: str):
        """
        Remove a property from the node.

        Args:
          - key (str): Property name to remove
        """
        self.properties.remove_property(key)

    def to_dict(self) -> dict:
        """
        Convert node to dictionary for JSON serialization.

        Returns:
          - dict: Node as dictionary following BloodHound OpenGraph schema
        """
        node_dict = {
            "id": self.id,
            "kinds": self.kinds.copy(),
            "properties": self.properties.to_dict(),
        }
        return node_dict

    def __eq__(self, other):
        """Check if two nodes are equal based on their ID."""
        if isinstance(other, Node):
            return self.id == other.id
        return False

    def __hash__(self):
        """Hash based on node ID for use in sets and as dictionary keys."""
        return hash(self.id)

    def __repr__(self) -> str:
        return f"Node(id='{self.id}', kinds={self.kinds}, properties={self.properties})"
