#!/usr/bin/env python3
# presentation_13.py
#
# 1 .Minimum window
# 2. Provide a title <-- Not recommended. Probably be deprecated.
# 2. Set size request to make it bigger
# 2. Use dir to get the Window (self) attributes.
# 3. Add the title field when instantiating the Window.
# 4. Add a grid
# 4. Place a frame in the grid
# 5. In the frame add another grid
# 5. Create a list of buttons and place them into the frames grid.
# 6. Add connect to each button to call routine
# 6. When buttons are clicked perform action to update label.
# 7. Add an identifier field to the buttons
# 7. On callback use identifier.
# 8. Add CSS function and call it on launching application.
# 8. Set style context for label to use CSS 
# 9. Add CSS for Frame and buttons
# 10. Add CSS Colour to buttons and label
# 11. Add Fav icon in the system tray. Not on the title bar with Ubuntu mate.
# 11. Replacement Header Bar supporting sub-title
# 12. Add a Message box and its response when button 0 is clicked.
# 13. Add an icon to the header bar

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
# 13. For Header icon button
from gi.repository import Gio


def add_provider(widget):
    # Provide the CSS for labels and frames.
    screen = widget.get_screen()
    style = widget.get_style_context()
    provider = Gtk.CssProvider()
    provider.load_from_data("""
    .label_top {
        border: 1px solid #000000;
        margin: 15px;
        font: 30px Arial, sans-serif;
        background: SkyBlue;
        }   
             
    .frame_second {
        margin: 10px;
        font: 25px Courier New, monospace;
        } 

    .button_in_frame_grid {
        margin: 5px;
        font: 25px Arial, sans-serif;
        background: Yellow;
        }   
    """.encode('utf-8')) 
        
    style.add_provider_for_screen(screen, provider, Gtk.STYLE_PROVIDER_PRIORITY_USER)


class MyWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Gtk Presentation # 13")        
        self.set_size_request(600, 400)
        #print(dir(self))
        #print(dir(Gtk))

        # Add fav icon to the system tray
        icon_theme = Gtk.IconTheme.get_default()                                   
        pixbuf = Gtk.IconTheme.load_icon(icon_theme, Gtk.STOCK_OK, size=32, flags=0)
        self.set_default_icon(pixbuf)

        # Replacement Header Bar supporting sub-title
        self.hb = Gtk.HeaderBar()
        self.hb.set_show_close_button(True)
        self.hb.props.title = "Gtk Presentation # 13"
        self.hb.props.subtitle = "Uses header bar supporting sub-title"
        self.set_titlebar(self.hb)

		# 13. Add Header icon button
        self.hb_menu_button = Gtk.Button()
        icon = Gio.ThemedIcon(name="open-menu-symbolic")
        image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
        self.hb_menu_button.add(image)
        self.hb_menu_button.set_name("styled_button") #for button on headerbar
        self.hb_menu_button.connect("clicked", self.on_icon_click)
        self.hb.pack_end(self.hb_menu_button)

        # Provide grid for window and insert a frame into the grid.
        self.grid = Gtk.Grid()
        self.add(self.grid)   
        
        # Add a label and a frame to the main frame
        self.label = Gtk.Label(label="My Label")
        self.label.get_style_context().add_class("label_top")
        self.grid.attach(self.label, 0, 0, 1, 1)        
        self.frame = Gtk.Frame(label="A Frame")
        self.frame.get_style_context().add_class("frame_second") 
        self.frame.set_label_align(0.5,0.5)       
        self.grid.attach(self.frame, 0, 1, 1, 1)  
        
        # Provide a grid for the frame and add button array with callback
        self.frame_grid = Gtk.Grid()
        self.frame.add(self.frame_grid)
        self.button_list = []
        for i, name in enumerate(["B1", "B2", "B3", "B4"]):
            button = Gtk.Button(label=name)
            button.get_style_context().add_class("button_in_frame_grid")
            button.connect("clicked", self.on_button_clicked, i)
            self.button_list.append(button)
            self.frame_grid.attach(self.button_list[i], i, 0, 1, 1)
            
    def on_button_clicked(self, button, identifier):
        s = "Button #{}".format(identifier)
        self.label.set_label(s)
        # Button 0 launches the Message box.
        if identifier == 0:
            self.message_dialog_1()
 
	# 13. Call back for icon on header bar
    def on_icon_click(self, widget):
        self.label.set_label("Icon pressed")
               
    # Add a Message box.
    def message_dialog_1(self):
        """
        Create a Gtk.MessageDialog
        """
        message_dialog = Gtk.MessageDialog(
                parent=self,
                #modal=True,
                destroy_with_parent=True,
                message_type=Gtk.MessageType.QUESTION,
                buttons=Gtk.ButtonsType.YES_NO,
                text="Will it be Yes or will it be No?",
                secondary_text="Yes or No will be placed in the label")
        message_dialog.connect("response", self.dialog_response)
        # show the messagedialog
        message_dialog.set_modal(True)
        message_dialog.run()  # Not .show()
        
    # Message Box response. 
    def dialog_response(self, widget, response_id):
        """
        Callback on Message Dialog button being clicked.
        """
        # If the button clicked gives response YES, continue.
        if response_id == Gtk.ResponseType.YES:
            print("Selected Yes")
            self.label.set_label("Yes")
        # If the button clicked gives response NO, stop application.
        elif response_id == Gtk.ResponseType.NO:
            print("Selected No")
            self.label.set_label("No")
        # If ESC is pressed then continue.
        elif response_id == Gtk.ResponseType.DELETE_EVENT:
            print("Esc pressed. Continuing...")
        # Finally, destroy the messagedialog
        widget.destroy()
        return       
            
if __name__=="__main__":
    win = MyWindow()
    win.connect("realize", add_provider)    
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()
	
