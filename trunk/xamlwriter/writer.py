
from docutils.core import publish_string
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

settings_overrides = {
    'file_insertion_enabled': False,
}

def publish_xaml(input_data, overrides=None):
    config = settings_overrides.copy()
    if overrides is not None:
        config.update(overrides)
    
    rv = publish_string(source=input_data, writer=XamlWriter(),
                        settings_overrides=config)
    return rv.root.to_string()