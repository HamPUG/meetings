#!/usr/bin/env python3
#
# image_embedding_tool.py
#
# Objectives: Embed an image into a python program file. Only one file to 
# distribute.
#
# Ian Stewart - 10 Jul 2020
#
# TODO: In get_image_temp_file_path should not have to write to file.
#   Should be able to decode the base 64 to a var (pixbuff?) and then use the
#   image as required.
#
import base64
import tempfile
import os
import sys
# GI Version checking - although specific versions are not required in all cases.
import gi
gi.require_version('Gst', '1.0')
gi.require_version('GObject', '2.0')
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
gi.require_version('GLib', '2.0')
gi.require_version('Pango', '1.0')
from gi.repository import Gtk, Gdk # #Gst, GObject, GLib, Pango

print("Gtk Version: {}.{}.{}".format(Gtk.get_major_version(), 
            Gtk.get_micro_version(), Gtk.get_minor_version()))

PYTHON_VERSION_MIN = (3, 0, 0)
if sys.version_info < PYTHON_VERSION_MIN: 
    print("Python must be at Version {}.{} or higher."
            .format(PYTHON_VERSION_MIN[0], PYTHON_VERSION_MIN[1]))
    sys.exit("Exiting...")


# Select which Icon image to use. 0,1,2,...:
ICON_IMAGE = 0

# Labelling...
VERSION = "2020-07-10"
TITLE = "Icon Embedding Tool"
FRAME_1 = "Convert an Image to Base 64 for embedding in a Python program"
LABEL_1 = "Click <b>Select Image</b> to locate an image to be converted to base 64"
BUTTON_1 =  "Select Image"
FRAME_2A = "Information"
FRAME_2B = "Image converted to Base 64"

# Set the initial window size in pixels. Note: Mouse can stretch window bigger.
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800
MARGIN_SIZE = 10

# Use CSS as method for changing fonts and colours, etc.
CSS = """
    /* Display */
    /* Warning changes the font in the file chooser dialog. Strange? 
    scrolledwindow {
        font-family: "Courier New", Mono;
        font-weight: 700;
        font-size: 15px;        
    } */
    
    /* CSS to set the font size for self.frame, which has been named 'frame' */
    #frame_2 * {
    font: 18px Mono;
    } 
"""
"""
Old CSS
    /* CSS to set the font size for self.frame, which has been named 'frame' */
    #frame * {
    font: 18px Sans;
    }
    /* CSS to set the font size for treeview, which has been named 'tree' */
    #tree * {
    font: 16px Sans;
    }
    /* CSS to set Message Dialog, but doesn't seem to work */
    #messagedialog * {
    font: 16px Sans;
    }
"""


