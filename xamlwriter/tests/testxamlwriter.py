import unittest

from xamlwriter.writer import XamlWriter
from xamlwriter.node import Node, TextNode

from docutils.core import publish_string


settings_overrides = {
    'file_insertion_enabled': False,
}

def tree_from_string(input_data):
    rv = publish_string(source=input_data, writer=XamlWriter(),
                        settings_overrides=settings_overrides)

    return rv.root


class TestXamlWriter(unittest.TestCase):
    
    def testBasic(self):
        tree = tree_from_string('')
        self.assertEqual(tree, Node('Document'))
    
        
    def testParagraph(self):
        tree = tree_from_string('Hello')
        
        node = Node('Document')
        node.children.append(Node('Paragraph'))
        node.children[0].children.append(TextNode('Hello'))
        self.assertEqual(tree.to_string(), node.to_string())
    
        
    def testItalics(self):
        tree = tree_from_string('*Hello*')
        
        node = Node('Document')
        para = Node('Paragraph')
        para.children.append(Node('Italic'))
        para.children[0].children.append(TextNode('Hello'))
        node.children.append(para)
        self.assertEqual(tree.to_string(), node.to_string())
    
        
    def testBold(self):
        tree = tree_from_string('**Hello**')
        
        node = Node('Document')
        para = Node('Paragraph')
        para.children.append(Node('Bold'))
        para.children[0].children.append(TextNode('Hello'))
        node.children.append(para)
        self.assertEqual(tree.to_string(), node.to_string())
    
        
    def testBlockquote(self):
        tree = tree_from_string('Hello\n\n    foo\n')
        
        node = Node('Document')
        para = Node('Paragraph')
        para.children.append(TextNode('Hello'))
        node.children.append(para)
        
        quote = Node('Paragraph')
        quote.attributes['TextIndent'] = "25"
        quote.children.append(TextNode('Hello'))
        node.children.append(quote)
        
        self.assertEqual(tree.to_string(), node.to_string())


if __name__ == '__main__':
    unittest.main()
