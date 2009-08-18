A XAML writer from `reStructured Text <http://docutils.sourceforge.net>`_ source.

The goal is to be able to write out 
`FlowDocument XAML <http://msdn.microsoft.com/en-us/library/aa970909.aspx>`_ 
from ReST documents for use in WPF and Silverlight / 
`Moonlight <http://www.mono-project.com/Moonlight>`_ projects.

It includes a `Pygments <http://pygments.org>`_ formatter for outputting a
syntax highlighted XAML representation of source code.

rst2xaml itself runs under CPython, but the generated XAML is intended for use
from IronPython (or any other .NET language). There is an example IronPython
script for displaying the generated XAML using a WPF
`FlowDocumentReader <http://msdn.microsoft.com/en-us/library/system.windows.controls.flowdocumentreader.aspx>`_.


Requirements
------------

rst2xaml depends on:

* `docutils <http://docutils.sourceforge.net/>`_
* Pygments_


Current status
--------------

The docutils writer for FlowDocument XAML can currently handle the following
markup features:

 * title and headings
 * paragraphs
 * bold
 * italics
 * superscript
 * literal blocks
 * inline literals
 * line blocks
 * bullet lists
 * enumerated lists
 * blockquotes
 * the raw:: xaml directive
 * the pygments code-block directive

The writer for Silverlight XAML, a subset of FlowDocument, can currently handle
the following markup features:

 * paragraphs
 * bold
 * italics
 * blockquotes
 * the raw:: xaml directive
 * the pygments code-block directive


Scripts
-------

There are three scripts that come with rst2xaml::

    python rst2xaml.py source.txt output.xaml
    python rst2xamlsl.py silverlight-source.txt silverlight-output.xaml
    ipy.exe display_xaml.py output.xaml

If ``display_xaml.py`` is run without a command line argument it will open a
file dialog for you to choose a xaml file to display.


Tests
-----

The tests use the `discover module <http://pypi.python.org/pypi/discover>`_,
which is included in the repository for convenience. You run the tests with:

    `python discover.py`
