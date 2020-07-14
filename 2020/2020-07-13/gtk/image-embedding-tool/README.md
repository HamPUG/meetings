# Image Embedding Tool

The program **image_embedding_tool.py** converts an image to a Base 64 constant which 
may then be embedded into a Python GTK program that is being developed.

When the developed program is run the Base 64 constant is then be reverted back to 
an image and may be used as the GUI programs logo or favicon, etc. 

Images of around 32 pixel x 32 pixel are suitable as when converted to base 64 they 
only take up about 50 lines at 76 characters per line.

Once you have selected the image you wish to embed, this program will display
the constant of the image converted to base 64 in its text view widget. 
*Select All* and *Copy* this constant into the program you are developing.

The constant in the text view widget will be similar to this...
```
    B64_IMAGE = (b"""
    PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiIHN0YW5kYWxvbmU9Im5vIj8+Cjwh
    LS0gQ3JlYXRlZCB3aXRoIElua3NjYXBlIChodHRwOi8vd3d3Lmlua3NjYXBlLm9yZy8pIC0tPgoK
    PHN2ZwogICB4bWxuczpkYz0iaHR0cDovL3B1cmwub3JnL2RjL2VsZW1lbnRzLzEuMS8iCiAgIHht
```
...snip...
``` 
    LjE0OTMgMC4wMzg2OCwtOS45MjYyIGwgLTcuMTQ1ODMzLC05LjE5MTUgeiIKICAgICAgIGlkPSJw
    YXRoMjgiCiAgICAgICBpbmtzY2FwZTpjb25uZWN0b3ItY3VydmF0dXJlPSIwIgogICAgICAgc29k
    aXBvZGk6bm9kZXR5cGVzPSJjY2NjY2NjYyIgLz4KICA8L2c+Cjwvc3ZnPgo=
    """)
```

Please review the code in the **image_embedding_tool.py** GTK program as it includes an
embedded image.

## Additional Code

As well as the base 64 constant, *B64_IMAGE*, the following need to be added to the GTK 
program that is being developed.

1.  At the start of the program add the following imports:
```
    import tempfile
    import base64
    import os
```

2.  For the image to be used as a favicon and display in the system tray, then
    after the Gtk.Window() class has been created add the line:
```       
    self.image_path_file = self.get_image_temp_file_path()
```

3. Add the following function:
```
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
```

4.  If its desired to use the image as a logo, then during the setup of the
    GUI include code like this:
```
        image = Gtk.Image.new_from_file(self.image_path_file)

        #os.remove(self.image_path_file)

        vbox.pack_start(image, expand=True, fill=True, padding=0)

        self.add(vbox)            
```

5. At the beginning of you program add a constant like:
```
    ICON_IMAGE = 0 
```

## Images for Experimenting

Three image files, one svg and two png, have been included in order to experiment with
using this program. The files are:
* N_32px.svg
* radio_retro_32
* radio_retro_64 



## Screenshots

On launching the program the initial screen is as follows:

<img src="https://github.com/irsbugs/image-embedding-tool/blob/master/initial_screen.png">

Note that the program contains an embedded image of a dogs face using the constant B64_IMAGE_2.
Line 39 of the program is: `ICON_IMAGE = 2`. If this is changed to `ICON_IMAGE = 1`, then 
this program will launch with a letter **N** as the logo and favicon.

After an image file has been selected the text view widget displays the image as base64 and assigns
it to the constant **B64_IMAGE**. *Select All* and *Copy* the contents of the constant in the text 
view widget into the program you are developing.

<img src="https://github.com/irsbugs/image-embedding-tool/blob/master/after_selecting_image.png">
