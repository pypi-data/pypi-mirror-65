#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# @copyright Copyright (C) Guichet Entreprises - All Rights Reserved
# 	All Rights Reserved.
# 	Unauthorized copying of this file, via any medium is strictly prohibited
# 	Dissemination of this information or reproduction of this material
# 	is strictly forbidden unless prior written permission is obtained
# 	from Guichet Entreprises.
# -----------------------------------------------------------------------------
import logging
import os
import os.path
import codecs

# ###############################################################################
# # Cool logo (or maybe cool logo, ascii one anyway)
# ###############################################################################
# __logo__ = r"""
#         _   __           __
#        / | / /___ ______/ /_
#       /  |/ / __ `/ ___/ __ \
#      / /|  / /_/ (__  ) / / /
#     /_/ |_/\__,_/____/_/ /_/

# """


###############################################################################
# Retrive the correct complet path
# This function return a folder or filename with a standard way of writing.
#
# @param folder_or_file_name the folder or file name
# @return the folder or filename normalized.
###############################################################################
def set_correct_path(folder_or_file_name):
    return os.path.abspath(folder_or_file_name)


###############################################################################
# Test a folder
# Test if the folder exist.
#
# @exception RuntimeError if the name is a file or not a folder
#
# @param folder the folder name
# @return the folder normalized.
###############################################################################
def check_folder(folder):
    if os.path.isfile(folder):
        logging.error('%s can not be a folder (it is a file)', folder)
        raise RuntimeError('%s can not be a folder (it is a file)' % folder)

    if not os.path.isdir(folder):
        logging.error('%s is not a folder', folder)
        raise RuntimeError('%s is not a folder' % folder)

    return set_correct_path(folder)


###############################################################################
# Test a folder
# test if the folder exist and create it if possible and necessary.
#
# @exception RuntimeError if the name is a file
#
# @param folder the folder name
# @return the folder normalized.
###############################################################################
def check_create_folder(folder):
    if os.path.isfile(folder):
        logging.error('%s can not be a folder (it is a file)', folder)
        raise RuntimeError('%s can not be a folder (it is a file)' % folder)

    if not os.path.isdir(folder):
        os.makedirs(folder, exist_ok=True)

    return set_correct_path(folder)

###############################################################################
# test if this is a file and correct the path
#
# @exception RuntimeError if the name is not a file or if the extension
#                         is not correct
#
# @param filename the file name
# @param filename_ext the file name extension like ".ext" or ".md"
# @return the filename normalized.
###############################################################################
def check_is_file_and_correct_path(filename, filename_ext=None):
    filename = set_correct_path(filename)

    if not os.path.isfile(filename):
        logging.error('"%s" is not a file', (filename))
        raise Exception('"%s" is not a file' % (filename))

    current_ext = os.path.splitext(filename)[1]
    if (filename_ext is not None) and (current_ext != filename_ext):

        raise Exception('The extension of the file %s '
                        'is %s and not %s as expected.' % (
                            filename, current_ext, filename_ext))

    return filename


#: BOMs to indicate that a file is a text file even if it contains zero bytes.
_TEXT_BOMS = (
    codecs.BOM_UTF16_BE,
    codecs.BOM_UTF16_LE,
    codecs.BOM_UTF32_BE,
    codecs.BOM_UTF32_LE,
    codecs.BOM_UTF8,
)


def is_binary_file(source_path):
    with open(source_path, 'rb') as source_file:
        initial_bytes = source_file.read(8192)
    return not any(initial_bytes.startswith(bom) for bom in _TEXT_BOMS)\
        and b'\0' in initial_bytes


###############################################################################
# Get the content of a file. This function delete the BOM.
#
# @param filename the file name
# @param encoding the encoding of the file
# @return the content
###############################################################################
def get_file_content(filename, encoding="utf-8"):
    logging.debug('Get content of the filename %s', (filename))
    filename = check_is_file_and_correct_path(filename)

    # Read the file
    input_file = codecs.open(filename, mode="r", encoding=encoding)
    try:
        content = input_file.read()
    except UnicodeDecodeError as err:
        raise IOError("%s\nCannot read the file %s" % (str(err),
                                                       filename))
    input_file.close()

    if content.startswith(u'\ufeff'):
        content = content[1:]

    return content

###############################################################################
# Set the content of a file. This function create a BOM in the UTF-8 encoding.
# This function create the file or overwrite the file.
#
# @param filename the file name
# @param content the content
# @param encoding the encoding of the file
# @param bom the bit order mark at the beginning of the file
# @return filename corrected
###############################################################################
def set_file_content(filename, content, encoding="utf-8", bom=True):
    logging.debug('Set content of the filename %s', (filename))
    filename = set_correct_path(filename)

    output_file = codecs.open(filename, "w", encoding=encoding)

    if bom and (not content.startswith(u'\ufeff')) and \
            (encoding == "utf-8"):
        output_file.write(u'\ufeff')

    output_file.write(content)
    output_file.close()

    return filename