class Icon_Window(Gtk.Window):
    'Launch the Icon window'
    def __init__(self):
        super(Icon_Window, self).__init__()
                
        self.setup_css()    
        self.setup_main()
        
        self.show_all()

        # Start
        Gtk.main()
        
        # Shutdown actions
        self.destroy()
        sys.exit()
      

    def convert_image_to_base64(self,filename):
        'Convert the icon image to Base64 text for embedding into python program.'
        with open(filename, "rb") as fid:
            data = fid.read()
        data_b64 = base64.encodebytes(data)
        #print('B64_IMAGE = (b"""')
        #print(data_b64.decode('utf-8') + '""")')
        #print()
        #print("Copy the above and paste into your python program")        
        s = 'B64_IMAGE = (b"""\n'
        s += data_b64.decode('utf-8') 
        s += '""")'        
        self.textbuffer.set_text(s)
        

    def get_image_temp_file_path(self):
        '''
        Get the desired B64_IMAGE data and decode it to binary bytes.
        Create a temp file. Returns tuple, E.g.  (13, '/tmp/icon_em0f7c2r.ico')
        [0] An OS-level handle to an open file as would be returned by os.open() 
        [1] The absolute pathname of that file.
        Write out binary bites to the temp file.
        Return the file path
        '''
        #print(len(B64_IMAGE_1)) # 4409
        # Decode the icon image stored as base 64
        if ICON_IMAGE == 0:
            b64_image = B64_IMAGE
        elif ICON_IMAGE == 1:
            b64_image = B64_IMAGE_1
        elif ICON_IMAGE == 2:
            b64_image = B64_IMAGE_2
        else:
            b64_image = B64_IMAGE_2

        image_data = base64.decodebytes(b64_image)
                
        # Create a tempfile
        temp_file_tuple = tempfile.mkstemp(suffix=".ico", 
                                           prefix="icon_", 
                                           dir=None, 
                                           text=False)

        #print(temp_file_tuple) # (13, '/tmp/icon_em0f7c2r.ico')

        # Write to image to tempfile
        with open(temp_file_tuple[0], "wb") as fout:
            fout.write(image_data)

        #print("Temp file exists:", os.path.isfile(temp_file_tuple[1]))
        #print("Temp files size:", os.stat(temp_file_tuple[1]).st_size)
        return temp_file_tuple[1]


    def setup_css(self):
        # Apply css for font and colour changes, etc.
        css_provider = Gtk.CssProvider()
        # If css start with b for bytes: css = b'* { background-color: #f00; }'
        #css_provider.load_from_data(css)
        css_provider.load_from_data(bytes(CSS.encode()))
        context = Gtk.StyleContext()
        screen = Gdk.Screen.get_default()
        context.add_provider_for_screen(screen, 
                                        css_provider,
                                        Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)


    def setup_main(self):

        # Get the path icon in a temp file.    
        self.image_path_file = self.get_image_temp_file_path()

        self.setup_window()
        
        self.setup_vbox_top()
        
        self.add(self.vbox)
        
        self.textbuffer.set_text(NOTES)    


    def setup_window(self):
        # Setup window
        self.set_title(TITLE)
        self.set_size_request(WINDOW_WIDTH, WINDOW_HEIGHT)
        #self.set_default_size(300, 200)
        self.connect("destroy", Gtk.main_quit, "WM destroy")
        self.set_position(Gtk.WindowPosition.CENTER_ALWAYS)

        self.set_icon_from_file(self.image_path_file)

        # Instantiate main container for the window   
        self.vbox = Gtk.VBox() 
        self.vbox.set_margin_start(MARGIN_SIZE)
        self.vbox.set_margin_end(MARGIN_SIZE) 
        self.vbox.set_margin_bottom(MARGIN_SIZE)     


    def setup_vbox_top(self):
        ' VBox contains two frames'

        # Frame_1: for logo, label and button
        self.frame_1 = Gtk.Frame(label = FRAME_1)
        self.frame_1.set_name("frame_1")
        self.frame_1.set_label_align(0.1, 0.9)
        self.frame_1.set_margin_bottom(MARGIN_SIZE)
        
        self.label_1 = Gtk.Label()
        #self.label_1.set_text(LABEL_1)
        self.label_1.set_markup(LABEL_1) 
        self.label_1.set_margin_start(10)
        self.label_1.set_margin_end(10)
        self.label_1.set_line_wrap(True) 
               
        self.button_1 = Gtk.Button(label = BUTTON_1)
        self.button_1.connect("clicked", self.cb_button_1)
        self.button_1.set_margin_start(MARGIN_SIZE)
        self.button_1.set_margin_end(MARGIN_SIZE) 
        
        image = Gtk.Image.new_from_file(self.image_path_file)
        #print("Temp file exists:", os.path.isfile(self.image_path_file))

        # Finished with image temp file? Remove.
        os.remove(self.image_path_file)

        self.hbox = Gtk.HBox()       
        self.hbox.pack_start(image, expand=True, fill=True, padding=0)
        self.hbox.pack_start(self.label_1, expand=True, fill=True, padding=0)
        self.hbox.pack_start(self.button_1, expand=True, fill=True, padding=0)
        self.frame_1.add(self.hbox)
    
        self.vbox.pack_start(self.frame_1, expand=False, fill=True, padding=0)

        # Frame 2: for around the information window
        self.frame_2 = Gtk.Frame(label = FRAME_2A)
        self.frame_2.set_name("frame_2")
        self.frame_2.set_label_align(0.1, 0.9)
                
        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.set_hexpand(True)
        scrolledwindow.set_vexpand(True)
        scrolledwindow.set_min_content_height(200)
        scrolledwindow.set_margin_start(MARGIN_SIZE)
        scrolledwindow.set_margin_end(MARGIN_SIZE) 
        scrolledwindow.set_margin_bottom(MARGIN_SIZE)
        
        self.textview = Gtk.TextView()
        self.textbuffer = self.textview.get_buffer()
        self.textbuffer.set_text("")
        scrolledwindow.add(self.textview)
        
        self.frame_2.add(scrolledwindow)

        self.vbox.pack_start(self.frame_2, expand=True, fill=True, padding=0)


    def cb_button_1(self, widget):
        'Select Image file button'
        self.frame_2.set_label(FRAME_2A)
        self.textbuffer.set_text(NOTES)
        self.open_file_chooser()

    
    def open_file_chooser(self):
        dialog = Gtk.FileChooserDialog(
            title = "Please choose an image file", 
            parent = self,
            action = Gtk.FileChooserAction.OPEN)
            
        dialog.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                           Gtk.STOCK_OPEN, Gtk.ResponseType.OK)
        
        dialog.set_default_size(800,800)  # No effect?
        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            file_path = dialog.get_filename()
            #print("Open clicked")
            #print("File selected: " + file_path)
            self.convert_image_to_base64(file_path)
            self.frame_2.set_label(FRAME_2B)
            #self.labelframe.set_label(os.path.basename(file_path))
            #self.editor.open_file(file_path)
        elif response == Gtk.ResponseType.CANCEL:
            #print("Cancel clicked")
            pass
            
        dialog.destroy()  


# Logo Version 1: 
# Nikola icon. Copied from...
# $ wget https://raw.githubusercontent.com/getnikola/nikola/master/logo/favicon.png
# Then used gimp to scale from 512 x 512 to 32 x 32

# Logo Version 2: 
# Copied from: https://github.com/getnikola/nikola/blob/master/logo/favicon.svg
# Used Inkscape to change 16 x 16 to 32 x 32
# Change black logo to blue colour to show up better.
# Local file name: favicon_blue_32_big.svg



