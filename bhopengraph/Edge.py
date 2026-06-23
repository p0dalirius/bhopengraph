#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File name          : Edge.py
# Author             : Remi Gascou (@podalirius_)
# Date created       : 12 Aug 2025

import re

from bhopengraph.Properties import Properties, primitive_category

# match_by strategies for resolving an edge endpoint to a node, as defined by
# the BloodHound OpenGraph edge schema.
#
# Source: https://bloodhound.specterops.io/opengraph/developer/edges

# MATCH_BY_ID resolves an endpoint by unique node id. This is the default.
MATCH_BY_ID = "id"
# MATCH_BY_NAME resolves an endpoint by name. Deprecated in BloodHound but still
# accepted; supported here so payloads using it can round-trip.
MATCH_BY_NAME = "name"
# MATCH_BY_PROPERTY resolves an endpoint dynamically from one or more property
# matchers evaluated at ingestion time.
MATCH_BY_PROPERTY = "property"

# The set of match strategies supported by the OpenGraph edge schema.
MATCH_BY_STRATEGIES = (MATCH_BY_ID, MATCH_BY_NAME, MATCH_BY_PROPERTY)

# edge_kind_pattern is the set of characters the OpenGraph schema allows in an
# edge kind: uppercase letters, lowercase letters, digits, and underscores.
#
# Source: https://bloodhound.specterops.io/opengraph/developer/edges
EDGE_KIND_PATTERN = re.compile(r"^[A-Za-z0-9_]+$")

# RESERVED_KIND_PREFIX is reserved by BloodHound in any letter case and must not
# be used for custom edge kinds.
RESERVED_KIND_PREFIX = "tag_"


def validate_kind(kind: str):
    """
    Validate an OpenGraph edge kind.

    A valid edge kind is non-empty, matches ``^[A-Za-z0-9_]+$`` (no spaces,
    dashes, or punctuation), and does not use the reserved ``tag_`` prefix (in
    any letter case).

    Source: https://bloodhound.specterops.io/opengraph/developer/edges

    Args:
      - kind (str): The edge kind to validate

    Returns:
      - str | None: An error message if the kind is invalid, otherwise None
    """
    if not kind:
        return "Edge kind cannot be empty"
    if not isinstance(kind, str):
        return "Edge kind must be a string"
    if not EDGE_KIND_PATTERN.match(kind):
        return f"Edge kind '{kind}' must match {EDGE_KIND_PATTERN.pattern}"
    if kind[: len(RESERVED_KIND_PREFIX)].lower() == RESERVED_KIND_PREFIX:
        return f"Edge kind '{kind}' must not use the reserved '{RESERVED_KIND_PREFIX}' prefix"
    return None


