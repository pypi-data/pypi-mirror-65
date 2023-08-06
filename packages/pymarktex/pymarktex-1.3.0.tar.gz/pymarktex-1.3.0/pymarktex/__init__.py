#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Special variables #
__version__ = '1.3.0'

# Built-in modules #
import os, sys, re, shutil, codecs, importlib

# Internal modules #
import pymarktex.templates.sinclair_bio

# First party modules #
from autopaths import Path
from autopaths.tmp_path import new_temp_dir

# Third party modules #
import pbs3

# Get paths to module #
self       = sys.modules[__name__]
module_dir = Path(os.path.dirname(self.__file__))

# The repository directory #
repos_dir = module_dir.directory

# Various paths #
logo_dir = repos_dir + 'logos/'

###############################################################################
class Document(object):
    """The main object is the document to be generated from markdown text."""

    def __repr__(self): return '<%s object on %s>' % (self.__class__.__name__, self.parent)

    def __init__(self, input_path, output_path=None, builtin_template=None):
        # Input #
        self.input_path = Path(input_path)
        # Output #
        if output_path is None: self.output_path = self.default_output_name
        else:                   self.output_path = Path(output_path)
        # Templates builtin #
        if builtin_template:
            subpackage = importlib.import_module('pymarktex.templates.' + builtin_template)
            self.header_template = subpackage.HeaderTemplate
            self.footer_template = subpackage.FooterTemplate

    def __call__(self): return self.generate()

    def generate(self):
        # Main steps #
        self.load_markdown()
        self.make_body()
        self.make_latex()
        self.make_pdf()
        # For convenience #
        return self.output_path

    @property
    def default_options(self):
        return {
            'name':        os.environ.get('USER_FULL_NAME'),
            'status':      os.environ.get('USER_STATUS'),
            'company':     os.environ.get('USER_COMPANY'),
            'subcompany':  os.environ.get('USER_SUBCOMPANY'),
            'title':       "Auto-generated report",
            'image_path':  logo_dir + 'logo.png',
        }

    @property
    def default_output_name(self):
        return Path(os.path.splitext(self.input_path)[0] + '.pdf')

    def load_markdown(self):
        """Load file in memory and separate the options and body."""
        # Read the file #
        self.input_path.must_exist()
        self.input = self.input_path.contents_utf8
        # Separate the top params and the rest of the markdown #
        find_results = re.findall(r'\A---(.+?)---(.+)', self.input, re.M|re.DOTALL)
        # We did not find any parameters #
        if not find_results:
            self.params = {}
            self.markdown = self.input
            return
        # We did find a set of parameters #
        self.params, self.markdown = find_results[0]
        self.params = [i.partition(':')[::2] for i in self.params.strip().split('\n')]
        self.params = dict([(k.strip(),v.strip()) for k,v in self.params])

    def make_body(self):
        """Convert the body to LaTeX."""
        kwargs = dict(_in=self.markdown, read='markdown', write='latex')
        self.body = pbs3.Command('pandoc')(**kwargs).stdout

    # Default templates #
    header_template = pymarktex.templates.sinclair_bio.HeaderTemplate
    footer_template = pymarktex.templates.sinclair_bio.FooterTemplate

    def make_latex(self, params=None, header=None, footer=None):
        """Add the header and footer."""
        # Copy the options #
        options = self.default_options.copy()
        if params: options.update(params)
        if hasattr(self, 'params'): options.update(self.params)
        # Header and Footer #
        self.header = self.header_template(options) if header is None else header
        self.footer = self.footer_template()        if footer is None else footer
        self.latex = str(self.header) + self.body + str(self.footer)

    def make_pdf(self, safe=False, include_src=False):
        """Call XeLaTeX (twice for cross-referencing)"""
        # Paths #
        self.tmp_dir    = new_temp_dir()
        self.tmp_path   = Path(self.tmp_dir + 'main.tex')
        self.tmp_stdout = Path(self.tmp_dir + 'stdout.txt')
        self.tmp_stderr = Path(self.tmp_dir + 'stderr.txt')
        self.tmp_log    = Path(self.tmp_dir + 'main.log')
        # Prepare #
        with codecs.open(self.tmp_path, 'w', encoding='utf8') as handle: handle.write(self.latex)
        self.cmd_params  = ["--interaction=nonstopmode", '-output-directory']
        self.cmd_params += [self.tmp_dir, self.tmp_path]
        # Call twice for references #
        self.call_xelatex(safe)
        self.call_xelatex(safe)
        # Check output directory exists #
        self.output_path.directory.create_if_not_exists()
        # Move into place #
        shutil.move(self.tmp_dir + 'main.pdf', self.output_path)
        # Show the latex source #
        if include_src: self.output_path.replace_extension('tex').write(self.latex, encoding='utf-8')

    def call_xelatex(self, safe=False):
        """
        Here we use the `pbs3` library under Windows and the sh` library under Unix.
        There is a cross-compatible library called `plumbum` but has an awkward syntax:

            cmd = plumbum.local['xelatex']
            ((cmd > self.tmp_stderr) >= self.tmp_stdout)()

        See https://github.com/tomerfiliba/plumbum/issues/441
        """
        if os.name == "posix":  cmd = pbs3.Command('xelatex')
        if os.name == "nt":     cmd = pbs3.Command('xelatex.exe')
        try:
            cmd(*self.cmd_params,
                _ok_code=[0] if not safe else [0,1],
                _err=str(self.tmp_stderr),
                _out=str(self.tmp_stdout))
        except pbs3.ErrorReturnCode_1:
            print('-' * 60)
            print("Xelatex exited with return code 1.")
            if self.tmp_stdout.exists:
                print("Here is the tail of the stdout at '%s':" % self.tmp_stdout.unix_style)
                print(self.tmp_stdout.pretty_tail)
            elif self.tmp_log.exists:
                print("Here is the tail of the log at '%s':" % self.tmp_log.unix_style)
                print(self.tmp_log.pretty_tail)
            print('-' * 60)
            raise

    def copy_to_outbox(self):
        """Copy the report to the outbox directory where it can be viewed by anyone."""
        self.outbox.directory.create(safe=True)
        shutil.copy(self.output_path, self.outbox)

    def purge_cache(self):
        """Some reports used pickled properties to avoid recalculations."""
        if not hasattr(self, 'cache_dir'): raise Exception("No cache directory to purge.")
        self.cache_dir.remove()
        self.cache_dir.create()