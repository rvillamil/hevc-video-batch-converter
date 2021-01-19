#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Import external libraries
import logging
import sys
import argparse
from .__version__ import __version__

# Import my libraries
from .HEVCConverter import HEVCConverter, pretty_print


# Metadata
__author__ = "Rodrigo Villamil Pérez"
__copyright__ = "RVP"
__license__ = "MIT Licencese"

"""
This is a skeleton file that can serve as a starting point for a Python
console script. To run this script uncomment the following lines in the
[options.entry_points] section in setup.cfg:

    console_scripts =
         hevcbatchconverter = hevcbatchconverter:run

Then run `python setup.py install` which will install the command `hevcbatchconverter`
inside your current environment.
Besides console scripts, the header (i.e. until _logger...) of this file can
also be used as template for Python modules.
"""
_logger = logging.getLogger(__name__)

def parse_args(args):
    """Parse command line parameters

    Args:
      args ([str]): command line parameters as list of strings

    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
    """
    parser = argparse.ArgumentParser(
        description="Command line tool providing access to the GitLab server")
    parser.add_argument(
        "--version",
        action="version",
        version="hevcbatchconverter {ver}".format(ver=__version__),
    )
    parser.add_argument(
        "-v",
        "--verbose",
        dest="loglevel",
        help="set loglevel to INFO",
        action="store_const",
        const=logging.INFO,
    )
    parser.add_argument(
        "-vv",
        "--very-verbose",
        dest="loglevel",
        help="set loglevel to DEBUG",
        action="store_const",
        const=logging.DEBUG,
    )
    
    parser.add_argument(
        '-p',
        '--path',
        help='Download path',        
        required=True
    )

    return parser.parse_args(args)


def setup_logging(loglevel):
    """Setup basic logging

    Args:
      loglevel (int): minimum loglevel for emitting messages
    """
    logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    logging.basicConfig(
        level=loglevel,
        stream=sys.stdout,
        format=logformat,
        datefmt="%Y-%m-%d %H:%M:%S"
    )


def main(args):
    """Main entry point allowing external calls

    Args:
      args ([str]): command line parameter list
    """
    args = parse_args(args)
    setup_logging(args.loglevel)
    _logger.debug("Running tool!")   
    hevcconverter = HEVCConverter()
    print ("Getting XMP file list in directory '%s'\n" % (args.path))
    xmp_files_length=hevcconverter.print_all_convertible_files_in_dir(args.path) 
    print ("There are '%d' XMP files in directory '%s'\n" % (xmp_files_length, args.path))
    input ("Press Enter Key to continue or Ctrl-C to abort")
    hevcconverter.convert_dir(args.path)
    _logger.debug("Tool ends here!")


def run():
    """Entry point for console_scripts
    """
    main(sys.argv[1:])


if __name__ == "__main__":
    run()


