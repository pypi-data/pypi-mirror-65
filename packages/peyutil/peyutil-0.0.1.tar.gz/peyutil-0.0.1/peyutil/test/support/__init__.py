#! /usr/bin/env python
from .struct_diff import DictDiff

def raise_http_error_with_more_detail(err):
    # show more useful information (JSON payload) from the server
    details = err.response.text
    raise ValueError("{e}, details: {m}".format(e=err, m=details))


__all__ = ['helper', 'pathmap', 'struct_diff']