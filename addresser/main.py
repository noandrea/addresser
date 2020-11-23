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

import argparse
import logging
from . import APP, _version
from .parser import parse, Address
from faker import Faker
import time
import json


def _to_json(a: Address, verbose: bool = False) -> str:
    if verbose:
        return json.dumps({
            "street": a.street,
            "housenumber": a.number,
            "src": a.src,
        })
    return json.dumps({
        "street": a.street,
        "housenumber": a.number
    })


def cmd_parse(args):
    """
    Parse one address

    Args:
        args: command line arguments
    """
    try:
        a = parse(args.data)
        print(_to_json(a, a.verbose))
    except Exception as err:
        print(f"Error massaging data: {err}")


def cmd_parse_file(args):
    """
    Parse a file containing addresses to their structured format
    """
    print(f"will process entries from {args.input} to {args.output}")
    start, count = time.time(), 0
    with open(args.input) as fr, open(args.output, "w") as fw:
        for line in fr:
            record = parse(line)
            fw.write(_to_json(record, args.verbose))
            count += 1
    print(f"completed: processed {count} lines in {time.time() - start}")


def cmd_generate_address(args):
    print(f"will generate {args.num} random addresses to {args.output}")
    start = time.time()
    locales = ['en', 'de', 'es', 'la',
               'ar_AA', 'ar_EG', 'ar_JO',
               'ar_PS', 'ar_SA', 'bg_BG',
               'bs_BA', 'cs_CZ', 'dk_DK',
               'el_CY', 'el_GR', 'et_EE',
               'fa_IR', 'fi_FI', 'fil_PH',
               'fr_CH', 'fr_FR', 'fr_QC',
               'he_IL', 'hi_IN', 'hr_HR',
               'hu_HU', 'hy_AM', 'id_ID',
               'it_IT', 'ja_JP', 'ka_GE',
               'ko_KR', 'lb_LU', 'lt_LT',
               'lv_LV', 'mt_MT', 'ne_NP',
               'nl_BE', 'nl_NL', 'no_NO',
               'pl_PL', 'pt_BR', 'pt_PT',
               'ro_RO', 'ru_RU', 'sk_SK',
               'sl_SI', 'sv_SE', 'ta_IN',
               'th_TH', 'tl_PH', 'tr_TR',
               'tw_GH', 'uk_UA', 'zh_CN',
               'zh_TW']

    # create a new faker instance
    Faker.seed(0)
    f = Faker(locales)
    # write the generated file
    with open(args.output, "w") as fp:
        for x in range(args.num):
            fp.write(f.street_address())
            fp.write("\n")
    print(f"completed: generated {args.num} lines in {time.time() - start}")


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
            "name": "parse",
            "help": "Parse an input string into a structured address",
            "target": cmd_parse,
            "opts": [
                {
                    "names": ["data"],
                    "help": "the string to prase",
                },
                {
                    "names": ["-v", "--verbose"],
                    "help": "add verbose json data (the original source)",
                    "action": "store_true",
                    "type": bool,
                    "default": False
                }
            ]
        },
        {
            "name": "parse-file",
            "help": "Parse a address list file into a JSONlines file",
            "target": cmd_parse_file,
            "opts": [
                {
                    "names": ["-o", "--output"],
                    "help": "the output JSONlines file name",
                    "default": "addresses.jsonl"
                },
                {
                    "names": ["-i", "--input"],
                    "help": "the input plain text file with addresses",
                    "default": "addresses.txt"
                },
                {
                    "names": ["-v", "--verbose"],
                    "help": "add verbose json data (the original source)",
                    "action": "store_true",
                    "default": False
                },
            ]
        },
        {
            "name": "generate-addresses",
            "help": "Generate a file with a list of addresses",
            "target": cmd_generate_address,
            "opts": [
                {
                    "names": ["-o", "--output"],
                    "help": "the file to write the list to",
                    "default": "addresses.txt"
                },
                {
                    "names": ["-n", "--num"],
                    "help": "number of records to generate",
                    "type": int,
                    "default": 100,
                },
            ]
        },
        {
            "name": "version",
            "help": "Print the version and exit",
            "target": cmd_version,
            "opts": []
        },

    ]
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()
    subparsers.required = True
    subparsers.dest = "command"
    # register all the commands
    for c in commands:
        subparser = subparsers.add_parser(c["name"], help=c["help"])
        subparser.set_defaults(func=c["target"])
        # add the sub arguments
        for sa in c.get("opts", []):
            kwargs = dict(
                help=sa.get("help"),
                default=sa.get("default"),
                type=sa.get("type", str),
            )
            if sa.get("action") is not None:
                del kwargs["type"]
                kwargs["action"] = sa.get("action")
            # parse the command
            subparser.add_argument(*sa["names"], **kwargs)

    # parse the arguments
    args = parser.parse_args()
    # call the function
    args.func(args)


if __name__ == "__main__":
    main()
