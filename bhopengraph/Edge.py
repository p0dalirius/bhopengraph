#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File name          : Edge.py
# Author             : Remi Gascou (@podalirius_)
# Date created       : 12 Aug 2025

from bhopengraph.Properties import Properties

# https://bloodhound.specterops.io/opengraph/schema#edge-json
EDGE_SCHEMA = {
    "title": "Generic Ingest Edge",
    "description": "Defines an edge between two nodes in a generic graph ingestion system. Each edge specifies a start and end node using either a unique identifier (id) or a name-based lookup. A kind is required to indicate the relationship type. Optional properties may include custom attributes. You may optionally constrain the start or end node to a specific kind using the kind field inside each reference.",
    "type": "object",
    "properties": {
        "start": {
            "type": "object",
            "properties": {
                "match_by": {
                    "type": "string",
                    "enum": ["id", "name"],
                    "default": "id",
                    "description": "Whether to match the start node by its unique object ID or by its name property."
                },
                "value": {
                    "type": "string",
                    "description": "The value used for matching — either an object ID or a name, depending on match_by."
                },
                "kind": {
                    "type": "string",
                    "description": "Optional kind filter; the referenced node must have this kind."
                }
            },
            "required": ["value"]
        },
        "end": {
            "type": "object",
            "properties": {
                "match_by": {
                    "type": "string",
                    "enum": ["id", "name"],
                    "default": "id",
                    "description": "Whether to match the end node by its unique object ID or by its name property."
                },
                "value": {
                    "type": "string",
                    "description": "The value used for matching — either an object ID or a name, depending on match_by."
                },
                "kind": {
                    "type": "string",
                    "description": "Optional kind filter; the referenced node must have this kind."
                }
            },
            "required": ["value"]
        },
        "kind": { "type": "string" },
        "properties": {
            "type": ["object", "null"],
            "description": "A key-value map of edge attributes. Values must not be objects. If a value is an array, it must contain only primitive types (e.g., strings, numbers, booleans) and must be homogeneous (all items must be of the same type).",
            "additionalProperties": {
                "type": ["string", "number", "boolean", "array"],
                "items": {
                    "not": {
                        "type": "object"
                    }
                }
            }
        }
    },
    "required": ["start", "end", "kind"],
    "examples": [
        {
            "start": {
                "match_by": "id",
                "value": "user-1234"
            },
            "end": {
                "match_by": "id",
                "value": "server-5678"
            },
            "kind": "HasSession",
            "properties": {
                "timestamp": "2025-04-16T12:00:00Z",
                "duration_minutes": 45
            }
        },
        {
            "start": {
                "match_by": "name",
                "value": "alice",
                "kind": "User"
            },
            "end": {
                "match_by": "name",
                "value": "file-server-1",
                "kind": "Server"
            },
            "kind": "AccessedResource",
            "properties": {
                "via": "SMB",
                "sensitive": True
            }
        },
        {
            "start": {
                "value": "admin-1"
            },
            "end": {
                "value": "domain-controller-9"
            },
            "kind": "AdminTo",
            "properties": {
                "reason": "elevated_permissions",
                "confirmed": False
            }
        },
        {
            "start": {
                "match_by": "name",
                "value": "Printer-007"
            },
            "end": {
                "match_by": "id",
                "value": "network-42"
            },
            "kind": "ConnectedTo",
            "properties": None
        }
    ]
}



