# -*- coding -*-
"""
Provides some command utility functions.

TODO:
  matcher that ignores empty lines and whitespace and has contains comparison
"""

from __future__ import absolute_import, print_function

import os.path
import shutil
import sys
import tempfile
import time
from datetime import datetime
from fnmatch import fnmatch

from behave4cli import pathutil, textutil
from behave4cli.__setup import TOPA

# -----------------------------------------------------------------------------
# CONSTANTS:
# -----------------------------------------------------------------------------
# HERE    = os.path.dirname(__file__)
# TOP     = os.path.join(HERE, "..")
# TOPA    = os.path.abspath(TOP)
WORKDIR_NAME = "__WORKDIR__"


# -----------------------------------------------------------------------------
# UTILITY FUNCTIONS:
# -----------------------------------------------------------------------------
def workdir_save_coverage_files(workdir, destdir=None):
    assert os.path.isdir(workdir)
    if not destdir:
        destdir = TOPA
    if os.path.abspath(workdir) == os.path.abspath(destdir):
        return  # -- SKIP: Source directory is destination directory (SAME).

    for fname in os.listdir(workdir):
        if fnmatch(fname, ".coverage.*"):
            # -- MOVE COVERAGE FILES:
            sourcename = os.path.join(workdir, fname)
            shutil.move(sourcename, destdir)


# def ensure_directory_exists(dirname):
#     """
#     Ensures that a directory exits.
#     If it does not exist, it is automatically created.
#     """
#     if not os.path.exists(dirname):
#         os.makedirs(dirname)
#     assert os.path.exists(dirname)
#     assert os.path.isdir(dirname)


def ensure_context_attribute_exists(context, name, default_value=None):
    """
    Ensure a behave resource exists as attribute in the behave context.
    If this is not the case, the attribute is created by using the default_value.
    """
    if not hasattr(context, name):
        setattr(context, name, default_value)


def ensure_workdir_exists(context):
    """
    Ensures that the work directory exists.
    In addition, the location of the workdir is stored as attribute in
    the context object.
    """
    ensure_context_attribute_exists(context, "workdir", None)
    if not context.workdir:
        context.workdir = os.path.abspath(
            os.path.join(context._config.base_dir, "..", WORKDIR_NAME)
        )
    pathutil.ensure_directory_exists(context.workdir)


def ensure_workdir_not_exists(context):
    """Ensures that the work directory does not exist."""
    ensure_context_attribute_exists(context, "workdir", None)
    if context.workdir:
        orig_dirname = real_dirname = context.workdir
        context.workdir = None
        if os.path.exists(real_dirname):
            renamed_dirname = tempfile.mktemp(
                prefix=os.path.basename(real_dirname),
                suffix="_DEAD",
                dir=os.path.dirname(real_dirname) or ".",
            )
            os.rename(real_dirname, renamed_dirname)
            real_dirname = renamed_dirname
        max_iterations = 2
        if sys.platform.startswith("win"):
            max_iterations = 15

        for iteration in range(max_iterations):
            if not os.path.exists(real_dirname):
                if iteration > 1:
                    print("REMOVE-WORKDIR after %s iterations" % (iteration + 1))
                break
            shutil.rmtree(real_dirname, ignore_errors=True)
            time.sleep(0.5)
        assert not os.path.isdir(real_dirname), "ENSURE not-isa dir: %s" % real_dirname
        assert not os.path.exists(real_dirname), (
            "ENSURE dir not-exists: %s" % real_dirname
        )
        assert not os.path.isdir(orig_dirname), "ENSURE not-isa dir: %s" % orig_dirname


def template_substitute_builtin_expressions(context, text):
    expected_text = text
    expressions = {
        "__WORKDIR__": pathutil.posixpath_normpath(context.workdir),
        "__CWD__": pathutil.posixpath_normpath(os.getcwd()),
        "__TODAY_YYYY_MM_DD__": datetime.today().strftime("%Y-%m-%d"),
    }
    if any("{" + k + "}" in text for k in expressions.keys()):
        expected_text = textutil.template_substitute(text, **expressions)
    return expected_text


# def create_textfile_with_contents(filename, contents):
#     """
#     Creates a textual file with the provided contents in the workdir.
#     Overwrites an existing file.
#     """
#     ensure_directory_exists(os.path.dirname(filename))
#     if os.path.exists(filename):
#         os.remove(filename)
#     outstream = open(filename, "w")
#     outstream.write(contents)
#     if not contents.endswith("\n"):
#         outstream.write("\n")
#     outstream.flush()
#     outstream.close()
#     assert os.path.exists(filename)

# def text_remove_empty_lines(text):
#     """
#     Whitespace normalization:
#       - Strip empty lines
#       - Strip trailing whitespace
#     """
#     lines = [ line.rstrip()  for line in text.splitlines()  if line.strip() ]
#     return "\n".join(lines)
#
# def text_normalize(text):
#     """
#     Whitespace normalization:
#       - Strip empty lines
#       - Strip leading whitespace  in a line
#       - Strip trailing whitespace in a line
#       - Normalize line endings
#     """
#     lines = [ line.strip()  for line in text.splitlines()  if line.strip() ]
#     return "\n".join(lines)

# def posixpath_normpath(pathname):
#     """
#     Convert path into POSIX path:
#       - Normalize path
#       - Replace backslash with slash
#     """
#     backslash = '\\'
#     pathname = os.path.normpath(pathname)
#     if backslash in pathname:
#         pathname = pathname.replace(backslash, '/')
#     return pathname
