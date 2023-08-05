import os
import sys
import argparse

def rfile(path: str):
    file: str = None
    if os.path.isfile(path) and os.access(path, os.R_OK): file = path
    return file

class Arguments(object):
    def __init__(self):
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
            version="xploitv v0.1.0",
            help="Print the version")

        # ---- Output
        output = self.__parser.add_argument_group(title="output")
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
        return self.__parser.parse_args()

    def help(self):
        self.__parser.print_help()
        sys.exit(1)
