
from pygments import highlight
from pygments.lexers import get_lexer_by_name

from docutils.parsers.rst import roles, directives, Directive

from xamlwriter.xamlformatter import XamlFormatter



from docutils import nodes
from docutils.parsers.rst import directives

from pygments import highlight
from pygments.lexers import get_lexer_by_name, TextLexer


flowdocument = True

def pygments_directive(name, arguments, options, content, lineno,
                       content_offset, block_text, state, state_machine):
    try:
        lexer = get_lexer_by_name(arguments[0])
    except ValueError:
        # no lexer found - use the text one instead of an exception
        lexer = TextLexer()
    # take an arbitrary option if more than one is given
    formatter = XamlFormatter(flowdocument=flowdocument)
    parsed = highlight(u'\n'.join(content), lexer, formatter)
    return [nodes.raw('', parsed, format='xaml')]

pygments_directive.arguments = (1, 0, 1)
pygments_directive.content = 1
pygments_directive.options = {}

directives.register_directive('code-block', pygments_directive)
