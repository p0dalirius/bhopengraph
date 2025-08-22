#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File name          : utils.py
# Author             : Remi Gascou (@podalirius_)
# Date created       : 21 Aug 2025


def filesize_string(size: int) -> str:
    """
    Convert a file size from bytes to a more readable format using the largest appropriate unit.

    This function takes an integer representing a file size in bytes and converts it to a human-readable
    string using the largest appropriate unit from bytes (B) to petabytes (PB). The result is rounded to
    two decimal places.

    Args:
        size (int): The file size in bytes.

    Returns:
        str: A string representing the file size in a more readable format, including the appropriate unit.
    """

    units = ["B", "kB", "MB", "GB", "TB", "PB"]
    for k in range(len(units)):
        if size < (1024 ** (k + 1)):
            break
    return "%4.2f %s" % (round(size / (1024 ** (k)), 2), units[k])
