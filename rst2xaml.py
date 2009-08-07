import sys

from docutils.core import publish_string
from xamlwriter.translator import XamlTranslator
from xamlwriter.writer import XamlWriter

USAGE = "rst2xaml input_file output_file"

if len(sys.argv) != 3:
    print USAGE
    sys.exit(1)
    
input_data = open(sys.argv[1]).read()
#print input_data


settings_overrides = {
    'file_insertion_enabled': False,
}
rv = publish_string(source=input_data, writer=XamlWriter(),
                    settings_overrides=settings_overrides)

output = rv.root.to_string()
#print output

handle = open(sys.argv[2])
handle.write(rv.root.to_string())
handle.close()