# https://bloodhound.specterops.io/opengraph/developer/edges
EDGE_SCHEMA = {
    "title": "Generic Ingest Edge",
    "description": "Defines an edge between two nodes in a generic graph ingestion system. Each edge specifies a start and end node, resolved either by unique identifier (id), by name, or dynamically through property matchers. A kind is required to indicate the relationship type. Optional properties may include custom attributes. You may optionally constrain the start or end node to a specific kind using the kind field inside each reference.",
    "type": "object",
    "properties": {
        "start": {
            "type": "object",
            "properties": {
                "match_by": {
                    "type": "string",
                    "enum": ["id", "name", "property"],
                    "default": "id",
                    "description": "How to resolve the start node: by its unique object ID, by its name property, or dynamically by property matchers.",
                },
                "value": {
                    "type": "string",
                    "description": "The value used for matching — either an object ID or a name, depending on match_by. Absent when match_by is 'property'.",
                },
                "property_matchers": {
                    "type": "array",
                    "description": "Property match criteria, used when match_by is 'property'. Matchers are AND-combined.",
                    "items": {
                        "type": "object",
                        "properties": {
                            "key": {"type": "string"},
                            "operator": {"type": "string"},
                            "value": {},
                        },
                        "required": ["key"],
                    },
                },
                "kind": {
                    "type": "string",
                    "description": "Optional kind filter; the referenced node must have this kind.",
                },
            },
        },
        "end": {
            "type": "object",
            "properties": {
                "match_by": {
                    "type": "string",
                    "enum": ["id", "name", "property"],
                    "default": "id",
                    "description": "How to resolve the end node: by its unique object ID, by its name property, or dynamically by property matchers.",
                },
                "value": {
                    "type": "string",
                    "description": "The value used for matching — either an object ID or a name, depending on match_by. Absent when match_by is 'property'.",
                },
                "property_matchers": {
                    "type": "array",
                    "description": "Property match criteria, used when match_by is 'property'. Matchers are AND-combined.",
                    "items": {
                        "type": "object",
                        "properties": {
                            "key": {"type": "string"},
                            "operator": {"type": "string"},
                            "value": {},
                        },
                        "required": ["key"],
                    },
                },
                "kind": {
                    "type": "string",
                    "description": "Optional kind filter; the referenced node must have this kind.",
                },
            },
        },
        "kind": {"type": "string"},
        "properties": {
            "type": ["object", "null"],
            "description": "A key-value map of edge attributes. Values must not be objects. If a value is an array, it must contain only primitive types (e.g., strings, numbers, booleans) and must be homogeneous (all items must be of the same type).",
            "additionalProperties": {
                "type": ["string", "number", "boolean", "array"],
                "items": {"not": {"type": "object"}},
            },
        },
    },
    "required": ["start", "end", "kind"],
    "examples": [
        {
            "start": {"match_by": "id", "value": "user-1234"},
            "end": {"match_by": "id", "value": "server-5678"},
            "kind": "HasSession",
            "properties": {"timestamp": "2025-04-16T12:00:00Z", "duration_minutes": 45},
        },
        {
            "start": {"match_by": "name", "value": "alice", "kind": "User"},
            "end": {"match_by": "name", "value": "file-server-1", "kind": "Server"},
            "kind": "AccessedResource",
            "properties": {"via": "SMB", "sensitive": True},
        },
        {
            "start": {
                "match_by": "property",
                "property_matchers": [
                    {"key": "username", "operator": "equals", "value": "alice.smith"}
                ],
                "kind": "User",
            },
            "end": {"match_by": "id", "value": "server-1"},
            "kind": "CustomRelationship",
        },
    ],
}


class PropertyMatcher(object):
    """
    A single property-based match criterion, used when an edge endpoint's match
    strategy is ``property``.

    Matcher values are restricted to primitives (string, number, boolean) by the
    schema. Multiple matchers on an endpoint are AND-combined. Only the
    ``equals`` operator is currently supported by BloodHound.

    Source: https://bloodhound.specterops.io/opengraph/developer/edges
    """

    def __init__(self, key: str, value, operator: str = "equals"):
        """
        Initialize a PropertyMatcher.

        Args:
          - key (str): The property name to match against
          - value: The value to compare against (must be a primitive)
          - operator (str): The comparison operator (defaults to "equals")
        """
        self.key = key
        self.operator = operator
        self.value = value

    def validate(self) -> tuple:
        """
        Validate the property matcher.

        Returns:
          - tuple[bool, list[str]]: (is_valid, list_of_errors)
        """
        errors = []
        if not self.key:
            errors.append("Property matcher requires a non-empty key")
        elif not isinstance(self.key, str):
            errors.append("Property matcher key must be a string")
        if self.value is not None and primitive_category(self.value) == "":
            errors.append("Property matcher value must be a primitive")
        return len(errors) == 0, errors

    def to_dict(self) -> dict:
        """
        Convert the matcher to a dictionary for JSON serialization.

        Returns:
          - dict: Matcher as {"key": ..., "operator": ..., "value": ...}
        """
        return {"key": self.key, "operator": self.operator, "value": self.value}

    def _signature(self) -> tuple:
        return (self.key, self.operator, self.value)

    def __eq__(self, other):
        if isinstance(other, PropertyMatcher):
            return self._signature() == other._signature()
        return False

    def __hash__(self):
        return hash(self._signature())

    def __repr__(self) -> str:
        return f"PropertyMatcher(key='{self.key}', operator='{self.operator}', value={self.value!r})"


