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
import sys
import os
import os.path
import codecs
from copy import deepcopy
import yaml
import networkx as nx
import pydot
import jinja2

from . import core

# -----------------------------------------------------------------------------
def dot_folder():
    """ Standard template forlder
    @return the template folder standard of the package
    """
    return core.check_folder(os.path.join(__get_this_folder(), "dot_render"))

# -----------------------------------------------------------------------------
# Apply function to every files in folder
#
# @param folder	The folder to scan
# @param process The function to pally to each file the function take one
#                parameter (the filename)
# @param filename_ext The file extension (markdown for the default)
# -----------------------------------------------------------------------------
def apply_function_in_folder(folder, process, filename_ext=".md"):
    for root, unused_dirs, files in os.walk(folder):
        for filename in files:
            if os.path.join(root, filename).endswith(filename_ext):
                process(os.path.join(root, filename))


# -----------------------------------------------------------------------------
# 	Analyse a bunch of yaml
# -----------------------------------------------------------------------------
def _analyse_file(yml_filename, data):
    filename = core.set_correct_path(yml_filename)
    logging.info("Analyse file %s", filename)
    with codecs.open(filename, "r", "utf-8") as ymlfile:
        yml_data = yaml.load(ymlfile, Loader=yaml.FullLoader)

    if 'description' not in yml_data \
            or 'name' not in yml_data['description']:
        return data

    node_name = yml_data['description']['name']
    if node_name not in data.nodes:
        logging.info("   Add node %s", node_name)
        data.add_node(node_name, data=yml_data)
    else:
        data.nodes[node_name]['data'] = yml_data

    if 'display' not in yml_data \
            or 'choice' not in yml_data['display']:
        return data

    for item in yml_data['display']['choice']:
        if 'target' not in item:
            continue
        target = item['target']
        if 'nash_target' in item:
            target = item['nash_target'] + "/" + target
        data.add_edge(node_name, target, data=item)

    return data


# -----------------------------------------------------------------------------
# 	Analyse a bunch of yaml
# -----------------------------------------------------------------------------
def analyse(yml_filename):
    yml_filename = core.set_correct_path(yml_filename)
    logging.info("Analyse file %s", yml_filename)
    yml_folder = os.path.dirname(yml_filename)

    # find all files to analyse
    files = []

    def add_yml(x): return files.append(x)
    apply_function_in_folder(yml_folder, add_yml, filename_ext=".yml")

    data = nx.DiGraph()
    for filename in files:
        _analyse_file(filename, data)

    return data

# -----------------------------------------------------------------------------
# 	Draw graph node label
# -----------------------------------------------------------------------------
def create_node_label(data):
    input_filename = os.path.join(dot_folder(), "box.html.j2")
    content = jinja2.Template(core.get_file_content(input_filename))
    return content.render(data)

# -----------------------------------------------------------------------------
# 	Draw graph node
# -----------------------------------------------------------------------------
def create_node(node_id, node):
    if node_id.startswith("nash.web"):
        return pydot.Node(name=node_id, rank="max", shape="box",
                          fixedsize=True,
                          fontname="Arial", fontsize=8,
                          style="filled,setlinewidth(0)",
                          fillcolor="#e53138", fontcolor="#ffffff",
                          margin=10, width=7)

    rank = node_id.count('/')
    if 'data' in node:
        label = ""
        label = create_node_label(node['data'])
    else:
        logging.error("node_id=%s pas de data" % node_id)
        label = ""

    result = pydot.Node(name=node_id, rank=rank,
                        shape="box",
                        label=label,
                        fixedsize=True,  # width=2,
                        fontname="Arial", fontsize=8,
                        style="filled,setlinewidth(0)",
                        fillcolor="#e53138",
                        fontcolor="#ffffff",
                        margin=0, width=3)
    return result

# -----------------------------------------------------------------------------
# 	Draw graph node
# -----------------------------------------------------------------------------
def create_edge(src, dest, edge):
    data = edge['data']
    result = pydot.Edge(src=src, dst=dest,
                        label=data['text'],
                        fontname="Arial", fontsize=8,
                        arrowsize=2,
                        style="setlinewidth(2)",
                        color="#848687",
                        )

    return result

# -----------------------------------------------------------------------------
# 	Create graph from analyse
# -----------------------------------------------------------------------------
def to_graph(data):
    site = pydot.Dot(graph_type='digraph',
                     fontname="Arial",
                     compound='true', size="2000",
                     #  splines="curved",
                     overlap="prism",
                     rankdir="LR",
                     splines="ortho")

    external = pydot.Cluster('ext', label='Forms',
                             fontname="Arial", style="bold",
                             fontcolor="#848687", color="#848687")

    # profiler = pydot.Cluster('profiler', label='Profiler',
    #                          fontname="Arial", style="bold",
    #                          fontcolor="#848687", color="#848687")

    # site.add_subgraph(profiler)
    site.add_subgraph(external)

    count = 0
    count_max = len(data.nodes)
    for node_id in data.nodes:
        count += 1
        logging.info("%04d/%04d : Create node %s", count, count_max,
                     node_id)
        if node_id.startswith("nash.web"):
            external.add_node(create_node(node_id, data.nodes[node_id]))
        else:
            site.add_node(create_node(node_id, data.nodes[node_id]))

    count = 0
    count_max = len(data.edges)
    for edge_id in data.edges:
        count += 1
        logging.info("%04d/%04d : Create edge %s", count, count_max,
                     edge_id)
        site.add_edge(create_edge(edge_id[0], edge_id[1], data.edges[edge_id]))

    return site


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
