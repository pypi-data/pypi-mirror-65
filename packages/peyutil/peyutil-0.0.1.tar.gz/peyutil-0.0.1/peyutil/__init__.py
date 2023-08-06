#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Simple utility functions that do not depend on any other part of
peyotl, but are used by packages that descend from peyotl
"""
from __future__ import absolute_import, print_function, division
__version__ = '0.0.1'  # sync with setup.py
import time
import os

__all__ = ['input_output', 'str_util', 'dict_wrapper', 'test', 'tokenizer']


def any_early_exit(iterable, predicate):
    """Tests each element in iterable by calling predicate(element). Returns True on first True, or False."""
    for i in iterable:
        if predicate(i):
            return True
    return False


def pretty_timestamp(t=None, style=0):
    """time formatter used in peyotl test reporting Y-m-d if style is 0, YmdHMS"""
    if t is None:
        t = time.localtime()
    if style == 0:
        return time.strftime("%Y-%m-%d", t)
    return time.strftime("%Y%m%d%H%M%S", t)


def doi2url(v):
    if v.startswith('http'):
        return v
    if v.startswith('doi:'):
        if v.startswith('doi: '):
            v = v[5:]  # trim 'doi: '
        else:
            v = v[4:]  # trim 'doi:'
    if v.startswith('10.'):  # it's a DOI!
        return 'http://dx.doi.org/' + v
    # convert anything else to URL and hope for the best
    return 'http://' + v


def get_unique_filepath(stem):
    """NOT thread-safe!
    return stems or stem# where # is the smallest
    positive integer for which the path does not exist.
    useful for temp dirs where the client code wants an
    obvious ordering.
    """
    fp = stem
    if os.path.exists(stem):
        n = 1
        fp = stem + str(n)
        while os.path.exists(fp):
            n += 1
            fp = stem + str(n)
    return fp


def propinquity_fn_to_study_tree(inp_fn, strip_extension=True):
    """This should only be called by propinquity - other code should be treating theses
    filenames (and the keys that are based on them) as opaque strings.

    Takes a filename (or key if strip_extension is False), returns (study_id, tree_id)

    propinquity provides a map to look up the study ID and tree ID (and git SHA)
    from these strings.
    """
    if strip_extension:
        study_tree = '.'.join(inp_fn.split('.')[:-1])  # strip extension
    else:
        study_tree = inp_fn
    x = study_tree.split('@')
    if len(x) != 2:
        msg = 'Currently we are expecting studyID@treeID.<file extension> format. Expected exactly 1 @ in the filename. Got "{}"'
        msg = msg.format(study_tree)
        raise ValueError(msg)
    return x

# Make the following names visible to client code using "from peyutil import ..."
# noinspection PyPep8
from .input_output import (download,
                           expand_path,
                           open_for_group_write,
                           parse_study_tree_list,
                           read_as_json,
                           write_to_filepath, write_as_json)

# noinspection PyPep8
from .str_util import (flush_utf_8_writer,
                       get_utf_8_string_io_writer,
                       increment_slug, is_int_type, is_str_type,
                       primitive_string_types,
                       reverse_dict,
                       slugify, StringIO,
                       underscored2camel_case,
                       UNICODE,
                       urlencode)

# noinspection PyPep8
from .tokenizer import (NewickEventFactory, NewickEvents,
                        NewickTokenizer, NewickTokenType)
