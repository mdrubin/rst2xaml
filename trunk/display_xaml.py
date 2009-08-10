# requires IronPython and .NET 3

import clr
clr.AddReference('PresentationFramework')
clr.AddReference('PresentationCore')
clr.AddReference('windowsbase')
from System.Windows.Controls import *
from System.Windows.Markup import XamlReader
from System.Windows import Window, Application

from Microsoft.Win32 import OpenFileDialog

dialog = OpenFileDialog()
dialog.ShowDialog()

stream = dialog.OpenFile()
reader = FlowDocumentReader()
flowDocument = XamlReader.Load(stream)
stream.Close()
reader.Document = flowDocument
w = Window()
w.Content = reader
Application().Run(w)

