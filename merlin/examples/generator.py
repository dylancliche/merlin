###############################################################################
# Copyright (c) 2019, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory
# Written by the Merlin dev team, listed in the CONTRIBUTORS file.
# <merlin@llnl.gov>
#
# LLNL-CODE-797170
# All rights reserved.
# This file is part of Merlin, Version: 1.0.5.
#
# For details, see https://github.com/LLNL/merlin.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
###############################################################################

"""
This module contains a list of examples that can be used when learning to use
Merlin, or for setting up new workflows.
"""
import glob
import logging
import os
import shutil

import tabulate
import yaml

from merlin.examples import examples


LOG = logging.getLogger(__name__)

EXAMPLE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "workflows")


def gather_example_dirs():
    result = {}
    for d in os.listdir(EXAMPLE_DIR):
        result[d] = d
    return result


def gather_all_examples():
    specs = glob.glob(os.path.join(EXAMPLE_DIR, "") + "*/*.yaml")
    return specs


def write_example(src_path, dst_path):
    """
    Write out the example workflow to a file.
    :param src_path: The path to copy from.
    :param content: The formatted content to write the file to.
    """
    if os.path.isdir(src_path):
        shutil.copytree(src_path, dst_path)
    else:
        shutil.copy(src_path, dst_path)


def list_examples():
    """List all available examples."""
    examples = gather_example_dirs()

    headers = ["name", "description"]
    rows = []
    print(gather_all_examples())
    for example_dir in examples:
        directory = os.path.join(os.path.join(EXAMPLE_DIR, example_dir), "")
        specs = glob.glob(directory + "*.yaml")
        for spec in specs:
            with open(spec) as f:
                spec_metadata = yaml.safe_load(f)["description"]
            rows.append([spec_metadata["name"], spec_metadata["description"]])
    return "\n" + tabulate.tabulate(rows, headers) + "\n"


def setup_example(name, outdir):
    """Setup the given example."""
    try:
        example = gather_example_dirs()[name]
    except KeyError:
        LOG.error(f"Example '{name}' not found.")
        return None

    if outdir is None:
        outdir = os.getcwd()

    if example == "simple_chain":
        src_path = os.path.join(
            EXAMPLE_DIR, os.path.join("simple_chain", "simple_chain.yaml")
        )
    else:
        src_path = os.path.join(EXAMPLE_DIR, example)

        outdir = os.path.join(outdir, example)
        if os.path.exists(outdir):
            LOG.error(f"File '{outdir}' already exists!")
            return None

    LOG.info(f"Copying example '{name}' to {outdir}")
    write_example(src_path, outdir)
    return example
