# requires IronPython and .NET 3

import sys
import clr
clr.AddReference('PresentationFramework')
clr.AddReference('PresentationCore')
clr.AddReference('windowsbase')
from System.Windows.Controls import *
from System.Windows.Markup import XamlReader
from System.Windows import Window, Application

if len(sys.argv) == 1:
	from Microsoft.Win32 import OpenFileDialog
	
	dialog = OpenFileDialog()
	dialog.ShowDialog()
	
	stream = dialog.OpenFile()
elif len(sys.argv) > 2:
	print 'display_xaml [xaml_file]'
	sys.exit(1)
else:
	from System.IO import File
	stream = File.OpenRead(sys.argv[1])

reader = FlowDocumentReader()
flowDocument = XamlReader.Load(stream)
stream.Close()
reader.Document = flowDocument
w = Window()
w.Content = reader
Application().Run(w)

