#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Import external libraries
import logging
import sys
import argparse
from .__version__ import __version__

# Import my libraries
from .HEVCConverter import HEVCConverter
from .PrettyPrinter import pretty_print, pretty_error


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

OUTPUT_DIR_NAME = "output"


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
        help='Photo files path',
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
    output_error = None
    args = parse_args(args)
    setup_logging(args.loglevel)
    current_path = args.path
    _logger.debug("Running tool on dir '%s'" % current_path)

    hevcconverter = HEVCConverter(current_path)
    pretty_print("Getting '%s' files list in directory '%s' ...\n" %
                 (HEVCConverter.XMP_EXTENSION, current_path))
    xmp_file_list = hevcconverter.all_xmp_files()
    for xmp_file in xmp_file_list:
        creation_date = hevcconverter.extract_creation_date_from_xmp_file(
            xmp_file)
        if creation_date:
            pretty_print("Detected file '{xmp_file}' with creation date '{creation_date}'".format(
                xmp_file=xmp_file, creation_date=creation_date))
        else:
            output_error = "There is a problem with '{xmp_file}'. Has not creation date!".format(
                xmp_file=xmp_file)
            break

    if len(xmp_file_list) > 0:
        input("Press Enter Key to continue or Ctrl-C to abort")
        pretty_print("Creating directory '%s' on current dir '%s'" %
                     (OUTPUT_DIR_NAME, current_path))
        hevcconverter.create_output_path(OUTPUT_DIR_NAME)
        print("------------------------------------")
        pretty_print("End process!. '%d' files has been proceseed! " %
                     (hevcconverter.run(xmp_file_list)))

    _logger.debug("Tool ends here with output error '%s'" % output_error)
    sys.exit(pretty_error(output_error)) if output_error else sys.exit(0)


def run():
    """Entry point for console_scripts
    """
    main(sys.argv[1:])


if __name__ == "__main__":
    run()
