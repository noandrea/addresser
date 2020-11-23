#!/usr/bin/env python3

# Copyright © 2020 Andrea Giacobino <no.andrea@gmail.com>

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from . import APP, _version
from .parser import parse
import argparse
import logging


def cmd_parse_once(args):
    """
    Parse one address
    """
    try:
        a = parse(args.data)
        print(a)
    except Exception as err:
        print(f"Error massaging data: {err}")


def cmd_version(args):
    """
    Print the version and exit
    """
    print(f"{APP} v{_version()}")


def main():
    # initialize logging
    logging.basicConfig(level=logging.ERROR)
    # list commands
    commands = [
        {
            'name': 'parse',
            'help': 'Parse an input string into a structured address',
            'target': cmd_parse_once,
            'opts': [
                {
                    "names": ["-i", "--input"],
                    "help": "The input csv file (default data.csv)",
                    "default": "data.csv"
                },
            ]
        },
        {
            'name': 'parse-stdin',
            'help': '''Read from the standard input and writes
the result on the standard output''',
            'target': cmd_parse_once,
            'opts': []
        },
        {
            'name': 'version',
            'help': 'Print the version and exit',
            'target': cmd_version,
            'opts': []
        },

    ]
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()
    subparsers.required = True
    subparsers.dest = 'command'
    # register all the commands
    for c in commands:
        subparser = subparsers.add_parser(c['name'], help=c['help'])
        subparser.set_defaults(func=c['target'])
        # add the sub arguments
        for sa in c.get('opts', []):
            subparser.add_argument(*sa['names'],
                                   help=sa['help'],
                                   action=sa.get('action'),
                                   default=sa.get('default'))

    # parse the arguments
    args = parser.parse_args()
    # call the function
    args.func(args)


if __name__ == "__main__":
    main()
