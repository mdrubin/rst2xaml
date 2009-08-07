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


if __name__ == '__main__':
    unittest.main()
