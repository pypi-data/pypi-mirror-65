#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Core modules
# --------------
import os
import sys
import argparse

# File type
# -----------
def rfile(path: str):
    ''' Defines the characteristics of a read file '''
    file: str = None
    if os.path.isfile(path) and os.access(path, os.R_OK): file = path
    return file

# Arguments class
# -----------------
class Arguments(object):
    def __init__(self):
        ''' Argument parser '''
        # Name and description
        self.__parser = argparse.ArgumentParser(
            prog="xploitv",
            add_help=True)

        # ---- Information
        information = self.__parser.add_argument_group(title="information")
        # Version
        information.add_argument(
            "-v",
            action="count",
            help="Verbosity (Default: -vv)")
        information.add_argument(
            "--version",
            action="version",
            version="xploitv v0.1.1",
            help="Print the version")

        # ---- Performance
        performance = self.__parser.add_argument_group(title="performance")
        # Number of threads
        performance.add_argument(
            "-t", "--threads",
            type=int,
            default=20,
            help="Define the number of threads")

        # ---- Output
        output = self.__parser.add_argument_group(title="output")
        # No banner
        output.add_argument(
            "-b", "--bare",
            action="store_true",
            help="Hide the banner")
        # Output format
        output.add_argument(
            "-x", "--extension",
            type=str,
            metavar="FORMAT",
            choices=["csv","txt"],
            help="Output extension (csv,txt)")

        # ---- Grabber
        grabber = self.__parser.add_argument_group(title="grabber (one required)")
        how = grabber.add_mutually_exclusive_group()
        # From ID
        how.add_argument(
            "-i", "--id",
            type=str,
            metavar="ID",
            help="Grab all the accounts linked to an identifier")
        # From wordlist
        how.add_argument(
            "-w", "--wordlist",
            type=rfile,
            metavar="FILE",
            help="Grab all the accounts linked to identifiers in a wordlist")

    def parse(self):
        ''' Parse the arguments '''
        return self.__parser.parse_args()

    def help(self):
        ''' Show the help message '''
        self.__parser.print_help()
        sys.exit(1)
