#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File name          : Edge.py
# Author             : Remi Gascou (@podalirius_)
# Date created       : 12 Aug 2025

from bhopengraph.Properties import Properties


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
        start_node_id: str,
        end_node_id: str,
        kind: str,
        properties: Properties = None,
    ):
        """
        Initialize an Edge.

        Args:
          - start_node_id (str): ID of the source node
          - end_node_id (str): ID of the destination node
          - kind (str): Type/class of the edge relationship
          - properties (Properties): Edge properties
        """
        if not start_node_id:
            raise ValueError("Start node ID cannot be empty")
        if not end_node_id:
            raise ValueError("End node ID cannot be empty")
        if not kind:
            raise ValueError("Edge kind cannot be empty")

        self.start_node_id = start_node_id
        self.end_node_id = end_node_id
        self.kind = kind
        self.properties = properties or Properties()

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
            "start": {"value": self.start_node_id, "match_by": "id"},
            "end": {"value": self.end_node_id, "match_by": "id"},
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
            start_node_id = None
            end_node_id = None
            
            if "start" in edge_data and "end" in edge_data:
                # BloodHound format: {"start": {"value": "id"}, "end": {"value": "id"}}
                start_node_id = edge_data["start"].get("value")
                end_node_id = edge_data["end"].get("value")
            elif "source" in edge_data and "target" in edge_data:
                # Alternative format: {"source": "id", "target": "id"}
                start_node_id = edge_data["source"]
                end_node_id = edge_data["target"]
            elif "start_node_id" in edge_data and "end_node_id" in edge_data:
                # Direct format: {"start_node_id": "id", "end_node_id": "id"}
                start_node_id = edge_data["start_node_id"]
                end_node_id = edge_data["end_node_id"]
            
            if not start_node_id or not end_node_id:
                return None
            
            properties_data = edge_data.get("properties", {})
            
            # Create Properties instance if properties data exists
            properties = None
            if properties_data:
                properties = Properties()
                for key, value in properties_data.items():
                    properties[key] = value
            
            return cls(start_node_id, end_node_id, kind, properties)
        except (KeyError, TypeError, ValueError):
            return None

    def get_start_node_id(self) -> str:
        """
        Get the start node ID.

        Returns:
          - str: Start node ID
        """
        return self.start_node_id

    def get_end_node_id(self) -> str:
        """
        Get the end node ID.

        Returns:
          - str: End node ID
        """
        return self.end_node_id

    def get_kind(self) -> str:
        """
        Get the edge kind/type.

        Returns:
          - str: Edge kind
        """
        return self.kind

    def __eq__(self, other):
        """Check if two edges are equal based on their start, end, and kind."""
        if isinstance(other, Edge):
            return (
                self.start_node_id == other.start_node_id
                and self.end_node_id == other.end_node_id
                and self.kind == other.kind
            )
        return False

    def __hash__(self):
        """Hash based on start, end, and kind for use in sets and as dictionary keys."""
        return hash((self.start_node_id, self.end_node_id, self.kind))

    def __repr__(self) -> str:
        return f"Edge(start='{self.start_node_id}', end='{self.end_node_id}', kind='{self.kind}', properties={self.properties})"
