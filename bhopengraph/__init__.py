#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File name          : __init__.py
# Author             : Remi Gascou (@podalirius_)
# Date created       : 12 Aug 2025

"""
OpenGraph module for BloodHound integration.

This module provides Python classes for creating and managing graph structures
that are compatible with BloodHound OpenGraph.
"""

from .__version__ import __version__
from .Edge import (
    MATCH_BY_ID,
    MATCH_BY_NAME,
    MATCH_BY_PROPERTY,
    Edge,
    Endpoint,
    PropertyMatcher,
)
from .Node import Node
from .OpenGraph import OpenGraph
from .Properties import Properties

__version__

__author__ = "Remi Gascou (@podalirius_)"

__all__ = [
    "Properties",
    "Node",
    "Edge",
    "Endpoint",
    "PropertyMatcher",
    "OpenGraph",
    "MATCH_BY_ID",
    "MATCH_BY_NAME",
    "MATCH_BY_PROPERTY",
]
