#!/usr/bin/env python
# -*- coding: utf-8 -*-
###############################################################################
# @copyright Copyright (C) Guichet Entreprises - All Rights Reserved
# 	All Rights Reserved.
# 	Unauthorized copying of this file, via any medium is strictly prohibited
# 	Dissemination of this information or reproduction of this material
# 	is strictly forbidden unless prior written permission is obtained
# 	from Guichet Entreprises.
###############################################################################

import os
import sys
import logging
import ctypes
import argparse
import tempfile
import webbrowser

import pygenash.inoutstream as ios
import pygenash.template as template
import pygenash.core as core


###############################################################################
# test the filename for argparsing
#
# @param filename The filename
# @return filename.
###############################################################################
def is_real_file(filename):
    """
    'Type' for argparse - checks that file exists but does not open.
    """
    if not os.path.isfile(filename):
        # Argparse uses the ArgumentTypeError to give a rejection message like:
        # error: argument input: x does not exist
        raise argparse.ArgumentTypeError("{0} does not exist".format(filename))
    return filename

###############################################################################
# Create a windows message box
#
# @param text The message
# @param title The title of the windows
# @return nothing.
###############################################################################
def message_box(text, title):
    ctypes.windll.user32.MessageBoxW(0, text, title, 0)

###############################################################################
# Find the filename of this file (depend on the frozen or not)
# This function return the filename of this script.
# The function is complex for the frozen system
#
# @return the filename of THIS script.
###############################################################################
def __get_this_filename():
    result = ""
    if getattr(sys, 'frozen', False):
        # frozen
        result = sys.executable
    else:
        # unfrozen
        result = __file__
    return result


###############################################################################
# Find the filename of this file (depend on the frozen or not)
# This function return the filename of this script.
# The function is complex for the frozen system
#
# @return the folder of THIS script.
###############################################################################
def __get_this_folder():
    return os.path.split(os.path.abspath(os.path.realpath(
        __get_this_filename())))[0]


###############################################################################
# Logging system
###############################################################################
def __set_logging_system():
    log_filename = os.path.splitext(os.path.abspath(
        os.path.realpath(__get_this_filename())))[0] + '.log'

    if ios.is_frozen():
        log_filename = os.path.abspath(os.path.join(
            tempfile.gettempdir(),
            os.path.basename(__get_this_filename()) + '.log'))

    logging.basicConfig(filename=log_filename, level=logging.INFO,
                        format='%(asctime)s: %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p')
    console = logging.StreamHandler(ios.initial_stream().stdout)
    console.setLevel(logging.INFO)

    # set a format which is simpler for console use
    formatter = logging.Formatter('%(asctime)s: %(levelname)-8s %(message)s')
    # tell the handler to use this format
    console.setFormatter(formatter)
    # add the handler to the root logger

    # if not ios.is_frozen():
    logging.getLogger('').addHandler(console)

    return console


###############################################################################
# Find the filename of this file (depend on the frozen or not)
###############################################################################
def get_this_filename():
    result = ""
    if getattr(sys, 'frozen', False):
        # frozen
        result = sys.executable
    else:
        # unfrozen
        result = __file__
    return result


###############################################################################
# Define the parsing of arguments of the command line
###############################################################################
def get_parser_for_command_line():
    description_arg = "This program apply a template for a standalone form"

    parser = argparse.ArgumentParser(description=description_arg)
    parser.add_argument('--windows',
                        action='store_true', dest='windows',
                        help='Define if we need all popups windows.')
    parser.add_argument('--verbose',
                        action='store_true', dest='verbose',
                        help='Put the logging system on the console for info.')
    parser.add_argument('--console', action='store_true', dest='console',
                        help='Set the output to the standard output '
                        'for console')

    parser.add_argument('--conf', dest="conf_filename", required=True,
                        type=is_real_file, metavar="FILE",
                        help="The yaml file with all parameter")

    parser.add_argument('--output', dest="output", required=True,
                        metavar="FILE",
                        help="The output folder name")

    parser.add_argument('--overwrite', action='store', dest='overwrite',
                        choices=['yes', 'no'], default='no',
                        help='Overwrite option')

    return parser

###############################################################################
# Logging system
###############################################################################
def __set_logging_system():
    log_filename = os.path.splitext(os.path.abspath(
        os.path.realpath(__get_this_filename())))[0] + '.log'

    if ios.is_frozen():
        log_filename = os.path.abspath(os.path.join(
            tempfile.gettempdir(),
            os.path.basename(__get_this_filename()) + '.log'))

    logging.basicConfig(filename=log_filename, level=logging.INFO,
                        format='%(asctime)s: %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p')
    console = logging.StreamHandler(ios.initial_stream().stdout)
    console.setLevel(logging.INFO)

    # set a format which is simpler for console use
    formatter = logging.Formatter('%(asctime)s: %(levelname)-8s %(message)s')
    # tell the handler to use this format
    console.setFormatter(formatter)
    # add the handler to the root logger

    # if not xe2.inoutstream.is_frozen():
    logging.getLogger('').addHandler(console)

    return console

###############################################################################
# Main script
###############################################################################
def __main():
    console = __set_logging_system()
    # ------------------------------------
    logging.info('+')
    logging.info('-------------------------------------------------------->>')
    logging.info('Started %s', __get_this_filename())
    logging.info('The Python version is %s.%s.%s',
                 sys.version_info[0], sys.version_info[1], sys.version_info[2])

    try:
        parser = get_parser_for_command_line()
        logging.info("parsing args")
        args = parser.parse_args()
        logging.info("parsing done")

        if args.verbose == "yes":
            console.setLevel(logging.INFO)
        if args.console == "yes":
            ios.initial_stream().apply_to_std_stream()
            if ios.is_frozen():
                logging.getLogger('').addHandler(console)

        logging.info("windows=%s", args.windows)
        logging.info("console=%s", args.console)
        logging.info("verbose=%s", args.verbose)

        logging.info("conf_filename=%s", args.conf_filename)
        logging.info("output=%s", args.output)
        logging.info("overwrite=%s", args.overwrite)

        template.generate(args.conf_filename, args.output,
                          overwrite=args.overwrite)

    except argparse.ArgumentError as errmsg:
        logging.error(str(errmsg))
        if 'args' in locals() and args.windows:
            message_box(text=parser.format_usage(), title='Usage')

    except SystemExit:
        logging.error("Exit")
        if 'args' in locals() and args.windows:
            message_box(text=parser.format_help(), title='Help')

    except BaseException as ex:
        logging.error(str(ex))
        if 'args' in locals() and args.windows:
            message_box(text=str(ex), title='Usage')

    logging.info('Finished')
    logging.info('<<--------------------------------------------------------')
    logging.info('+')


###############################################################################
# Call main if the script is main
###############################################################################
if __name__ == '__main__':
    __main()
