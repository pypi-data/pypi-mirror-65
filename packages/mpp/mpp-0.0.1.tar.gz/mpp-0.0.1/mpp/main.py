#!/usr/bin/env python

import argparse
import sys

from mpp.src.commands import setup, config, freeze, installer


__version__ = "0.0.1"


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    setup_parser = subparsers.add_parser(
        "setup",
        description="Ask some questions to setup the project",
        help="ask some questions to setup the project"
    )
    setup_parser.set_defaults(func=setup)

    config_parser = subparsers.add_parser(
        "config",
        description="Show project parameters and edit them",
        help="show project parameters and edit them"
    )
    config_parser.add_argument("parameters", metavar="parameter", nargs="*", help="parameters to edit")
    config_parser.add_argument("--list", action="store_true", help="show project parameters")
    config_parser.set_defaults(func=config)

    freeze_parser = subparsers.add_parser(
        "freeze",
        description="Create an executable using PyInstaller",
        help="create an executable using PyInstaller"
    )
    freeze_parser.set_defaults(func=freeze)

    installer_parser = subparsers.add_parser(
        "installer",
        description="Create an installer with NSIS",
        help="create an installer with NSIS"
    )
    installer_parser.set_defaults(func=installer)

    args = parser.parse_args()

    if not hasattr(args, "func"):
        parser.print_help()
        sys.exit(0)

    args.func(args)
