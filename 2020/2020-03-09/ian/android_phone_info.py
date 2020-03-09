#!/usr/bin/env python3
# Get Android phone info
# Rename this as main.py
# $ buildozer android debug deploy

from kivy.properties import StringProperty
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.base import runTouchApp
from kivy.lang import Builder

# Get stuff to display
import os

i_list = []

i_list.append("Python Information")
i_list.append("")
i_list.append("Current Working Directory: {}".format(os.getcwd()))

x = os.uname()
i_list.append("System Name: {}".format(x.sysname))
i_list.append("Node Name: {}".format(x.nodename))
i_list.append("Release: {}".format( x.release))
i_list.append("Version: {}".format(x.version))
i_list.append("Machine: {}:".format(x.machine))

i_list.append("")
i_list.append("Top level directory /...")
x = os.listdir("/")
for item in sorted(x):
    i_list.append(item)

try:
    x = os.listdir("/oem/")
    i_list.append("")
    i_list.append("Directory /oem/...")
    for item in sorted(x):
        i_list.append(item)
except:
    pass

try:
    x = os.listdir("/storage/")
    i_list.append("")
    i_list.append("Directory /storage/...")
    for item in sorted(x):
        i_list.append(item)
except:
    pass

s = ""
for item in i_list:
    s += item + "\\n"
    
Builder.load_string('''
<ScrollableLabel>:
    text: "{}"
    Label:
        text: root.text
        font_size: 35
        text_size: self.width, None
        size_hint_y: None
        height: self.texture_size[1]
'''.format(s))


class ScrollableLabel(ScrollView):
    text = StringProperty('')

runTouchApp(ScrollableLabel())
