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

from .Properties import Properties
from .Node import Node
from .Edge import Edge
from .OpenGraph import OpenGraph

__version__ = "1.1.0"
__author__ = "Remi Gascou (@podalirius_)"

__all__ = ["Properties", "Node", "Edge", "OpenGraph"]