class Endpoint(object):
    """
    Identifies the start or end of an edge and describes how BloodHound should
    resolve it to a node.

    An endpoint can be resolved by node id (the default and preferred strategy),
    by name (deprecated but still accepted), or dynamically by property matchers.
    An optional ``kind`` filter constrains the matched node to a specific kind;
    it is strongly recommended when matching by name or property to avoid
    attaching the edge to the wrong node on a name collision.

    Source: https://bloodhound.specterops.io/opengraph/developer/edges
    """

    def __init__(
        self,
        match_by: str = MATCH_BY_ID,
        value: str = "",
        kind: str = "",
        property_matchers: list = None,
    ):
        """
        Initialize an Endpoint.

        Prefer the ``by_id``, ``by_name``, and ``by_property`` constructors for
        clarity.

        Args:
          - match_by (str): One of "id", "name", or "property"
          - value (str): The id or name value (for "id"/"name" strategies)
          - kind (str): Optional kind filter
          - property_matchers (list): PropertyMatcher list (for "property")
        """
        self.match_by = match_by or MATCH_BY_ID
        self.value = value or ""
        self.kind = kind or ""
        self.property_matchers = list(property_matchers) if property_matchers else []

    @classmethod
    def by_id(cls, value: str) -> "Endpoint":
        """Create an endpoint resolved by node id."""
        return cls(match_by=MATCH_BY_ID, value=value)

    @classmethod
    def by_name(cls, value: str, kind: str = "") -> "Endpoint":
        """
        Create an endpoint resolved by name. ``kind`` is optional and
        disambiguates the kind of the target node.
        """
        return cls(match_by=MATCH_BY_NAME, value=value, kind=kind)

    @classmethod
    def by_property(cls, property_matchers: list, kind: str = "") -> "Endpoint":
        """
        Create an endpoint resolved by property matchers. ``kind`` is optional.
        """
        return cls(
            match_by=MATCH_BY_PROPERTY, kind=kind, property_matchers=property_matchers
        )

    def validate(self) -> tuple:
        """
        Validate the endpoint for internal consistency with its match strategy.

        Returns:
          - tuple[bool, list[str]]: (is_valid, list_of_errors)
        """
        errors = []
        if self.match_by in (MATCH_BY_ID, MATCH_BY_NAME):
            if not self.value:
                errors.append(
                    f"Endpoint with match_by '{self.match_by}' requires a non-empty value"
                )
            elif not isinstance(self.value, str):
                errors.append("Endpoint value must be a string")
        elif self.match_by == MATCH_BY_PROPERTY:
            if not self.property_matchers:
                errors.append(
                    "Endpoint with match_by 'property' requires at least one property matcher"
                )
            for matcher in self.property_matchers:
                if not isinstance(matcher, PropertyMatcher):
                    errors.append("Property matchers must be PropertyMatcher instances")
                    continue
                is_matcher_valid, matcher_errors = matcher.validate()
                if not is_matcher_valid:
                    errors.extend(matcher_errors)
        else:
            errors.append(f"Unsupported match_by '{self.match_by}'")
        return len(errors) == 0, errors

    def to_dict(self) -> dict:
        """
        Convert the endpoint to a dictionary for JSON serialization, matching the
        shape BloodHound expects for the endpoint's match strategy.

        Returns:
          - dict: Endpoint as a dictionary
        """
        endpoint_dict = {"match_by": self.match_by}

        if self.match_by == MATCH_BY_PROPERTY:
            endpoint_dict["property_matchers"] = [
                matcher.to_dict() for matcher in self.property_matchers
            ]
        else:
            endpoint_dict["value"] = self.value

        if self.kind:
            endpoint_dict["kind"] = self.kind

        return endpoint_dict

    @classmethod
    def from_dict(cls, data: dict) -> "Endpoint":
        """
        Create an Endpoint from a dictionary (typically parsed from JSON).

        Defaults to id matching when ``match_by`` is omitted.

        Args:
          - data (dict): Dictionary containing endpoint data

        Returns:
          - Endpoint: Endpoint instance
        """
        match_by = data.get("match_by") or MATCH_BY_ID
        kind = data.get("kind", "")

        if match_by == MATCH_BY_PROPERTY:
            matchers = []
            for matcher_data in data.get("property_matchers", []):
                matchers.append(
                    PropertyMatcher(
                        key=matcher_data.get("key"),
                        value=matcher_data.get("value"),
                        operator=matcher_data.get("operator", "equals"),
                    )
                )
            return cls.by_property(matchers, kind)

        return cls(match_by=match_by, value=data.get("value", ""), kind=kind)

    def signature(self) -> tuple:
        """
        Return a hashable signature uniquely identifying this endpoint, used for
        edge equality and deduplication.

        Returns:
          - tuple: A hashable representation of the endpoint
        """
        return (
            self.match_by,
            self.value,
            self.kind,
            tuple(matcher._signature() for matcher in self.property_matchers),
        )

    def __eq__(self, other):
        if isinstance(other, Endpoint):
            return self.signature() == other.signature()
        return False

    def __hash__(self):
        return hash(self.signature())

    def __repr__(self) -> str:
        if self.match_by == MATCH_BY_PROPERTY:
            return f"Endpoint(match_by='{self.match_by}', kind='{self.kind}', property_matchers={self.property_matchers})"
        return f"Endpoint(match_by='{self.match_by}', value='{self.value}', kind='{self.kind}')"


