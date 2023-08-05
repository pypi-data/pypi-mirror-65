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
import sys
import os
import os.path
import logging
import codecs
from shutil import copyfile
import yaml
import jinja2


from . import core


# -----------------------------------------------------------------------------
def std_folder():
    """ Standard template forlder
    @return the template folder standard of the package
    """
    return core.check_folder(os.path.join(__get_this_folder(), "templates"))

# -----------------------------------------------------------------------------
def generate_file(input_filename, output_filename, context, overwrite):
    logging.debug("input=%s --> output=%s", input_filename, output_filename)
    if os.path.isfile(output_filename) and not overwrite:
        logging.error("Can not write the file %s", output_filename)
        return

    if core.is_binary_file(input_filename):
        logging.debug("Write the binary file %s", output_filename)
        copyfile(input_filename, output_filename)
        return

    content = jinja2.Template(core.get_file_content(input_filename))
    logging.debug("Write the file %s", output_filename)
    core.set_file_content(output_filename, content.render(context))


# -----------------------------------------------------------------------------
def generate(conf_filename, output, template_name=None,
             template_folder=None, overwrite=True):
    """Generate a stand alone form for Nash

    Arguments:
        conf_filename {string} -- filename of the yaml conf
        output {string} -- path to the output folder

    Keyword Arguments:
        template_name {string} -- name of the template
                                it could be inside the conf also
                                    (default: {None})
        template_folder {string} -- folder to pick up the template
                                (default: {None})
        overwrite {bool} -- overwrite existing files
                                (default: {True})
    """

    logging.info(" -- > Generate template template_name=%s conf=%s "
                 "template_folder=%s output=%s",
                 template_name, conf_filename, template_folder, output)

    conf_filename = core.check_is_file_and_correct_path(conf_filename)
    logging.debug(" read conf=%s", conf_filename)
    with codecs.open(conf_filename, "r", "utf-8") as ymlfile:
        conf_yaml = yaml.load(ymlfile, Loader=yaml.FullLoader)

    if template_name is None:
        template_name = conf_yaml['template_name']

    if template_folder is None:
        template_folder = std_folder()
    template_folder = os.path.join(template_folder, template_name)
    template_folder = core.check_folder(template_folder)

    output = core.set_correct_path(output)
    output = os.path.join(output, conf_yaml['description']['name'])
    
    if os.path.isdir(output) and not overwrite:
        logging.error("Destination folder already exist %s", output)
        raise Exception("Destination folder already exist %s" % output)

    logging.debug(" correct output=%s", output)
    core.check_create_folder(output)

    for root, unused_dirs, files in os.walk(template_folder):
        for filename in files:
            input_filename = os.path.join(root, filename)
            output_filename = os.path.join(
                output, os.path.relpath(input_filename, template_folder))
            if os.path.splitext(output_filename)[1].lower() == ".j2":
                output_filename = os.path.splitext(output_filename)[0]

            generate_file(input_filename, output_filename,
                          conf_yaml, overwrite)

    logging.info(" -- > End of the template generation")


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
