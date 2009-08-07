
from docutils.writers import Writer
from xamlwriter.translator import XamlTranslator


class XamlWriter(Writer):
    """Writer to convert a docutils nodetree to a XAML nodetree."""

    supported = ('xaml',)
    output = None

    def translate(self):
        visitor = XamlTranslator(self.document)
        self.document.walkabout(visitor)
        self.output = visitor