class Edge(object):
    """
    Edge class representing a directed edge in the OpenGraph.

    Follows BloodHound OpenGraph schema requirements with start/end endpoints,
    kind, and properties. All edges are directed and one-way as per BloodHound
    requirements.

    Sources:
    - https://bloodhound.specterops.io/opengraph/developer/edges
    - https://bloodhound.specterops.io/opengraph/developer/graph-data
    """

    def __init__(
        self,
        start_node: str,
        end_node: str,
        kind: str,
        properties: Properties = None,
        start_match_by: str = MATCH_BY_ID,
        end_match_by: str = MATCH_BY_ID,
    ):
        """
        Initialize an Edge whose endpoints are resolved by id or name.

        For property-based matching or kind filters on endpoints, use the
        ``with_endpoints`` constructor.

        Args:
          - start_node (str): Value of the source endpoint (id or name)
          - end_node (str): Value of the destination endpoint (id or name)
          - kind (str): Type/class of the edge relationship
          - properties (Properties): Edge properties
          - start_match_by (str): "id" (default) or "name"
          - end_match_by (str): "id" (default) or "name"
        """
        if not start_node:
            raise ValueError("Start node ID cannot be empty")
        if not end_node:
            raise ValueError("End node ID cannot be empty")

        self._init_common(
            Endpoint(match_by=start_match_by, value=start_node),
            Endpoint(match_by=end_match_by, value=end_node),
            kind,
            properties,
        )

    @classmethod
    def with_endpoints(
        cls,
        start: Endpoint,
        end: Endpoint,
        kind: str,
        properties: Properties = None,
    ) -> "Edge":
        """
        Create an Edge from explicit endpoints, allowing any match strategy for
        either end (id, name, or property).

        Args:
          - start (Endpoint): The source endpoint
          - end (Endpoint): The destination endpoint
          - kind (str): Type/class of the edge relationship
          - properties (Properties): Edge properties

        Returns:
          - Edge: A new Edge instance
        """
        obj = cls.__new__(cls)
        obj._init_common(start, end, kind, properties)
        return obj

    def _init_common(
        self, start: Endpoint, end: Endpoint, kind: str, properties: Properties
    ):
        kind_error = validate_kind(kind)
        if kind_error:
            raise ValueError(kind_error)

        is_start_valid, start_errors = start.validate()
        if not is_start_valid:
            raise ValueError(f"Invalid start endpoint: {'; '.join(start_errors)}")

        is_end_valid, end_errors = end.validate()
        if not is_end_valid:
            raise ValueError(f"Invalid end endpoint: {'; '.join(end_errors)}")

        self.start = start
        self.end = end
        self.kind = kind
        self.properties = properties or Properties()

    # Backward-compatible accessors for the pre-endpoint Edge API. These expose
    # the underlying endpoints so existing callers using start_node / end_node /
    # start_match_by / end_match_by continue to work unchanged.

    @property
    def start_node(self) -> str:
        return self.start.value

    @start_node.setter
    def start_node(self, value: str):
        self.start.value = value

    @property
    def end_node(self) -> str:
        return self.end.value

    @end_node.setter
    def end_node(self, value: str):
        self.end.value = value

    @property
    def start_match_by(self) -> str:
        return self.start.match_by

    @start_match_by.setter
    def start_match_by(self, value: str):
        self.start.match_by = value

    @property
    def end_match_by(self) -> str:
        return self.end.match_by

    @end_match_by.setter
    def end_match_by(self, value: str):
        self.end.match_by = value

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
            "start": self.start.to_dict(),
            "end": self.end.to_dict(),
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

            if "start" not in edge_data or "end" not in edge_data:
                return None

            start = Endpoint.from_dict(edge_data["start"])
            end = Endpoint.from_dict(edge_data["end"])

            properties_data = edge_data.get("properties", {})

            # Create Properties instance if properties data exists
            properties = None
            if properties_data:
                properties = Properties()
                for key, value in properties_data.items():
                    properties[key] = value

            return cls.with_endpoints(start, end, kind, properties)
        except (KeyError, TypeError, ValueError):
            return None

    def get_start_node(self) -> str:
        """
        Get the start endpoint value (the id or name; empty for property-matched
        endpoints).

        Returns:
          - str: Start endpoint value
        """
        return self.start.value

    def get_end_node(self) -> str:
        """
        Get the end endpoint value (the id or name; empty for property-matched
        endpoints).

        Returns:
          - str: End endpoint value
        """
        return self.end.value

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
        return f"[{self.start.signature()}]-({self.kind})->[{self.end.signature()}]"

    def __eq__(self, other):
        """
        Check if two edges are equal based on their endpoints and kind.

        Args:
          - other (Edge): The other edge to compare to

        Returns:
          - bool: True if the edges are equal, False otherwise
        """
        if isinstance(other, Edge):
            return (
                self.kind == other.kind
                and self.start == other.start
                and self.end == other.end
            )
        return False

    def __hash__(self):
        """
        Hash based on endpoints and kind for use in sets and as dictionary keys.

        Returns:
          - int: Hash of the endpoints and kind
        """
        return hash((self.start.signature(), self.end.signature(), self.kind))

    def validate(self) -> tuple:
        """
        Validate the edge against the EDGE_SCHEMA.

        Returns:
            - tuple[bool, list[str]]: (is_valid, list_of_errors)
        """
        errors = []

        # Validate kind
        kind_error = validate_kind(self.kind)
        if kind_error:
            errors.append(kind_error)

        # Validate endpoints
        is_start_valid, start_errors = self.start.validate()
        if not is_start_valid:
            errors.extend(f"Start endpoint: {e}" for e in start_errors)

        is_end_valid, end_errors = self.end.validate()
        if not is_end_valid:
            errors.extend(f"End endpoint: {e}" for e in end_errors)

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
        return f"Edge(start='{self.start.value}', end='{self.end.value}', kind='{self.kind}', properties={self.properties})"
