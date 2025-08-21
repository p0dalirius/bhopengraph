#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File name          : setup.py
# Author             : Remi Gascou (@podalirius_)
# Date created       : 12 Aug 2025

import setuptools

long_description = """
<p align="center">
  A python library to create BloodHound OpenGraphs easily
  <br>
  <img alt="PyPI" src="https://img.shields.io/pypi/v/bhopengraph">
  <img alt="GitHub release (latest by date)" src="https://img.shields.io/github/v/release/p0dalirius/bhopengraph">
  <a href="https://twitter.com/intent/follow?screen_name=podalirius_" title="Follow"><img src="https://img.shields.io/twitter/follow/podalirius_?label=Podalirius&style=social"></a>
  <a href="https://www.youtube.com/c/Podalirius_?sub_confirmation=1" title="Subscribe"><img alt="YouTube Channel Subscribers" src="https://img.shields.io/youtube/channel/subscribers/UCF_x5O7CSfr82AfNVTKOv_A?style=social"></a>
  <br>
</p>

## Features

This module provides Python classes for creating and managing graph structures that are compatible with BloodHound OpenGraph. The classes follow the [BloodHound OpenGraph schema](https://bloodhound.specterops.io/opengraph/schema) and [best practices](https://bloodhound.specterops.io/opengraph/best-practices).

If you don't know about BloodHound OpenGraph yet, a great introduction can be found here: [https://bloodhound.specterops.io/opengraph/best-practices](https://bloodhound.specterops.io/opengraph/best-practices)

## Examples

Here is an example of a Python program using the [bhopengraph](https://github.com/p0dalirius/bhopengraph) python library to model the [Minimal Working JSON](https://bloodhound.specterops.io/opengraph/schema#minimal-working-json) from the OpenGraph Schema documentation:

```py
from bhopengraph.OpenGraph import OpenGraph
from bhopengraph.Node import Node
from bhopengraph.Edge import Edge
from bhopengraph.Properties import Properties

# Create an OpenGraph instance
graph = OpenGraph(source_kind="Base")

# Create nodes
bob_node = Node(
    id="123",
    kinds=["Person", "Base"],
    properties=Properties(
        displayname="bob",
        property="a",
        objectid="123",
        name="BOB"
    )
)

alice_node = Node(
    id="234",
    kinds=["Person", "Base"],
    properties=Properties(
        displayname="alice",
        property="b",
        objectid="234",
        name="ALICE"
    )
)

# Add nodes to graph
graph.addNode(bob_node)
graph.addNode(alice_node)

# Create edge: Bob knows Alice
knows_edge = Edge(
    start_node_id=alice_node.id,
    end_node_id=bob_node.id,
    kind="Knows"
)

# Add edge to graph
graph.addEdge(knows_edge)

# Export to file
graph.exportToFile("minimal_example.json")
```

This gives us the following [Minimal Working JSON](https://bloodhound.specterops.io/opengraph/schema#minimal-working-json) as per the documentation:

```json
{
  "graph": {
    "nodes": [
      {
        "id": "123",
        "kinds": [
          "Person",
          "Base"
        ],
        "properties": {
          "displayname": "bob",
          "property": "a",
          "objectid": "123",
          "name": "BOB"
        }
      },
      {
        "id": "234",
        "kinds": [
          "Person",
          "Base"
        ],
        "properties": {
          "displayname": "alice",
          "property": "b",
          "objectid": "234",
          "name": "ALICE"
        }
      }
    ],
    "edges": [
      {
        "kind": "Knows",
        "start": {
          "value": "123",
          "match_by": "id"
        },
        "end": {
          "value": "234",
          "match_by": "id"
        }
      }
    ]
  },
  "metadata": {
    "source_kind": "Base"
  }
}
```

## Contributing

Pull requests are welcome. Feel free to open an issue if you want to add other features.

## References

- [BloodHound OpenGraph Best Practices](https://bloodhound.specterops.io/opengraph/best-practices)
- [BloodHound OpenGraph Schema](https://bloodhound.specterops.io/opengraph/schema)
- [BloodHound OpenGraph API](https://bloodhound.specterops.io/opengraph/api)
- [BloodHound OpenGraph Custom Icons](https://bloodhound.specterops.io/opengraph/custom-icons)

"""

with open('requirements.txt', 'r', encoding='utf-8') as f:
    requirements = [x.strip() for x in f.readlines()]

setuptools.setup(
    name="bhopengraph",
    version="1.1.0",
    description="A python library to create BloodHound OpenGraphs easily",
    url="https://github.com/p0dalirius/bhopengraph",
    author="Podalirius",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author_email="podalirius@protonmail.com",
    packages=["bhopengraph"],
    include_package_data=True,
    license="GPL2",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.11',
    install_requires=requirements,
    entry_points={
      "console_scripts": [
        "bhopengraph=bhopengraph.__main__:main"
      ]
    }
)