B64_IMAGE_2 = (b"""
AAABAAEAMjIAAAEAGABoHwAAFgAAACgAAAAyAAAAZAAAAAEAGAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAD/////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////8AAP//////////////////
////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////
/////////////////////////////wAA////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////
////AAD/////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////8AAP//////////////////
////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////
/////////////////////////////wAA////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////
////AAD/////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////8AAP//////////////////
//////////////////////////////////////7+/v39/f///////+bm5re3t5WVlYGBgW9vb25t
bW5tbW5ubmxra29vb4qKipycnMvLy/Pz8/////r6+vv8/Pj4+P////7+/vn5+f39/fz8/P39/f//
//////////////7+/v7+/v7+/v7+/gAA////////////////////////////////////////////
/v7+//3++/7/////3ODfcW9vFA4OAAAAAAAAAAMFCA4REhwgFyMlGyorGSsrDyEhERseBgkMAAAA
AAAAAAAALSwsm5WV//f4/////Pz7/P39/f7+/f39/////////////////v7+////////////////
////AAD////////////////////////////////////////////8/v75/Pz59/dGRUcAAAAACQg+
WVdxmpiNvbmXz8ya09Cc1NGX1tSS1NKW1tSb1dSh0tOm0NGbyMSNtK9sh4QyPTwAAAAEAgOIiIf/
///9/f3////////////////////////////////////+/v7+/v7+/v4AAP//////////////////
//////////////////////////r+/s/X1QwODSAkJXeTlJzX1ofTz3/NyYPOyYfMx5PQyqDY0ou2
tnegoom0tqPY14zNzIPPy4zPy4/Py5DLyaLW1pfJyFV5eQAAAEFGRvz7+//+//////7/////////
//////////////7+/v7+/v///////wAA/////////////////////////////////f39/v7+/f39
9fT0BAYFUWhkp9jWj87Nis7Pi8vNlc7QmsnLpcrLVGZmAAQDAAAAAAAAAAAAAgoMV35/l9XTiMzM
hsrKiMvMiMvLi83NjcvKpdDMHSoqUVBS/////v7+/f//////////////////////////////////
////AAD////////////////////////////////////6+vr///8uLS5hdXeb0s9/0cx/z8yQy82O
y8uNy8t7r7AgOjxScHOHqquSzMuc1dSk09OPtbhTa25IaWyQz9CMzM2MzM2MzM2LzM2Nzs6Py8uq
1tQWIyOUmJj9/Pz///////////////////////////////////////8AAP//////////////////
//////////////7+/v///42MjB4wMJzU1pHP0IfLyYnNy47NzIzNyozMyJLNy5fS0o3MzYvMzY3L
yozOzIjOy4fNyo7MypjPzorKyYvLyovLyozNzIzMy4vNy4bMypHOzZjDwAAAAOzt7P78/P//////
/////////////////////////////wAA/////////////////////v/++P39+/z8/v7+zdTUAAAA
m8XBidHMicrMjc3Ri8nNkc3QiMnGot/biL26h7e3iL69ndnYmNPPhMvGic/KnNfWm9TUgLm6h7Sv
nM/KndjTjczJi8rHj83Mjc3NjcvLj8PCeZeVGBcZ////+vz5/P78+vv7///+///+////////////
////AAD////////////////////+///5/f39/Pzo5ecKDQ2VsrBilJCLzsyIzM2Jys6Rys6e0dJr
h4kHDhEGCQsZHyIUFxoAAAQ3R0eNq6tuiYodJygAAwkXGx4ZIyMAAAAiMjKKtLOR09B+zsmMzMyM
zcua1NNUfHxtgIJBQEH////6+vn//v3///7///7///7///////////8AAP//////////////////
//////n6+vXy8yMfIXyJizReXJzU1I3Ky43Nz4vJyqHS1CY7PRwyM4K0taLb2prY1pvV1KHW1m2O
jggOER8xMoqws7HT16nV2JfZ1KjW1HGLjAAFCGeFhp7Q0I3NzIrOy4rNyZfMyTNJSVdlZmBdXf//
/////////vv//v3//////////////wAA/////////////Pz8/v7+//7/8/PyDg4OAAAAT2lrm9LS
jsvMhLu+lczNn9PSGTIxZIKBo87PksnKi87Nhc7Mis3MkMzMlNLNNERFZJSShM3Jjs3Mf8/Mhc7K
hM/LiM3KoNTUIjI1dYSGl8zKmNbReLu3kc3MntHREiEiAAACVVFU/////Pv6+f79+/7+////////
////AAD////////////9/f3///////8xLy4AAABYd3aazs6QzM6V0NI5ZGSItLRDX15ihIOf0tGR
zM2OzMyNzMyMzcyNzcyOzMyP0s04P0Jtjo+JzsuZysyIzcydyc2PzMyAz8uF0c2b1tQYMTCYtrZJ
cG1koJ2LzMqQzMyg0dIeKiwAAAOXlJX////6/Pr7/vz///////////8AAP////////////7+/v39
/bu5uQAAAEVdWp3X04zRz4vKzI/Ky6LY1C1APQsREKHMzZLV1oTS0obOzY3NzZLKzY/LzIrNzYTU
zTc/QmqOj4PPypzKzIfNzInMzYzMzZDLzJXKyara2X2lpAAAAGqGhZzQz4vMy4rMy5DOzaPQ0Q4V
FwgFCP/8/Pz9/P///////////////wAA/////////////f39////U1NTCxQUmtbSjczMhs7Mhc7M
kc3LjMvKodHTeaGkNUlNT3Z6ncvQhsvLes3Li8zMo9PVldDPjtLQNkJIZ4+TgMzKmNPUks/OiszM
hMvNi87Qjb7BL1NTRl1dlcTKls3PjszNis3Nh83MhMzKi8/Mhq6tAAAAvbm6/Pz8+v79////////
////AAD////////////+/v7///8VFBRlgH+JysWTzs+JzcyGz8uRz8uEyceQzcyOyMiT0M+N0c+N
zcyZ0dGhz9CTvbwsP0BEXV2c19IzRklti4uMvr0pPD1SZ2eT1dGg0dOZyMyPzc6S09GPzMqMzc2I
yMmKysqMy8uSz8+MzcuLzcqj1dMXJSWPjo/9+/v+//7///////////8AAP////////////7+/v//
/xMSEoWwq4fQyJLKzI/LzI7PzaDRz3iqqXenp6LX1IzNyYLQyovY0DdXVUBFSQcLCw0cHBERERkr
JxskJD1FRAULChIZGRgVFgcZFjA6O3mhpX3My4LOy6DU1JLExHSkpYW0tabY2ZDIyY/NzIzNzJbS
zT1RUIeNjP////7+/f///////////wAA/////////////v7+////OTc4gqqmg83Gj8rLkc3NYZmY
WGtsAAAAQUBCAAECS2hmpNHNkdDKfqSjCwYIHxocGBkZIRUXHBMTCwgHEgsKGRcWFBwZHBoZKhse
BwwOm9LRg8/NkcDBKTAzICAgHxscGR0gUHN0e7Szjc7Ni8vKmdTQNUhHo6in//////7+////////
////AAD////////////6+vr///+CgoJjfnyGz8iKzs2PzMyn09QcIiXEwML///////9pa2sfJyee
yMWi0M4zREYVFxkfGR0QDQ4OAAAMDg0XERIJAAELFxUbGxoNBgl4nJyWzs2EpqkGCQqwra//////
//9dWVxid3mh1dWJzcqHyseq29kMGhnf4eH//Pz+//7///////////8AAP////////////////7+
/trX1x0qK5LY0oPLyo/Qz1RydbCxtPb7+//+/f////n9+8nPzhYkI43Bvp/S0yo8QBURFhYaHB0Y
GAUQDhsdHCYYGxcdHQkFBmSJiZTU0mCFhD03POnk54GIiWtxb72/u////z9HS5rFx4vMy4rPzZnD
wQsOD////////////////////////wAA/v7+/f399fX1Ozs7mpqa////FBQVjsbDjsvLl9XTHS0t
////+v3/wsPDGRwYABowABg9FRskAwsNcZKWpNTWPFxhBAIACAUFAQMGAgABEAcKAAIBep+bpN3b
OEpMi4SAkpydAA0fH1mjI2i3EjpZREVS29zhP1lXjM/SjMvKa3+CdnN1////XV5ea2tr/////f39
////AAD+/v7///97e3sAAAAAAACTk5Oam55RZ2ePzsyHvrxsdnj//fu5wbcAAiYueOMolf8jj/oq
hfMcMVw9PTUzSkemzs6FrLNajoyd19KHwLtdjIio2dV2paIjJy/LwbfO1dwBETYmi+kUj+kWhPMS
iPkeV7KJhIgmPSqX19ui2NkKExT///8uLCwFBgYAAADl5eX6+vr///8AAP///////xUVFQUFBQEB
ARESEuPl5RsaHZnS0oOzsYeLjP///yYhJzKF3xGB2wUhTBQpWRl/4h2J8Sc2SoaJgh0jIzZCTG6U
lX+jon6hoGB+fR0pKhIVF8vQ1f//+T5DTSdtwiB85QEIKQIADhldoBSU+ilCVzdCRZ3U4mWKimRp
aLOwsAAAAAMCAwMCA3Fxcf7+/v///wAA/v7+0NDQAAAAAAAAAAAAAAAAJCQkCgMHSWdnlsXDanBw
//75ARQzFon/DDZiDwcAAAEBDDZjBX3/EDd1V2BYwubngKqoJSYnCAABAAAARmNljL+/hq2wgZeQ
////NSo1Gn7iGUyQBAMAHiEhDB43Boz5MVyJN0JAreLcEh8eAAAAMC4tAgQCAwEDAQABFRUV////
////AAD///9JSUkAAAAAAAAAAAAAAAAYGhkEAAESHyCp3dgpPTn///8BFisajP4cS5IuLizl/f9i
gaAdgf8VQHI1TEeV1diKy8RwnpsAAAACCgys2dqNysun1NlOPT3///9JR0cZfMoVfdcODxn///+m
uMIdgPcZPnNWh49upqYDBgUHBAMUEhABAwEEAQQBAAEAAAC4uLj8/PwAANvb2wAAAAICAgAAAAAA
AAAAAAEBAAIBAj5KTI3FwH+ppaakpVJQViVwwReG8h8/drvAxjxznDCO7AEMG2mOj4fHy5LNyqPQ
zgAAADI7PpvPz4fQz4/U1CEwMbq9u8HIxQ4vYRyB9yJuu2hzmyhpizqT9QsaKaTWyKrIwwAAAAYE
AwIAAAABAAEAAQMCAwMDAyMjI////wAAbW1tAQEBAQEBAAAAAAAAAAEAAgEABAAAKDk4mNXQlczM
XHVwoKecNDlCJliSKovkHnvCN4bTEi1eAQgJptLOgs3Ois7KnNnTFBwfTmFjjs7Mjs7NjMvLdp6a
AAAAz8nHfoKODzdtInrWOJfnOnrHECRMjLzCj87Jms3LAAAAAAAAAwAAAQAAAAEAAQICAAAAAAAA
wsLCAAATExMDAwMCAgIAAAAAAAAAAAABAQACAAAUIB+h29aU0tA/YWx6kJ5kaWJWWVsaIDYIBR0G
ABEAAAd4qJeEzcSEy9KVyc6X1dAiLjBdenqLzcuOzs2LzMua1NkvSE0AAABOTEmMkpk0OVEVFSZD
VGVsl59ahYWMysuAtbcAAAABAgEDAAABAAAAAQABAQEBAQEEBARycnIAABcXFwMDAwEBAQAAAAAA
AAAAAAEBAAIBAQAAAKbW1IvLyZHHvgADABcfGQ8WHwAACQAFAAMCAniVj5PXy4bMzJDJ0o/My5PW
0CQyNF58fYzNy47NzIvLy4zNzqLS2zlQUwAAAAQAABAGAx4iGgsMCCw6N6DX1IXLylJ8fAAAAAAB
AAIBAQEAAAAAAAEBAQUFBQEBAXV1dQAAs7OzAAAAAwMDAAAAAAAAAAAAAQEAAgAAAAAAa4yLkM3L
iM3Oi77CR09VHRcZIiUjTWhfkMPBkM7RhcnOkcnSlMrNic/JmtrTGCAhVGtsjM3LjczMjs3NjMzH
kczQms/TfaWhNUlICxIXHycqUHpzjM3Jj8rMptPRKT85AAEBAAAAAAAAAAAAAAAAAQEBAwMDFRUV
6urqAAD////AwMACAgIAAAAAAAAAAAAAAQABAAADAAMdKSue0dKFzciL0c+I0NWZ292a19SS0M+G
zcqKzc+PytCKzMuKzsqOy8ybzcwAAAEoODuU09GNzMyJzMuRzsuLys2Lz82JzcSX0tCj2eKY2dyb
y8aTzs+CydCXxMMAAAADAAAAAAABAQEAAAAAAAABAQEiIiL19fX8/PwAAPz8/P///8zMzAAAAAIC
AgEBAQACAQEAAAQBAgAAAGWFgqPT0pLGypDMzI7NyY7Oy4jK0I/NzZPMyI3KyYrTzIbNypbN0Uxn
ZQQAAQAAAJW7vJHKyoTNy5PLzI/KzIzOy4zRyYvMyJDMzo7MzYPOx4TRzpvS1SAtLgQFBAEAAAEB
AQEBAQICAgMDAx0dHf////z8/P39/QAA/////f39////urq6AAAABQUFAQIBAwICAgAAAQMCAAIB
YISBmtvZjcvLjtDQjNHPg83Lic/Mic7LidDNisvJm8/Pc5udAAEABQMCAgECEBgaoc3PisrJjs7O
is7MiM3Mis7NicnJlNLSlc3Ol87OptTSKD49AAIABgQEAAEBAQEBBAQEBAQEGxsb8vLy/Pz8/f39
////AAD9/f3////+/v78/Pza2tpMTEwAAAAAAAACAAACAAAAAgEAAAAZIiM6Tk42W1uMxMWWy86D
yMiF0M6Lzcqg09FVb20AAAAAAwIGBAUFAAEBAwYEDA9+oKOb29iGy8eJ0MyK0MyM0MxspqQqR0o1
SEoDCg0DAgMEAAAEAQEAAAAAAAANDQ10dHT6+vr6+vr////9/f3+/v4AAP7+/v////7+/v7+/v7+
/v///////+fn55qWl0VBQgAAAAYCAiMjIpi4tKTa1o7Ny4/KzKrZ3I20t01nZwAEAwACAAYEAgIE
AwMCAggDBAgDBQMDBQAAAA0cHWiGhp/MypzTz5HOyZfQzLrb2niKjAUFBwQAAggGCFxeX7m5ufX1
9f////////39/f7+/v39/f///////wAA/////////////////////////v7+/f39////////4+Li
VVJSAQIAAAAARFlYX4WDSWdmEhsfAAAADxETISIjNTU0QkNBTU1OT05OT09PSkhIQj4/My8wJRse
CgYIAAAALDs6VndzW3x4LTc3AAAAExQVhoaG/v///f///f39/v7+/v7+////////////////////
+vr6AAD////////////////////////9/f3+///6/Pz6/f36/v3////39fepo6RdWllXU1SZl5jX
29n4+fj////////////////////////////////////////////+/f/y9fW+wsOAfn5TTU5zc3PD
xsX////+/////f/+/f79/f3////////////////+/v7////+/v7+/v4AAP//////////////////
//////////////////7///7///7///z+/v39/f///////////vz+/f7///7//v////7/////////
//////7///7///7///////7///z9/f7////////////////////+/v////7+///+//79/f//////
//////7+/v////////7+/v7+/v7+/gAA////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////
////AAD/////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////8AAP//////////////////
////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////
/////////////////////////////wAA////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////
////AAD/////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////8AAP//////////////////
////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////
/////////////////////////////wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA==
""")


