import unittest
from textwrap import dedent
from docutils.core import publish_string

from xamlwriter.writer import XamlWriter, publish_xaml
from xamlwriter.node import Node, TextNode


settings_overrides = {
    'file_insertion_enabled': False,
}

def tree_from_string(input_data):
    input_data = dedent(input_data)
    rv = publish_string(source=input_data, writer=XamlWriter(),
                        settings_overrides=settings_overrides)

    return rv.root


def get_root():
    node = Node('FlowDocument')
    node.attributes['xmlns'] = "http://schemas.microsoft.com/winfx/2006/xaml/presentation"
    node.attributes['xmlns:x'] = "http://schemas.microsoft.com/winfx/2006/xaml"
    return node


class TestXamlWriter(unittest.TestCase):
    
    def testBasic(self):
        tree = tree_from_string('')
        self.assertEqual(tree, get_root())
    
        
    def testParagraph(self):
        tree = tree_from_string('Hello')
        
        node = get_root()
        node.children.append(Node('Paragraph'))
        node.children[0].children.append(TextNode('Hello'))
        self.assertEqual(tree, node)
    
        
    def testItalics(self):
        tree = tree_from_string('*Hello*')
        
        node = get_root()
        para = Node('Paragraph')
        para.children.append(Node('Italic'))
        para.children[0].children.append(TextNode('Hello'))
        node.children.append(para)
        self.assertEqual(tree, node)
    
        
    def testBold(self):
        tree = tree_from_string('**Hello**')
        
        node = get_root()
        para = Node('Paragraph')
        para.children.append(Node('Bold'))
        para.children[0].children.append(TextNode('Hello'))
        node.children.append(para)
        self.assertEqual(tree, node)
    
        
    def testBlockquote(self):
        tree = tree_from_string('Hello\n\n    foo\n')
        
        node = get_root()
        para = Node('Paragraph')
        para.children.append(TextNode('Hello'))
        node.children.append(para)
        
        quote = Node('Paragraph')
        quote.attributes['TextIndent'] = "25"
        quote.children.append(TextNode('foo'))
        node.children.append(quote)
        
        self.assertEqual(tree, node)


    def testRawXaml(self):
        data = '.. raw:: xaml\n\n   foo'
        output = publish_xaml(data)
        node = get_root()
        node.children.append(TextNode('foo'))
        self.assertEqual(output, node.to_string())
        
    
    def testLiteralBlock(self):
        node = get_root()
        literal = Node('Paragraph')
        literal.attributes['FontFamily'] = 'monospace'
        literal.attributes['xml:space'] = 'preserve'
        node.children.append(literal)
        literal.children.append(TextNode('foo'))
        
        self.assertEqual(tree_from_string('::\n\n    foo'), node)
    
       
    def testSuperscript(self):
        node = get_root()
        para = Node('Paragraph')
        superscript = Node('Run')
        superscript.attributes['Typography.Variants'] = 'Superscript'
        para.children.append(superscript)
        node.children.append(para)
        superscript.children.append(TextNode('foo'))
        
        self.assertEqual(tree_from_string(':sup:`foo`'), node)
    
    
    def testLineBlock(self):
        node = get_root()
        para = Node('Paragraph')
        para.children.append(TextNode('foo'))
        para.children.append(Node('LineBreak'))
        para.children.append(TextNode('bar'))
        para.children.append(Node('LineBreak'))
        
        node.children.append(para)
        
        actual = tree_from_string("""\
            | foo
            | bar""")
        
        self.assertEqual(actual, node)
        

if __name__ == '__main__':
    unittest.main()