class Edge(object):
    """
    Edge class representing a directed edge in the OpenGraph.

    Follows BloodHound OpenGraph schema requirements with start/end nodes, kind, and properties.
    All edges are directed and one-way as per BloodHound requirements.

    Sources:
    - https://bloodhound.specterops.io/opengraph/schema#edges
    - https://bloodhound.specterops.io/opengraph/schema#minimal-working-json
    """

    def __init__(
        self,
        start_node: str,
        end_node: str,
        kind: str,
        properties: Properties = None,
        start_match_by: str = "id",
        end_match_by: str = "id",
    ):
        """
        Initialize an Edge.

        Args:
          - start_node (str): ID of the source node
          - end_node (str): ID of the destination node
          - kind (str): Type/class of the edge relationship
          - properties (Properties): Edge properties
        """
        if not start_node:
            raise ValueError("Start node ID cannot be empty")
        if not end_node:
            raise ValueError("End node ID cannot be empty")
        if not kind:
            raise ValueError("Edge kind cannot be empty")

        self.start_node = start_node
        self.end_node = end_node
        self.kind = kind
        self.properties = properties or Properties()

        self.start_match_by = start_match_by
        self.end_match_by = end_match_by

    def set_property(self, key: str, value):
        """
        Set a property on the edge.

        Args:
          - key (str): Property name
          - value: Property value
        """
        self.properties[key] = value

    def get_property(self, key: str, default=None):
        """
        Get a property from the edge.

        Args:
          - key (str): Property name
          - default: Default value if property doesn't exist

        Returns:
          - Property value or default
        """
        return self.properties.get_property(key, default)

    def remove_property(self, key: str):
        """
        Remove a property from the edge.

        Args:
          - key (str): Property name to remove
        """
        self.properties.remove_property(key)

    def to_dict(self) -> dict:
        """
        Convert edge to dictionary for JSON serialization.

        Returns:
          - dict: Edge as dictionary following BloodHound OpenGraph schema
        """
        edge_dict = {
            "kind": self.kind,
            "start": {"value": self.start_node, "match_by": self.start_match_by},
            "end": {"value": self.end_node, "match_by": self.end_match_by},
        }

        # Only include properties if they exist and are not empty
        if self.properties and len(self.properties) > 0:
            edge_dict["properties"] = self.properties.to_dict()

        return edge_dict

    @classmethod
    def from_dict(cls, edge_data: dict):
        """
        Create an Edge instance from a dictionary.

        Args:
            - edge_data (dict): Dictionary containing edge data

        Returns:
            - Edge: Edge instance or None if data is invalid
        """
        try:
            if "kind" not in edge_data:
                return None

            kind = edge_data["kind"]

            # Handle different edge data formats
            start_node = None
            end_node = None
            start_match_by = None
            end_match_by = None

            if "start" in edge_data and "end" in edge_data:
                # Direct format: {"start": "id", "end": "id"}
                start_node = edge_data["start"]["value"]
                start_match_by = edge_data["start"]["match_by"]
                end_node = edge_data["end"]["value"]
                end_match_by = edge_data["end"]["match_by"]

            if not start_node or not end_node:
                return None

            properties_data = edge_data.get("properties", {})

            # Create Properties instance if properties data exists
            properties = None
            if properties_data:
                properties = Properties()
                for key, value in properties_data.items():
                    properties[key] = value

            return cls(
                start_node, end_node, kind, properties, start_match_by, end_match_by
            )
        except (KeyError, TypeError, ValueError):
            return None

    def get_start_node(self) -> str:
        """
        Get the start node ID.

        Returns:
          - str: Start node ID
        """
        return self.start_node

    def get_end_node(self) -> str:
        """
        Get the end node ID.

        Returns:
          - str: End node ID
        """
        return self.end_node

    def get_kind(self) -> str:
        """
        Get the edge kind/type.

        Returns:
          - str: Edge kind
        """
        return self.kind

    def get_unique_id(self) -> str:
        """
        Get a unique ID for the edge.

        Returns:
          - str: Unique ID for the edge
        """
        return f"[{self.start_match_by}:{self.start_node}]-({self.kind})->[{self.end_match_by}:{self.end_node}]"

    def __eq__(self, other):
        """
        Check if two edges are equal based on their start, end, and kind.

        Args:
          - other (Edge): The other edge to compare to

        Returns:
          - bool: True if the edges are equal, False otherwise
        """
        if isinstance(other, Edge):
            return (
                self.start_node == other.start_node
                and self.end_node == other.end_node
                and self.kind == other.kind
            )
        return False

    def __hash__(self):
        """
        Hash based on start, end, and kind for use in sets and as dictionary keys.

        Returns:
          - int: Hash of the start, end, and kind
        """
        return hash((self.start_node, self.end_node, self.kind))

    def validate(self) -> tuple[bool, list[str]]:
        """
        Validate the edge against the EDGE_SCHEMA.
        
        Returns:
            - tuple[bool, list[str]]: (is_valid, list_of_errors)
        """
        errors = []
        
        # Validate required fields
        if not self.start_node or self.start_node is None:
            errors.append("Start node cannot be empty")
        elif not isinstance(self.start_node, str):
            errors.append("Start node must be a string")
            
        if not self.end_node or self.end_node is None:
            errors.append("End node cannot be empty")
        elif not isinstance(self.end_node, str):
            errors.append("End node must be a string")
            
        if not self.kind or self.kind is None:
            errors.append("Edge kind cannot be empty")
        elif not isinstance(self.kind, str):
            errors.append("Edge kind must be a string")
        
        # Validate match_by values
        if not isinstance(self.start_match_by, str):
            errors.append("Start match_by must be a string")
        elif self.start_match_by not in ["id", "name"]:
            errors.append("Start match_by must be either 'id' or 'name'")
            
        if not isinstance(self.end_match_by, str):
            errors.append("End match_by must be a string")
        elif self.end_match_by not in ["id", "name"]:
            errors.append("End match_by must be either 'id' or 'name'")
        
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
        return f"Edge(start='{self.start_node}', end='{self.end_node}', kind='{self.kind}', properties={self.properties})"