B64_IMAGE_1 = (b"""
PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiIHN0YW5kYWxvbmU9Im5vIj8+Cjwh
LS0gQ3JlYXRlZCB3aXRoIElua3NjYXBlIChodHRwOi8vd3d3Lmlua3NjYXBlLm9yZy8pIC0tPgoK
PHN2ZwogICB4bWxuczpkYz0iaHR0cDovL3B1cmwub3JnL2RjL2VsZW1lbnRzLzEuMS8iCiAgIHht
bG5zOmNjPSJodHRwOi8vY3JlYXRpdmVjb21tb25zLm9yZy9ucyMiCiAgIHhtbG5zOnJkZj0iaHR0
cDovL3d3dy53My5vcmcvMTk5OS8wMi8yMi1yZGYtc3ludGF4LW5zIyIKICAgeG1sbnM6c3ZnPSJo
dHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyIKICAgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIw
MDAvc3ZnIgogICB4bWxuczpzb2RpcG9kaT0iaHR0cDovL3NvZGlwb2RpLnNvdXJjZWZvcmdlLm5l
dC9EVEQvc29kaXBvZGktMC5kdGQiCiAgIHhtbG5zOmlua3NjYXBlPSJodHRwOi8vd3d3Lmlua3Nj
YXBlLm9yZy9uYW1lc3BhY2VzL2lua3NjYXBlIgogICB3aWR0aD0iMzIiCiAgIGhlaWdodD0iMzIi
CiAgIGlkPSJzdmcyOTkxIgogICB2ZXJzaW9uPSIxLjEiCiAgIGlua3NjYXBlOnZlcnNpb249IjAu
OTIuNSAoMjA2MGVjMWY5ZiwgMjAyMC0wNC0wOCkiCiAgIGlua3NjYXBlOmV4cG9ydC14ZHBpPSI5
MCIKICAgaW5rc2NhcGU6ZXhwb3J0LXlkcGk9IjkwIgogICBzb2RpcG9kaTpkb2NuYW1lPSJmYXZp
Y29uX2JsdWVfMzJfYmlnLnN2ZyI+CiAgPGRlZnMKICAgICBpZD0iZGVmczI5OTMiIC8+CiAgPHNv
ZGlwb2RpOm5hbWVkdmlldwogICAgIGlkPSJiYXNlIgogICAgIHBhZ2Vjb2xvcj0iI2ZmZmZmZiIK
ICAgICBib3JkZXJjb2xvcj0iIzY2NjY2NiIKICAgICBib3JkZXJvcGFjaXR5PSIxLjAiCiAgICAg
aW5rc2NhcGU6cGFnZW9wYWNpdHk9IjAuMCIKICAgICBpbmtzY2FwZTpwYWdlc2hhZG93PSIyIgog
ICAgIGlua3NjYXBlOnpvb209IjIyLjYyNzQxNyIKICAgICBpbmtzY2FwZTpjeD0iMTUuMDIzMTY5
IgogICAgIGlua3NjYXBlOmN5PSIxNi41MjA5NzgiCiAgICAgaW5rc2NhcGU6ZG9jdW1lbnQtdW5p
dHM9InB4IgogICAgIGlua3NjYXBlOmN1cnJlbnQtbGF5ZXI9ImxheWVyMSIKICAgICBzaG93Z3Jp
ZD0idHJ1ZSIKICAgICBib3JkZXJsYXllcj0idHJ1ZSIKICAgICBvYmplY3R0b2xlcmFuY2U9IjEi
CiAgICAgZ3JpZHRvbGVyYW5jZT0iMSIKICAgICBpbmtzY2FwZTp3aW5kb3ctd2lkdGg9IjEzNTUi
CiAgICAgaW5rc2NhcGU6d2luZG93LWhlaWdodD0iMTAwMiIKICAgICBpbmtzY2FwZTp3aW5kb3ct
eD0iMTUxIgogICAgIGlua3NjYXBlOndpbmRvdy15PSI0MiIKICAgICBpbmtzY2FwZTp3aW5kb3ct
bWF4aW1pemVkPSIwIgogICAgIHNob3dndWlkZXM9ImZhbHNlIj4KICAgIDxpbmtzY2FwZTpncmlk
CiAgICAgICB0eXBlPSJ4eWdyaWQiCiAgICAgICBpZD0iZ3JpZDMxMjEiCiAgICAgICBlbXBzcGFj
aW5nPSI1IgogICAgICAgdmlzaWJsZT0idHJ1ZSIKICAgICAgIGVuYWJsZWQ9InRydWUiCiAgICAg
ICBzbmFwdmlzaWJsZWdyaWRsaW5lc29ubHk9ImZhbHNlIiAvPgogIDwvc29kaXBvZGk6bmFtZWR2
aWV3PgogIDxtZXRhZGF0YQogICAgIGlkPSJtZXRhZGF0YTI5OTYiPgogICAgPHJkZjpSREY+CiAg
ICAgIDxjYzpXb3JrCiAgICAgICAgIHJkZjphYm91dD0iIj4KICAgICAgICA8ZGM6Zm9ybWF0Pmlt
YWdlL3N2Zyt4bWw8L2RjOmZvcm1hdD4KICAgICAgICA8ZGM6dHlwZQogICAgICAgICAgIHJkZjpy
ZXNvdXJjZT0iaHR0cDovL3B1cmwub3JnL2RjL2RjbWl0eXBlL1N0aWxsSW1hZ2UiIC8+CiAgICAg
ICAgPGRjOnRpdGxlPjwvZGM6dGl0bGU+CiAgICAgIDwvY2M6V29yaz4KICAgIDwvcmRmOlJERj4K
ICA8L21ldGFkYXRhPgogIDxnCiAgICAgaW5rc2NhcGU6bGFiZWw9IkxheWVyIDEiCiAgICAgaW5r
c2NhcGU6Z3JvdXBtb2RlPSJsYXllciIKICAgICBpZD0ibGF5ZXIxIgogICAgIHRyYW5zZm9ybT0i
dHJhbnNsYXRlKDAsLTEwMjAuMzYyMikiPgogICAgPHBhdGgKICAgICAgIHN0eWxlPSJmaWxsOiNm
NWFiMTQ7ZmlsbC1vcGFjaXR5OjE7ZmlsbC1ydWxlOm5vbnplcm87c3Ryb2tlOm5vbmU7c3Ryb2tl
LXdpZHRoOjIuMzMzMzMzMjUiCiAgICAgICBkPSJtIDIzLjQzNzUsMTAyMi4zNjIyIHYgMTguODEy
NSBsIC01LjEwNDE2NywtNi41Nzg0IGMgMC4wMTY1NywxMC4zMDA4IDAsLTAuNDk3NyAtMC4wMjMx
LDkuODM3NCBsIDQuNjE2ODI3LDUuOTI4NSBIIDMwIHYgLTI4IHoiCiAgICAgICBpZD0icGF0aDI4
LTUiCiAgICAgICBpbmtzY2FwZTpjb25uZWN0b3ItY3VydmF0dXJlPSIwIgogICAgICAgc29kaXBv
ZGk6bm9kZXR5cGVzPSJjY2NjY2NjYyIgLz4KICAgIDxwYXRoCiAgICAgICBzdHlsZT0iZmlsbDoj
MzNhNGQ1O2ZpbGwtb3BhY2l0eToxO2ZpbGwtcnVsZTpub256ZXJvO3N0cm9rZTpub25lO3N0cm9r
ZS13aWR0aDoyLjMzMzMzMzI1IgogICAgICAgZD0ibSAxLjk5OTk5OTgsMTAyMi4zNjIyIHYgMjgg
aCA2LjU2MjQ5OTkgdiAtMTguNDQ4IGwgNy4zOTg4MzAzLDkuNTY1NyBjIDAsMCAwLjAxMTA4LC0w
LjE0OTMgMC4wMzg2OCwtOS45MjYyIGwgLTcuMTQ1ODMzLC05LjE5MTUgeiIKICAgICAgIGlkPSJw
YXRoMjgiCiAgICAgICBpbmtzY2FwZTpjb25uZWN0b3ItY3VydmF0dXJlPSIwIgogICAgICAgc29k
aXBvZGk6bm9kZXR5cGVzPSJjY2NjY2NjYyIgLz4KICA8L2c+Cjwvc3ZnPgo=
""")

