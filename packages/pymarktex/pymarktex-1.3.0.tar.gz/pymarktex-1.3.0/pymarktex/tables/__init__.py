# Futures #
from __future__ import division

# Built-in modules #

# Internal modules #
from pymarktex.templates import Template

# First party modules #
from autopaths import Path

# Third party modules #

###############################################################################
class LatexTable(Template):
    """
    A table in latex code which can have its caption adjusted.
    For instance you can adjust the caption like this:

        >>> from pymarktex.tables import LatexTable
        >>> return LatexTable(path='~/all_values.tex', caption='Lorem')
    """

    def abs_path(self): return self.path.unix_style

    def __init__(self, path    = None,
                       caption = None,
                       label   = None,
                       table   = None,
                       **kwargs):
        # Check inputs #
        if path is None and table is None:
            raise Exception("You need to specify a table or a path.")
        # Path #
        if path is not None:    self.path = Path(path)
        else:                   self.path = table.path
        # Caption #
        if caption is not None: self.caption = caption
        else:                   self.caption = ''
        if table is not None and hasattr(table, 'caption'): self.caption = table.caption
        # Label #
        if   label is not None: self.label = r"\label{" + label + "}\n"
        elif table is not None: self.label = r"\label{" + table.short_name + "}\n"
        else:                   self.label = ''
        # Graph #
        if table is not None:   self.table = table
        # Keyword arguments #
        self.kwargs = kwargs
        # Call the graph if it's not generated #
        if table is not None and not table: table.save()
        # Check the file was created #
        if not self.path.exists: raise Exception("No file at '%s'." % self.path)