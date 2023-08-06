#! /usr/bin/env python

##############################################################################
#  Based on DendroPy Phylogenetic Computing Library.
#
#  Copyright 2010 Jeet Sukumaran and Mark T. Holder.
#  All rights reserved.
#
#  See "LICENSE.txt" for terms and conditions of usage.
#
#  If you use this work or any portion thereof in published work,
#  please cite it as:
#
#     Sukumaran, J. and M. T. Holder. 2010. DendroPy: a Python library
#     for phylogenetic computing. Bioinformatics 26: 1569-1571.
#
##############################################################################

"""
Path mapping for various test resources.
"""
from peyutil import pretty_timestamp, write_as_json

try:
    import anyjson
except:
    import json


    class Wrapper(object):
        pass


    anyjson = Wrapper()
    anyjson.loads = json.loads
import codecs
import os

class PathMapForTests(object):
    def __init__(self, path_map_filepath):
        support_dir = os.path.dirname(path_map_filepath)
        self.tests_dir = os.path.join(support_dir, os.path.pardir)
        self.package_dir = os.path.join(self.tests_dir, os.path.pardir)
        self.scripts_dir = os.path.join(self.package_dir, os.path.pardir, "scripts")
        self.tests_data_dir = os.path.join(self.tests_dir, "data")
        self.tests_output_dir = os.path.join(self.tests_dir, "output")
        self.tests_scratch_dir = os.path.join(self.tests_dir, "scratch")


    def all_files(self, prefix):
        d = os.path.join(self.tests_data_dir, prefix)
        s = set()
        for p in os.listdir(d):
            fp = os.path.join(d, p)
            if os.path.isfile(fp):
                s.add(fp)
        return s


    def nexson_obj(self, filename):
        """Returns a dict that is the deserialized nexson object
        'filename' should be the fragment of the filepath below
        the nexson test dir.
        """
        with self.nexson_file_obj(filename) as fo:
            fc = fo.read()
            return anyjson.loads(fc)


    def nexson_file_obj(self, filename):
        """ Returns file object.
        'filename' should be the fragment of the filepath below
        the nexson test dir.
        """
        fp = self.nexson_source_path(filename=filename)
        return codecs.open(fp, mode='r', encoding='utf-8')


    def shared_test_dir(self):
        return os.path.join(self.tests_data_dir, "shared-api-tests")


    def nexson_source_path(self, filename=None):
        if filename is None:
            filename = ""
        return os.path.join(self.tests_data_dir, "nexson", filename)


    def nexml_source_path(self, filename=None):
        if filename is None:
            filename = ""
        return os.path.join(self.tests_data_dir, "nexml", filename)


    def named_output_stream(self, filename=None, suffix_timestamp=True):
        fp = self.named_output_path(filename=filename, suffix_timestamp=suffix_timestamp)
        return open(fp, "w")


    def named_output_path(self, filename=None, suffix_timestamp=True):
        if filename is None:
            filename = ""
        else:
            if isinstance(filename, list):
                filename = os.path.sep.join(filename)
            if suffix_timestamp:
                filename = "%s.%s" % (filename, pretty_timestamp(style=1))
        if not os.path.exists(self.tests_output_dir):
            os.makedirs(self.tests_output_dir)
        return os.path.join(self.tests_output_dir, filename)


    def script_source_path(self, filename=None):
        if filename is None:
            filename = ""
        return os.path.join(self.scripts_dir, filename)


    def next_unique_scratch_filepath(self, fn):
        frag = os.path.join(self.tests_scratch_dir, fn)
        if os.path.exists(self.tests_scratch_dir):
            if not os.path.isdir(self.tests_scratch_dir):
                mf = 'Cannot create temp file "{f}" because a file "{c}" is in the way'
                msg = mf.format(f=frag, c=self.tests_scratch_dir)
                raise RuntimeError(msg)
        else:
            os.makedirs(self.tests_scratch_dir)
        return self.next_unique_filepath(frag)


    def next_unique_filepath(self, fp):
        """Not thread safe.
        """
        if os.path.exists(fp):
            ind = 0
            while True:
                np = '{f}.{i:d}'.format(f=fp, i=ind)
                if not os.path.exists(np):
                    return np
                ind += 1
        return fp


    def json_source_path(self, filename=None):
        if filename is None:
            filename = ""
        return os.path.join(self.tests_data_dir, "json", filename)


    def collection_obj(self, filename):
        """Returns a dict that is the deserialized collection object
        'filename' should be the fragment of the filepath below
        the collection test dir.
        """
        with self.collection_file_obj(filename) as fo:
            fc = fo.read()
            return anyjson.loads(fc)


    def collection_file_obj(self, filename):
        """ Returns file object.
        'filename' should be the fragment of the filepath below
        the collection test dir.
        """
        fp = self.collection_source_path(filename=filename)
        return codecs.open(fp, mode='r', encoding='utf-8')


    def collection_source_path(self, filename=None):
        if filename is None:
            filename = ""
        return os.path.join(self.tests_data_dir, "collections", filename)


    def amendment_obj(self, filename):
        """Returns a dict that is the deserialized amendment object
        'filename' should be the fragment of the filepath below
        the amendment test dir.
        """
        with self.amendment_file_obj(filename) as fo:
            fc = fo.read()
            return anyjson.loads(fc)


    def amendment_file_obj(self, filename):
        """ Returns file object.
        'filename' should be the fragment of the filepath below
        the amendment test dir.
        """
        fp = self.amendment_source_path(filename=filename)
        return codecs.open(fp, mode='r', encoding='utf-8')


    def amendment_source_path(self, filename=None):
        if filename is None:
            filename = ""
        return os.path.join(self.tests_data_dir, "amendments", filename)

    def equal_blob_check(self, unit_test, diff_file_tag, first, second):
        if first != second:
            # dd = DictDiff.create(first, second)
            ofn = self.next_unique_scratch_filepath(diff_file_tag + '.obtained_rt')
            efn = self.next_unique_scratch_filepath(diff_file_tag + '.expected_rt')
            write_as_json(first, ofn)
            write_as_json(second, efn)
            # er = dd.edits_expr()
            if first != second:
                m_fmt = "Conversion failed see files {o} and {e}"
                m = m_fmt.format(o=ofn, e=efn)
                unit_test.assertEqual("", m)

def get_test_path_mapper():
    return PathMapForTests(path_map_filepath=__file__)

