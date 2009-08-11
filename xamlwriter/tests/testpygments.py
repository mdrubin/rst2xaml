import unittest

from textwrap import dedent

from xamlwriter.writer import publish_xaml

# This installs the pygments directive
import xamlwriter.register_directive


def make_source(string):
    return '.. code-block:: python\n\n    ' +  '\n    '.join(string.splitlines())

def make_doc(string):
    return ('<FlowDocument xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation" '
            'xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml">'
            '<Paragraph FontFamily="Global Monospace" xml:space="preserve">%s'
            '</Paragraph></FlowDocument>' % string)


class TestPygments(unittest.TestCase):
    
    def testComment(self):
        source = make_source('# comment')
        
        expected = make_doc('<Run Foreground="#408080" FontStyle="Italic"># comment</Run><Run></Run>\n')
        self.assertEqual(publish_xaml(source), expected)
    

    def testXamlEscape(self):
        self.fail()


    def DONTtestClass(self):
        source = make_source("""\
        import foo
        
        assert something
        
        class Foo(object):
            def method(self, arg1, arg2=None):
                if a == b:
                    return 3
                
                raise Exception("Weird error")
        """)
        
        print publish_xaml(source)



if __name__ == '__main__':
    unittest.main()
