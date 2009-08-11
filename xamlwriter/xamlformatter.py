# a xaml formatter for pygments


import sys, os
import StringIO

try:
    set
except NameError:
    from sets import Set as set

from pygments.formatter import Formatter
from pygments.token import Token, Text, STANDARD_TYPES
from pygments.util import get_bool_opt, get_int_opt, get_list_opt


__all__ = ['XamlFormatter']


def escape_xaml(text):
    """Escape &, <, > as well as single and double quotes for HTML."""
    return text.replace('&', '&amp;').  \
                replace('<', '&lt;').   \
                replace('>', '&gt;').   \
                replace('"', '&quot;'). \
                replace("'", '&#39;')


class XamlFormatter(Formatter):
    name = 'XAML'
    aliases = ['xaml']
    filenames = ['*.xaml']

    def __init__(self, flowdocument=True, **options):
        Formatter.__init__(self, **options)
        self.flowdocument = flowdocument
        
        self.linenos = 0
        if flowdocument:
            self.lineseparator = '\n'
        else:
            self.lineseparator = '<LineBreak />'
        self.hl_lines = set()
        self.styles = {}
        
        for token, style in self.style:
            format_string = ''
            # a style item is a tuple in the following form:
            # colors are readily specified in hex: 'RRGGBB'
            if style['color']:
                format_string = ' Foreground="#%s"' % style['color']
            if style['bold']:
                format_string += ' FontWeight="Bold"'
            if style['italic']:
                format_string += ' FontStyle="Italic"'
            if style['underline']:
                # not used ?
                pass
            if not self.flowdocument:
                format_string += ' FontFamily="Consolas, Global Monospace"'
            self.styles[token] = format_string


    def format(self, tokensource, outfile):
        """
        The formatting process uses several nested generators; which of
        them are used is determined by the user's options.

        Each generator should take at least one argument, ``inner``,
        and wrap the pieces of text generated by this.

        Always yield 2-tuples: (code, text). If "code" is 1, the text
        is part of the original tokensource being highlighted, if it's
        0, the text is some piece of wrapping. This makes it possible to
        use several different wrappers that process the original source
        linewise, e.g. line number generators.
        """
        source = self._format_lines(tokensource)

        start = end = ''
        if self.flowdocument:
            start = '<Paragraph FontFamily="Consolas, Global Monospace" xml:space="preserve">'
            end = '</Paragraph>'
            
        outfile.write(start)
        for t, piece in source:
            outfile.write(piece)
        
        outfile.write(end)
            

    def _format_lines(self, tokensource):
        """
        Just format the tokens, without any wrapping tags.
        Yield individual lines.
        """
        enc = self.encoding
        lsep = self.lineseparator
        

        lspan = ''
        line = ''
        for ttype, value in tokensource:
            cspan = '<Run%s>' % self.styles[ttype]
            
            
            if not self.flowdocument:
                value = value.replace(' ', '&#0160;')
            parts = escape_xaml(value).split('\n')
            
            # for all but the last line
            for part in parts[:-1]:
                if line:
                    if lspan != cspan:
                        line += (lspan and '</Run>') + cspan + part + \
                                (cspan and '</Run>') + lsep
                    else: # both are the same
                        line += part + (lspan and '</Run>') + lsep
                    yield 1, line
                    line = ''
                elif part:
                    yield 1, cspan + part + (cspan and '</Run>') + lsep
                else:
                    yield 1, lsep
            # for the last line
            if line and parts[-1]:
                if lspan != cspan:
                    line += (lspan and '</Run>') + cspan + parts[-1]
                    lspan = cspan
                else:
                    line += parts[-1]
            elif parts[-1]:
                line = cspan + parts[-1]
                lspan = cspan
            # else we neither have to open a new span nor set lspan

        if line:
            yield 1, line + (lspan and '</Run>') + lsep
            

