A XAML writer from [reStructured Text](http://docutils.sourceforge.net/) source documents.

The goal is to be able to write out [FlowDocument XAML](http://msdn.microsoft.com/en-us/library/aa970909.aspx) from rest documents for use in WPF and Silverlight / [Moonlight](http://www.mono-project.com/Moonlight) projects.

It includes a [Pygments](http://pygments.org) formatter for outputting a syntax highlighted XAML representation of source code.

rst2xaml itself runs under CPython, but the generated XAML is intended for use from IronPython (or any other .NET language). There is an example IronPython script for displaying the generated XAML using a WPF FlowDocumentReader.

# Current status #

Both the FlowDocument and Silverlight XAML output support the following features of the docutils markup format:

  * title and headings
  * paragraphs
  * bold
  * italics
  * literal blocks
  * inline literals
  * line blocks
  * bullet lists
  * enumerated lists
  * blockquotes
  * the raw:: xaml directive
  * the pygments code-block directive

In addition FlowDocument supports superscript, although this only works with fonts that support it.

See the issues page for additional limitations or bugs.


# Scripts #

There are three scripts that come with rst2xaml:
```
    python rst2xaml.py source.txt output.xaml
    python rst2xamlsl.py silverlight-source.txt silverlight-output.xaml
    ipy.exe display_xaml.py output.xaml
```


If `display_xaml.py` is run without a command line argument it will open a
file dialog for you to choose a xaml file to display.


# Tests #

The tests use the [discover module](http://pypi.python.org/pypi/discover), which is included in the repository for convenience. You run the tests with:

> `python discover.py`

## rst2xaml FlowDocument output ##

![http://www.voidspace.org.uk/python/weblog/images/rst2xaml-wpf.jpg](http://www.voidspace.org.uk/python/weblog/images/rst2xaml-wpf.jpg)

## rst2xaml Silverlight output ##

![http://www.voidspace.org.uk/python/silverlight-rst2xaml.png](http://www.voidspace.org.uk/python/silverlight-rst2xaml.png)