#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Third party modules #
import pystache

###############################################################################
class Template(object):
    """The template base class."""

    delimiters     = (u'@@[', u']@@')
    escape         = lambda s: lambda u: u # Needed otherwise celled with self
    search_dirs    = None
    str_encoding   = 'utf8'
    file_encoding  = 'utf8'

    def __repr__(self): return '<%s object on %s>' % (self.__class__.__name__, self.parent)
    def __str__(self):  return self.render()

    def __init__(self, options=None):
        self.options = options if options else {}

    def render(self, escape=None, search_dirs=None, delimiters=None, str_encoding=None, file_encoding=None):
        # Options #
        delimiters    = self.delimiters    if delimiters is None    else delimiters
        escape        = self.escape        if escape is None        else escape
        search_dirs   = self.search_dirs   if search_dirs is None   else search_dirs
        str_encoding  = self.str_encoding  if str_encoding is None  else str_encoding
        file_encoding = self.file_encoding if file_encoding is None else file_encoding
        # The delimiters are in the defaults #
        pystache.defaults.DELIMITERS = delimiters
        # Create renderer #
        renderer = pystache.Renderer(escape          = escape(),
                                     search_dirs     = search_dirs,
                                     string_encoding = str_encoding,
                                     file_encoding   = file_encoding)
        # Call render #
        return renderer.render(self)