B64_IMAGE = (b"""
PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiIHN0YW5kYWxvbmU9Im5vIj8+Cjwh
LS0gQ3JlYXRlZCB3aXRoIElua3NjYXBlIChodHRwOi8vd3d3Lmlua3NjYXBlLm9yZy8pIC0tPgoK
PHN2ZwogICB4bWxuczpkYz0iaHR0cDovL3B1cmwub3JnL2RjL2VsZW1lbnRzLzEuMS8iCiAgIHht
bG5zOmNjPSJodHRwOi8vY3JlYXRpdmVjb21tb25zLm9yZy9ucyMiCiAgIHhtbG5zOnJkZj0iaHR0
cDovL3d3dy53My5vcmcvMTk5OS8wMi8yMi1yZGYtc3ludGF4LW5zIyIKICAgeG1sbnM6c3ZnPSJo
dHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyIKICAgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIw
MDAvc3ZnIgogICB4bWxuczpzb2RpcG9kaT0iaHR0cDovL3NvZGlwb2RpLnNvdXJjZWZvcmdlLm5l
dC9EVEQvc29kaXBvZGktMC5kdGQiCiAgIHhtbG5zOmlua3NjYXBlPSJodHRwOi8vd3d3Lmlua3Nj
YXBlLm9yZy9uYW1lc3BhY2VzL2lua3NjYXBlIgogICB3aWR0aD0iMzIiCiAgIGhlaWdodD0iMzIi
CiAgIGlkPSJzdmcyOTkxIgogICB2ZXJzaW9uPSIxLjEiCiAgIGlua3NjYXBlOnZlcnNpb249IjAu
OTIuNSAoMjA2MGVjMWY5ZiwgMjAyMC0wNC0wOCkiCiAgIGlua3NjYXBlOmV4cG9ydC14ZHBpPSI5
MCIKICAgaW5rc2NhcGU6ZXhwb3J0LXlkcGk9IjkwIgogICBzb2RpcG9kaTpkb2NuYW1lPSJmYXZp
Y29uX2JsdWVfMzJfYmlnLnN2ZyI+CiAgPGRlZnMKICAgICBpZD0iZGVmczI5OTMiIC8+CiAgPHNv
ZGlwb2RpOm5hbWVkdmlldwogICAgIGlkPSJiYXNlIgogICAgIHBhZ2Vjb2xvcj0iI2ZmZmZmZiIK
ICAgICBib3JkZXJjb2xvcj0iIzY2NjY2NiIKICAgICBib3JkZXJvcGFjaXR5PSIxLjAiCiAgICAg
aW5rc2NhcGU6cGFnZW9wYWNpdHk9IjAuMCIKICAgICBpbmtzY2FwZTpwYWdlc2hhZG93PSIyIgog
ICAgIGlua3NjYXBlOnpvb209IjIyLjYyNzQxNyIKICAgICBpbmtzY2FwZTpjeD0iMTUuMDIzMTY5
IgogICAgIGlua3NjYXBlOmN5PSIxNi41MjA5NzgiCiAgICAgaW5rc2NhcGU6ZG9jdW1lbnQtdW5p
dHM9InB4IgogICAgIGlua3NjYXBlOmN1cnJlbnQtbGF5ZXI9ImxheWVyMSIKICAgICBzaG93Z3Jp
ZD0idHJ1ZSIKICAgICBib3JkZXJsYXllcj0idHJ1ZSIKICAgICBvYmplY3R0b2xlcmFuY2U9IjEi
CiAgICAgZ3JpZHRvbGVyYW5jZT0iMSIKICAgICBpbmtzY2FwZTp3aW5kb3ctd2lkdGg9IjEzNTUi
CiAgICAgaW5rc2NhcGU6d2luZG93LWhlaWdodD0iMTAwMiIKICAgICBpbmtzY2FwZTp3aW5kb3ct
eD0iMTUxIgogICAgIGlua3NjYXBlOndpbmRvdy15PSI0MiIKICAgICBpbmtzY2FwZTp3aW5kb3ct
bWF4aW1pemVkPSIwIgogICAgIHNob3dndWlkZXM9ImZhbHNlIj4KICAgIDxpbmtzY2FwZTpncmlk
CiAgICAgICB0eXBlPSJ4eWdyaWQiCiAgICAgICBpZD0iZ3JpZDMxMjEiCiAgICAgICBlbXBzcGFj
aW5nPSI1IgogICAgICAgdmlzaWJsZT0idHJ1ZSIKICAgICAgIGVuYWJsZWQ9InRydWUiCiAgICAg
ICBzbmFwdmlzaWJsZWdyaWRsaW5lc29ubHk9ImZhbHNlIiAvPgogIDwvc29kaXBvZGk6bmFtZWR2
aWV3PgogIDxtZXRhZGF0YQogICAgIGlkPSJtZXRhZGF0YTI5OTYiPgogICAgPHJkZjpSREY+CiAg
ICAgIDxjYzpXb3JrCiAgICAgICAgIHJkZjphYm91dD0iIj4KICAgICAgICA8ZGM6Zm9ybWF0Pmlt
YWdlL3N2Zyt4bWw8L2RjOmZvcm1hdD4KICAgICAgICA8ZGM6dHlwZQogICAgICAgICAgIHJkZjpy
ZXNvdXJjZT0iaHR0cDovL3B1cmwub3JnL2RjL2RjbWl0eXBlL1N0aWxsSW1hZ2UiIC8+CiAgICAg
ICAgPGRjOnRpdGxlPjwvZGM6dGl0bGU+CiAgICAgIDwvY2M6V29yaz4KICAgIDwvcmRmOlJERj4K
ICA8L21ldGFkYXRhPgogIDxnCiAgICAgaW5rc2NhcGU6bGFiZWw9IkxheWVyIDEiCiAgICAgaW5r
c2NhcGU6Z3JvdXBtb2RlPSJsYXllciIKICAgICBpZD0ibGF5ZXIxIgogICAgIHRyYW5zZm9ybT0i
dHJhbnNsYXRlKDAsLTEwMjAuMzYyMikiPgogICAgPHBhdGgKICAgICAgIHN0eWxlPSJmaWxsOiNm
NWFiMTQ7ZmlsbC1vcGFjaXR5OjE7ZmlsbC1ydWxlOm5vbnplcm87c3Ryb2tlOm5vbmU7c3Ryb2tl
LXdpZHRoOjIuMzMzMzMzMjUiCiAgICAgICBkPSJtIDIzLjQzNzUsMTAyMi4zNjIyIHYgMTguODEy
NSBsIC01LjEwNDE2NywtNi41Nzg0IGMgMC4wMTY1NywxMC4zMDA4IDAsLTAuNDk3NyAtMC4wMjMx
LDkuODM3NCBsIDQuNjE2ODI3LDUuOTI4NSBIIDMwIHYgLTI4IHoiCiAgICAgICBpZD0icGF0aDI4
LTUiCiAgICAgICBpbmtzY2FwZTpjb25uZWN0b3ItY3VydmF0dXJlPSIwIgogICAgICAgc29kaXBv
ZGk6bm9kZXR5cGVzPSJjY2NjY2NjYyIgLz4KICAgIDxwYXRoCiAgICAgICBzdHlsZT0iZmlsbDoj
MzNhNGQ1O2ZpbGwtb3BhY2l0eToxO2ZpbGwtcnVsZTpub256ZXJvO3N0cm9rZTpub25lO3N0cm9r
ZS13aWR0aDoyLjMzMzMzMzI1IgogICAgICAgZD0ibSAxLjk5OTk5OTgsMTAyMi4zNjIyIHYgMjgg
aCA2LjU2MjQ5OTkgdiAtMTguNDQ4IGwgNy4zOTg4MzAzLDkuNTY1NyBjIDAsMCAwLjAxMTA4LC0w
LjE0OTMgMC4wMzg2OCwtOS45MjYyIGwgLTcuMTQ1ODMzLC05LjE5MTUgeiIKICAgICAgIGlkPSJw
YXRoMjgiCiAgICAgICBpbmtzY2FwZTpjb25uZWN0b3ItY3VydmF0dXJlPSIwIgogICAgICAgc29k
aXBvZGk6bm9kZXR5cGVzPSJjY2NjY2NjYyIgLz4KICA8L2c+Cjwvc3ZnPgo=
""")
NOTES = """
Image Embedding Tool. Version: {}
 
This tool converts an image to Base 64 text which may then be embedded into a 
python GTK program.

When the program is run the Base 64 text is then be reverted back to an image 
and used as the GUI programs logo or favicon, etc.


As well as the base 64 variable, the following need to be added to the GTK 
program being developed.

1.  At the start of the program add the following imports:

    import tempfile
    import base64
    import os

2.  For the image to be used as a favicon and display in the system tray, then
    after the Gtk.Window() class has been created add the line:
        
    self.image_path_file = self.get_image_temp_file_path()


3. Add the following function:

    def get_image_temp_file_path(self):
        '''
        Select the desired B64_IMAGE data and decode it to binary bytes.
        Create a temp file. Returns tuple, E.g.  (13, '/tmp/icon_em0f7c2r.ico')
        [0] An OS-level handle to an open file as would be returned by os.open() 
        [1] The absolute pathname of the file.
        Write out binary bytes to the temp file.
        Return the file path
        '''
        
        # Select the embedded icon image stored in base64
        if ICON_IMAGE == 0:
            b64_image = B64_IMAGE
        elif ICON_IMAGE == 1:
            b64_image = B64_IMAGE_1
        elif ICON_IMAGE == 2:
            b64_image = B64_IMAGE_2

        # Decode base64 data
        image_data = base64.decodebytes(b64_image)
                
        # Use tempfile to create a /tmp/ file for the image
        temp_file_tuple = tempfile.mkstemp(suffix=".ico", 
                                           prefix="icon_", 
                                           dir=None, 
                                           text=False)

        # Write to image to temp_file
        with open(temp_file_tuple[0], "wb") as fout:
            fout.write(image_data)

        # Return path and temp filename
        return temp_file_tuple[1]    


4.  If its desired to use the image as a Logo, then during the setup of the
    GUI include code like this:

        image = Gtk.Image.new_from_file(self.image_path_file)

        #os.remove(self.image_path_file)

        vbox.pack_start(image, expand=True, fill=True, padding=0)

        self.add(vbox)            

""".format(VERSION)


