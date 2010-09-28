# -*- coding: utf-8 -*-
#
# NumPy documentation build configuration file, created by
# sphinx-quickstart on Wed May  7 09:45:59 2008.
#
# This file is execfile()d with the current directory set to its containing dir.
#
# The contents of this file are pickled, so don't put values in the namespace
# that aren't pickleable (module imports are okay, they're removed automatically).
#
# All configuration values have a default value; values that are commented out
# serve to show the default value.

import sys, os
from scikits.timeseries import __version__ as ts_version

# If your extensions are in another directory, add it here. If the directory
# is relative to the documentation root, use os.path.abspath to make it
# absolute, like shown here.
sys.path.extend([

    # numpy standard doc extensions
    os.path.join(os.path.dirname(__file__), '..', 'sphinxext'),

    # timeseries specific doc extensions
    os.path.join(os.path.dirname(__file__), '..', 'sphinxext_ts')
])


# Check Sphinx version
import sphinx
if sphinx.__version__ < "0.6":
    raise RuntimeError("Sphinx 0.6 or newer required")



# General configuration
# ---------------------

# Add any Sphinx extension module names here, as strings. They can be extensions
# coming with Sphinx (named 'sphinx.ext.*') or your custom ones.
extensions = ['sphinx.ext.autodoc', 'sphinx.ext.autosummary',
              'sphinx.ext.coverage', 'sphinx.ext.intersphinx',
              'sphinx.ext.pngmath', 
              'numpydoc', 'phantom_import', 'tsplot_directive']

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix of source filenames.
source_suffix = '.rst'

# The master toctree document.
master_doc = 'contents'

# General substitutions.
project = 'TimeSeries'
copyright = '2008, Pierre GERARD-MARCHANT, Matt KNOX'

# The default replacements for |version| and |release|, also used in various
# other places throughout the built documents.
#
# The short X.Y version.
version = ts_version

# There are two options for replacing |today|: either, you set today to some
# non-false value, then it is used:
#today = ''
# Else, today_fmt is used as the format for a strftime call.
today_fmt = '%B %d, %Y'

# List of documents that shouldn't be included in the build.
#unused_docs = []

# The reST default role (used for this markup: `text`) to use for all documents.
default_role = "autolink"

# List of directories, relative to source directories, that shouldn't be searched
# for source files.
exclude_dirs = []

# If true, '()' will be appended to :func: etc. cross-reference text.
add_function_parentheses = False

# If true, the current module name will be prepended to all description
# unit titles (such as .. function::).
add_module_names = False

# If true, sectionauthor and moduleauthor directives will be shown in the
# output. They are ignored by default.
#show_authors = False

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'


# Options for HTML output
# -----------------------

# The style sheet to use for HTML and HTML Help pages. A file of that name
# must exist either in Sphinx' static/ path, or in one of the custom paths
# given in html_static_path.
html_style = 'timeseries.css'

# The name for this set of Sphinx documents.  If None, it defaults to
# "<project> v<release> documentation".
html_title = "%s v%s Reference Guide" % (project, version)

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# If not '', a 'Last updated on:' timestamp is inserted at every page bottom,
# using the given strftime format.
html_last_updated_fmt = '%b %d, %Y'

# If true, SmartyPants will be used to convert quotes and dashes to
# typographically correct entities.
#html_use_smartypants = True

# Content template for the index page.
html_index = 'index.html'

# Custom sidebar templates, maps document names to template names.
html_sidebars = {'index': 'indexsidebar.html'}

# Additional templates that should be rendered to pages, maps page names to
# template names.
html_additional_pages = {'index': 'index.html'}

# If false, no module index is generated.
html_use_modindex = True

# If true, the reST sources are included in the HTML build as _sources/<name>.
#html_copy_source = True

# If true, an OpenSearch description file will be output, and all pages will
# contain a <link> tag referring to it.  The value of this option must be the
# base URL from which the finished HTML is served.
#html_use_opensearch = ''

# If nonempty, this is the file name suffix for HTML files (e.g. ".xhtml").
#html_file_suffix = '.xhtml'

# Output file base name for HTML help builder.
htmlhelp_basename = 'TimeSeriesDoc'

# Pngmath should try to align formulas properly
pngmath_use_preview = True


# Options for LaTeX output
# ------------------------

# The paper size ('letter' or 'a4').
#latex_paper_size = 'letter'

# The font size ('10pt', '11pt' or '12pt').
#latex_font_size = '10pt'

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title, author, document class [howto/manual]).
_stdauthor = u"Written by Pierre Gérard-Marchant and Matt Knox"
latex_documents = [
  ('index', 'TimeSeries.tex', 'TimeSeries Reference Guide',
   _stdauthor, 'manual'),
]

# The name of an image file (relative to this directory) to place at the top of
# the title page.
#latex_logo = None

# For "manual" documents, if this is true, then toplevel headings are parts,
# not chapters.
#latex_use_parts = False

# Additional stuff for the LaTeX preamble.
latex_preamble = r'''
\usepackage{ucs}
\usepackage{amsmath}

% In the parameters section, place a newline after the Parameters
% header
\usepackage{expdlist}
\let\latexdescription=\description
\def\description{\latexdescription{}{} \breaklabel}

% Make Examples/etc section headers smaller and more compact
\makeatletter
\titleformat{\paragraph}{\normalsize\py@HeaderFamily}%
            {\py@TitleColor}{0em}{\py@TitleColor}{\py@NormalColor}
\titlespacing*{\paragraph}{0pt}{1ex}{0pt}
\makeatother

% Do not quote function signatures: asd() instead of `asd()`
\renewcommand\samp[1]{\code{#1}}

% Large function headers
\let\oldmethodline=\methodline
\renewcommand\methodline[2]{\oldmethodline{\Large #1}{#2}}

% Large method headers
\let\oldfuncline=\funcline
\renewcommand\funcline[2]{\oldfuncline{\Large #1}{#2}}

% Fix footer/header
\renewcommand{\chaptermark}[1]{\markboth{\MakeUppercase{\thechapter.\ #1}}{}}
\renewcommand{\sectionmark}[1]{\markright{\MakeUppercase{\thesection.\ #1}}}

'''

# Documents to append as an appendix to all manuals.
#latex_appendices = []

# If false, no module index is generated.
latex_use_modindex = False

# -----------------------------------------------------------------------------
# Intersphinx configuration
# -----------------------------------------------------------------------------
intersphinx_mapping = {'http://docs.python.org/dev': None,
                       'http://docs.scipy.org/doc/numpy': None,
                       'http://docs.scipy.org/doc/scipy/reference': None,
                       'http://matplotlib.sourceforge.net': None}


# -----------------------------------------------------------------------------
# Numpy extensions
# -----------------------------------------------------------------------------

# If we want to do a phantom import from an XML file for all autodocs
phantom_import_file = 'dump.xml'

# Edit links
#numpydoc_edit_link = '`Edit </pydocweb/doc/%(full_name)s/>`__'

# -----------------------------------------------------------------------------
# Coverage checker
# -----------------------------------------------------------------------------
coverage_ignore_modules = r"""
    """.split()
coverage_ignore_functions = r"""
    test($|_) (some|all)true bitwise_not cumproduct pkgload
    generic\.
    """.split()
coverage_ignore_classes = r"""
    """.split()

coverage_c_path = []
coverage_c_regexes = {}
coverage_ignore_c_items = {}

#
plotting_scripts_directory = "examples/plotting"
