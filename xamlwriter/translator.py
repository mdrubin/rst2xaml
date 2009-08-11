import copy
import re

from xamlwriter.node import ErrorNode, Node, TextNode
from docutils import nodes
from docutils.nodes import NodeVisitor, SkipNode



class XamlTranslator(NodeVisitor):

    words_and_spaces = re.compile(r'\S+| +|\n')

    def __init__(self, document, flowdocument=True):
        NodeVisitor.__init__(self, document)
        self.flowdocument = flowdocument
        if flowdocument:
            self.root = Node('FlowDocument')
            self.curnode = self.root
        else:
            self.root = Node('Canvas')
            node = Node('TextBlock')
            self.curnode = node
            self.root.attributes['x:Class'] = 'System.Windows.Controls.Canvas'
        self.root.attributes['xmlns'] = "http://schemas.microsoft.com/winfx/2006/xaml/presentation"
        self.root.attributes['xmlns:x'] = "http://schemas.microsoft.com/winfx/2006/xaml"        
        self.context = []
        self.initial_header_level = 2
        self.section_level = 0

    def begin_node(self, node, tagname, **more_attributes):
        new_node = Node(tagname)
        attributes = new_node.attributes
        for name, value in more_attributes.iteritems():
            attributes[name] = value
        if node is not None:
            # ids and classes handled here
            pass
        new_node.parent = self.curnode
        self.curnode.children.append(new_node)
        self.curnode = new_node

    def end_node(self):
        self.curnode = self.curnode.parent

    def add_text(self, text):
        if text:
            self.curnode.children.append(TextNode(text))

    def add_node(self, name, text='', **attributes):
        self.begin_node(None, name, **attributes)
        self.add_text(text)
        self.end_node()

    def unknown_visit(self, node):
        # should raise here or indicate unsupported feature some way
        return

    def unknown_departure(self, node):
        return

    trivial_nodes = {
        'paragraph': ('Paragraph', {}),
        'strong': ('Bold', {}),
        'block_quote': ('Section', {'Margin': "16,0,0,0"}),
        'emphasis': ('Italic', {}),
        'literal_block': ('Paragraph', {'FontFamily': 'Consolas, Global Monospace', 
                                  'xml:space': 'preserve'}),
        'superscript': ('Run', {'Typography.Variants': 'Superscript'}),
        'line_block': ('Paragraph', {}), 
        'bullet_list': ('List', {}),
        'list_item': ('ListItem', {}),
        'enumerated_list': ('List', {'MarkerStyle': 'Decimal'}),
        'literal': ('Run', {'FontFamily': 'Consolas, Global Monospace', 'xml:space': 'preserve'})
    }

    def dispatch_visit(self, node):
        # don't call visitor methods for trivial nodes
        node_name = node.__class__.__name__
        if node_name == 'Text':
            self.add_text(node.astext())
            raise SkipNode
        tagname, atts = self.trivial_nodes.get(node_name, (None, None))
        if tagname:
            self.begin_node(node, tagname, **atts)
        else:
            getattr(self, 'visit_' + node_name, self.unknown_visit)(node)

    def dispatch_departure(self, node):
        node_name = node.__class__.__name__
        tagname, _ = self.trivial_nodes.get(node_name, (None, None))
        if tagname:
            self.end_node()
        else:
            getattr(self, 'depart_' + node_name, self.unknown_departure)(node)

    def visit_xaml(self, node):
        node = copy.deepcopy(node['xaml'])
        node.parent = self.curnode
        self.curnode.children.append(node)
        raise SkipNode
    
    def visit_line(self, node):
        pass
    
    def depart_line(self, node):
        self.add_node('LineBreak')
    
    def visit_paragraph(self, node):
        if self.flowdocument:
            self.begin_node('Paragraph')
        else:
            self.begin_node('Run')
        
    def depart_paragraph(self, node):
        self.end_node()
        if not self.flowdocument:
            self.add_node('LineBreak')
            self.add_node('LineBreak')

        