#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File name          : Logger.py
# Author             : Remi Gascou (@podalirius_)
# Date created       : 21 Aug 2025

import time

class Logger(object):
    """
    Simple logger class that prints messages with timestamps
    """

    def __init__(self, debug=False):
        super(Logger, self).__init__()
        self.__debug = debug
        self.__indent_level = 0
    
    def increment_indent(self):
        """
        Increment the indentation level
        """
        self.__indent_level += 1

    def decrement_indent(self):
        """
        Decrement the indentation level
        """
        if self.__indent_level > 0:
            self.__indent_level -= 1

    def log(self, message):
        """
        Print a message with timestamp
        """
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        indent = "  │ " * self.__indent_level
        if self.__debug:
            print("[%s] [\x1b[92m-----\x1b[0m] %s%s" % (timestamp, indent, message))
        else:
            print("[%s] %s%s" % (timestamp, indent, message))

    def debug(self, message):
        """
        Print a debug message with timestamp
        """
        if self.__debug:
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            indent = "  │ " * self.__indent_level
            print("[%s] [\x1b[93mDEBUG\x1b[0m] %s%s" % (timestamp, indent, message))