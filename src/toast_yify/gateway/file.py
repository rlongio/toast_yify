#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This is a skeleton file that can serve as a starting point for a Python
console script. To run this script uncomment the following lines in the
[options.entry_points] section in setup.cfg:

    console_scripts =
         fibonacci = toast_yify.skeleton:run

Then run `python setup.py install` which will install the command `fibonacci`
inside your current environment.
Besides console scripts, the header (i.e. until _logger...) of this file can
also be used as template for Python modules.

Note: This skeleton file can be safely removed if not needed!
"""

import argparse
import logging
import sys
import csv

from toast_yify import __version__

__author__ = "Ryan Long"
__copyright__ = "Ryan Long"
__license__ = "mit"

_logger = logging.getLogger(__name__)


class File:

    def __init__(self, file_path="./TOAST_YIFY"):
        self.file_path = file_path


    def fetch_latest_entries(self):
        with open(self.file_path, newline='') as csv_file:
            db_reader = csv.reader(csv_file, delimiter=',', quotechar='|')
            for i in db_reader:
                yield {
                    'name': i[2],
                    'image_url': i[1],
                    'rating': i[3],
                    'categories': i[0],
                }

    def add_entry(self, data):
        row = [data[x] for x in sorted(data.keys())]
        with open(self.file_path, 'w', newline='') as csv_file:
            db_writer = csv.writer(csv_file, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            db_writer.writerow(row)

    def add_entries(self, data):
        with open(self.file_path, 'w', newline='') as csv_file:
            db_writer = csv.writer(csv_file, delimiter=',',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
            for row in data:
                db_writer.writerow(row[x] for x in sorted(row.keys()))



def parse_args(args):
    """Parse command line parameters

    Args:
      args ([str]): command line parameters as list of strings

    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
    """
    parser = argparse.ArgumentParser(
        description="Just a Fibonnaci demonstration")
    parser.add_argument(
        '--version',
        action='version',
        version='toast_yify {ver}'.format(ver=__version__))
    parser.add_argument(
        dest="n",
        help="n-th Fibonacci number",
        type=int,
        metavar="INT")
    parser.add_argument(
        '-v',
        '--verbose',
        dest="loglevel",
        help="set loglevel to INFO",
        action='store_const',
        const=logging.INFO)
    parser.add_argument(
        '-vv',
        '--very-verbose',
        dest="loglevel",
        help="set loglevel to DEBUG",
        action='store_const',
        const=logging.DEBUG)
    return parser.parse_args(args)


def setup_logging(loglevel):
    """Setup basic logging

    Args:
      loglevel (int): minimum loglevel for emitting messages
    """
    logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    logging.basicConfig(level=loglevel, stream=sys.stdout,
                        format=logformat, datefmt="%Y-%m-%d %H:%M:%S")


def main(args):
    pass

def run():
    """Entry point for console_scripts
    """
    main(sys.argv[1:])


if __name__ == "__main__":
    run()