WELCOME_MESSAGE = """
Icon Embedding Tool. Version: {}
 
This tool converts an image to Base 64 text which may then be embedded into a 
python program.

When the program runs the Base 64 text may then be convert back to an image 
and used as a logo or favicon, etc.
""".format(VERSION)

if __name__=="__main__":
    print(WELCOME_MESSAGE)
    Gtk.init(None)
    Icon_Window()
          
          
"""
Notes:

The image is stored in a /tmp file and loaded with: 
image = Gtk.Image.new_from_file(self.image_path_file)


Using new from file. Should be able to use pixel buffer / pixbuf?

Gtk.Image.new() variations...
new
new_from_animation
new_from_file
new_from_gicon
new_from_icon_name
new_from_icon_set
new_from_pixbuf
new_from_resource
new_from_stock
new_from_surface

https://developer.gnome.org/gdk-pixbuf/2.36/
https://developer.gnome.org/gdk-pixbuf/2.36/gdk-pixbuf-Image-Data-in-Memory.html

gdk_pixbuf_new_from_bytes ()
Creates a new GdkPixbuf out of in-memory readonly image data. 
Currently only RGB images with 8 bits per sample are supported. 

http://openbooks.sourceforge.net/books/wga/graphics-gdk-pixbuf.html
"""
