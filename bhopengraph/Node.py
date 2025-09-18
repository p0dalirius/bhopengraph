#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File name          : Node.py
# Author             : Remi Gascou (@podalirius_)
# Date created       : 12 Aug 2025

from bhopengraph.Properties import Properties


# https://bloodhound.specterops.io/opengraph/schema#node-json

NODE_SCHEMA = {
    "title": "Generic Ingest Node",
    "description": "A node used in a generic graph ingestion system. Each node must have a unique identifier (`id`) and at least one kind describing its role or type. Nodes may also include a `properties` object containing custom attributes.",
    "type": "object",
    "properties": {
        "id": { "type": "string" },
        "properties": {
            "type": ["object", "null"],
            "description": "A key-value map of node attributes. Values must not be objects. If a value is an array, it must contain only primitive types (e.g., strings, numbers, booleans) and must be homogeneous (all items must be of the same type).",
            "additionalProperties": {
                "type": ["string", "number", "boolean", "array"],
                "items": {
                    "not": {
                        "type": "object"
                    }
                }
            }
        },
        "kinds": {
            "type": ["array"],
            "items": { "type": "string" },
            "maxItems": 3,
            "minItems": 1,
            "description": "An array of kind labels for the node. The first element is treated as the node's primary kind and is used to determine which icon to display in the graph UI. This primary kind is only used for visual representation and has no semantic significance for data processing."
        }
    },
    "required": ["id", "kinds"],
    "examples": [
        {
            "id": "user-1234",
            "kinds": ["Person"]
        },
        {
            "id": "device-5678",
            "properties": {
                "manufacturer": "Brandon Corp",
                "model": "4000x",
                "isActive": True,
                "rating": 43.50
            },
            "kinds": ["Device", "Asset"]
        },
        {
            "id": "location-001",
            "properties": None,
            "kinds": ["Location"]
        }
    ]
}


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

        if len(self.kinds) >= 3:
            raise ValueError("Node can only have a maximum of 3 kinds")

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

    @classmethod
    def from_dict(cls, node_data: dict):
        """
        Create a Node instance from a dictionary.

        Args:
            - node_data (dict): Dictionary containing node data

        Returns:
            - Node: Node instance or None if data is invalid
        """
        try:
            if "id" not in node_data:
                return None

            node_id = node_data["id"]
            kinds = node_data.get("kinds", [])
            properties_data = node_data.get("properties", {})

            # Create Properties instance if properties data exists
            properties = None
            if properties_data:
                properties = Properties()
                for key, value in properties_data.items():
                    properties[key] = value

            return cls(node_id, kinds, properties)
        except (KeyError, TypeError, ValueError):
            return None

    def __eq__(self, other):
        """
        Check if two nodes are equal based on their ID.

        Args:
          - other (Node): The other node to compare to

        Returns:
          - bool: True if the nodes are equal, False otherwise
        """
        if isinstance(other, Node):
            return self.id == other.id
        return False

    def __hash__(self):
        """
        Hash based on node ID for use in sets and as dictionary keys.

        Returns:
          - int: Hash of the node ID
        """
        return hash(self.id)

    def validate(self) -> tuple[bool, list[str]]:
        """
        Validate the node against the NODE_SCHEMA.
        
        Returns:
            - tuple[bool, list[str]]: (is_valid, list_of_errors)
        """
        errors = []
        
        # Validate required fields
        if not self.id or self.id is None:
            errors.append("Node ID cannot be empty")
        elif not isinstance(self.id, str):
            errors.append("Node ID must be a string")
        
        # Validate kinds
        if not isinstance(self.kinds, list):
            errors.append("Kinds must be a list")
        elif len(self.kinds) < 1:
            errors.append("Node must have at least one kind")
        elif len(self.kinds) > 3:
            errors.append("Node can have at most 3 kinds")
        else:
            for i, kind in enumerate(self.kinds):
                if not isinstance(kind, str):
                    errors.append(f"Kind at index {i} must be a string")
        
        # Validate properties if they exist
        if self.properties is not None:
            if not isinstance(self.properties, Properties):
                errors.append("Properties must be a Properties instance")
            else:
                is_props_valid, prop_errors = self.properties.validate()
                if not is_props_valid:
                    errors.extend(prop_errors)
        
        return len(errors) == 0, errors

    def __repr__(self) -> str:
        return f"Node(id='{self.id}', kinds={self.kinds}, properties={self.properties})"
