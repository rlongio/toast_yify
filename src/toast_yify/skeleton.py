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
from time import sleep

from bs4 import BeautifulSoup
from win10toast import ToastNotifier

from toast_yify import __version__

from toast_yify.gateway.file import File

__author__ = "Ryan Long"
__copyright__ = "Ryan Long"
__license__ = "mit"

_logger = logging.getLogger(__name__)

DB = File()


def toast():
    toaster = ToastNotifier()
    toaster.show_toast("Hello World!!!",
                       "Python is 10 seconds awsm!",
                       icon_path="custom.ico",
                       duration=10)

    toaster.show_toast("Example two",
                       "This notification is in it's own thread!",
                       icon_path=None,
                       duration=5,
                       threaded=True)
    # Wait for threaded notification to finish
    while toaster.notification_active():
        sleep(0.1)


def parse_entries_from_html(html_doc):
    soup = BeautifulSoup(html_doc, 'html.parser').find_all('figure')
    for node in soup:
        yield from build_entry(node)


def build_entry(node):
    yield {
        'name': node.img['alt'].replace(" download", ""),
        'image_url': node.img['src'],
        'rating': ' '.join([x.string for x in node.find_all('h4')[:1]]),
        'categories': ', '.join(
            [x.string for x in node.find_all('h4')[1:]]),
    }


def get_latest_x_entries_from_persistence(max=10):
    entries = DB.fetch_latest_entries()
    index = 1
    while index < max:
        try:
            index += 1
            yield next(entries)
        except StopIteration:
            return


def get_latest_x_entries_from_site(number=None):
    default = 10
    if number is None:
        number = default
    result = []
    for x in range(number):
        result.append(x)
    return result


def update():
    """
    * Connect to VPN
    1. Pull last X entries from site
    2. Pull last X entries from persistence
    3. Get the diff
        1. If diff write to persistence
        *. Rotating?
        2. If diff send toast
    :return:
    """
    return True


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
    """Main entry point allowing external calls

    Args:
      args ([str]): command line parameter list
    """
    args = parse_args(args)
    setup_logging(args.loglevel)
    _logger.debug("Starting crazy calculations...")
    print("The {}-th Fibonacci number is {}".format(args.n, args.n))
    _logger.info("Script ends here")


def run():
    """Entry point for console_scripts
    """
    main(sys.argv[1:])


if __name__ == "__main__":
    toast()
    run()
