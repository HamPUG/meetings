#!/usr/bin/env python3
#
# File: pythonhouse.py
#
# Description:
# Python script that will launch a draw document using the socket connection 
# and then draw a picture comprised of rectangles and ellipses.
# 
# Written for: Hamilton Python User Group - Presentation 11 May 2015
#              http://www.hampug.org.nz   http://www.meetup.com/nzpug-hamilton/
#               
# Copyright:   This work is licensed under a Creative Commons 
#              Attribution-ShareAlike 4.0 International License.
#              http://creativecommons.org/licenses/by-sa/4.0/
#              
# Author: Ian Stewart
# Release: 2015 May 11
# Version: 1.0
# Test Platform: LibreOffice 4.2, python 3.4, Linux 3.13.0-43, ubuntu-14-04 
#
# PREREQUISITES:
# 1. Ensure you have python3 installed.
# 2. Ensure that Python3-Uno-Bridge is installed. 
#    Check: >>> import uno
#           >>> dir(uno) ...should output about a list of about 50 items.
#    To install: sudo apt-get install python3-uno
#
# LAUNCHING THIS PROGRAM:
# 1. Ensure that there are no libreoffice/openoffce applications running.
# 2. Open a terminal window and enter the command:
#    soffice "--accept=socket,host=localhost,port=2002;urp;StarOffice.ServiceManager"
# 3. Open another terminal window and run this python program:
#    $ python3 pythonhouse.py
# 
# References/Credits: 
# https://wiki.openoffice.org/wiki/Danny%27s_Python_Modules
# https://wiki.openoffice.org/wiki/Danny.OOo.DrawLib.py
# http://www.openoffice.org/udk/python/python-bridge.html
#
# TODO: Check if program runs on a Windows platform.
#
import sys
# Exit if python less than version 3.0.0
if sys.hexversion < 0x03000000:
    sys.exit('\nPython3 is required. Please restart using Python3 \n'
              'Version {0} of python not supported. Exiting...'
              .format(sys.version.split()[0]))               
              
# Importing...
try: 
    import uno
except ImportError:
    sys.exit("ImportError:\nInstall uno: sudo apt-get install python3-uno")

import unohelper
from time import sleep

#Objects from LibreOffice
from com.sun.star.awt import Size
from com.sun.star.awt import Point

# Enumerated constants from LibreOffice.

# FillStyle Constants
from com.sun.star.drawing.FillStyle import NONE, SOLID, GRADIENT, HATCH, BITMAP
# LineStyle Constants
# Note conflict would exist with the duplicate constants NONE, SOLID, etc. 
from com.sun.star.drawing.LineStyle import NONE as lsNONE
from com.sun.star.drawing.LineStyle import SOLID as lsSOLID 
from com.sun.star.drawing.LineStyle import DASH as lsDASH

from com.sun.star.view.PaperOrientation import PORTRAIT, LANDSCAPE
from com.sun.star.view.PaperFormat import A3, A4, A5, B4, B5, LETTER, LEGAL, TABLOID, USER
# USER The real paper size is user defined in 100th mm. 

from com.sun.star.drawing.TextHorizontalAdjust import LEFT, CENTER, RIGHT, BLOCK

from com.sun.star.style.ParagraphAdjust import LEFT as paLEFT
from com.sun.star.style.ParagraphAdjust import RIGHT as paRIGHT
from com.sun.star.style.ParagraphAdjust import BLOCK as paBLOCK
from com.sun.star.style.ParagraphAdjust import CENTER as paCENTER
from com.sun.star.style.ParagraphAdjust import STRETCH as paSTRETCH

#from com.sun.star.text.ControlCharacter import PARAGRAPH_BREAK
#from com.sun.star.text.TextContentAnchorType import AS_CHARACTER

# TODO: Work out how use PageStyle / PageProperties.
# This doesn't work...
#from com.sun.star.style.PageStyle import PageProperties
#from com.sun.star.style.PageProperties import 
# 
#Constants:
PAGE_WIDTH = 29700 # A4 Landscape
PAGE_HEIGHT = 21000 # A4 Landscape
PAGE_ORIENTATION = LANDSCAPE
TITLE = "Python UNO Connection to LibreOffice Draw Example"
MESSAGE1 = """
Error: __main__.NoConnectException: Connector : couldn't connect to socket\n
Perform the following:
1. Ensure that there are no libreoffice/openoffce applications running.
2. Open a new terminal window and enter the command:
soffice "--accept=socket,host=localhost,port=2002;urp;StarOffice.ServiceManager"
3. From the original terminal re-launch this program: $ python3 pythonhouse.py
"""  
 
#------------------------------------------------------------------------------ 
#   Create connection to libreoffice and return the desktop object
#------------------------------------------------------------------------------ 
def connection_to_libreoffice():
    '''Establish python connection to LibreOffice and return the desktop'''
    
    localContext = uno.getComponentContext()
				       
    resolver = localContext.ServiceManager.createInstanceWithContext(
	    "com.sun.star.bridge.UnoUrlResolver", localContext)
    try:
        smgr = resolver.resolve(
        "uno:socket,host=localhost,port=2002;urp;StarOffice.ServiceManager")
    except:
        sys.exit(MESSAGE1)
                
    remoteContext = smgr.getPropertyValue("DefaultContext")

    desktop = smgr.createInstanceWithContext("com.sun.star.frame.Desktop",
            remoteContext)

    return desktop

    # Alternative port 8100
    #smgr = resolver.resolve(
    #    "uno:socket,host=localhost,port=8100;urp;StarOffice.ServiceManager")
            
    #Alternative variable naming:
    #mycontext = uno.getComponentContext()
    #resolver = mycontext.ServiceManager.createInstanceWithContext
    #    ("com.sun.star.bridge.UnoUrlResolver", mycontext)
    #myapi = resolver.resolve
    #("uno:socket,host=localhost,port=2002;urp;StarOffice.ComponentContext")

#------------------------------------------------------------------------------ 
#   Creating new documents on the desktop
#------------------------------------------------------------------------------ 
def make_writer_document(desktop): 
    """Create a new Writer document.""" 
    return desktop.loadComponentFromURL(
            "private:factory/swriter", "_blank", 0, () )

def make_calc_document(desktop): 
    """Create a new Calc document.""" 
    return desktop.loadComponentFromURL(
            "private:factory/scalc", "_blank", 0, () )            

def make_draw_document(desktop): 
    """Create a new Draw document.""" 
    return desktop.loadComponentFromURL(
            "private:factory/sdraw", "_blank", 0, () )

def make_impress_document(desktop): 
    """Create a new Impress document.""" 
    return desktop.loadComponentFromURL(
            "private:factory/simpress", "_blank", 0, () )
    

#------------------------------------------------------------------------------ 
#   Set the documents style / layout
#------------------------------------------------------------------------------
#TODO: Use  com.sun.star.style.PageStyle and PageProperties

def set_page_dimensions(doc, width, height, orientation):
    '''Set the page dimensions in 1/100th's of mm'''
    oDoc.getCurrentController().CurrentPage.Width = width
    oDoc.getCurrentController().CurrentPage.Height = height    
    oDoc.getCurrentController().CurrentPage.Orientation = orientation

 
def set_page_based_on_printer(doc, orientation):
    #TODO: Not used   
    '''
    The paper capabilities of the printer can be reflected back to determine
    the choices of paper size and capability of orientation, etc. This is 
    instead of forcing the width and height dimension settings of a Draw page.

    The get/set of getPrinter() determine the Name of the Printer, and 
    PaperOrientation PaperFormat PaperSize, etc.
    
    Set the Paper Orientation, but need to preserve the 
    PaperSize and PaperFormat or they will reset to default.
    '''
    print(doc.getPrinter()[1:]) #.Name('PaperFormat')))
    
    # Returns a complex tuple with Name and Value fields
    desc = doc.getPrinter()
    print(len(desc)) #8
    
    for i in range(len(desc)):
        #print(desc[i])
        #Name PaperOrientation PaperFormat PaperSize IsBusy 
        #CanSetPaperOrientation CanSetPaperFormat CanSetPaperSize
        # Name is the name of the printer E.g. "DCP7065DN" a Brother printer.
        
        if desc[i].Name == 'CanSetPaperOrientation':
            print(desc[i].Value) # True
            
            if desc[i].Name == 'PaperOrientation':
                desc[i].Value = orientation  
                
        else:
            print("Warning: CanSetPaperOrientation = False")        

    doc.setPrinter(desc)  


    # "USER" should specify the size of the paper in 100th's' mm.
    # It may be specifying the PaperSize is measured in Twips. 
    # There are approximately 56.7 twips per mm.

 
#------------------------------------------------------------------------------ 
#   Shape functions 
#------------------------------------------------------------------------------  
def make_rectangle_shape(doc, position=None, size=None): 
    """Create a new RectangleShape with an optional position and size.""" 
    shape = make_shape(
            doc, "com.sun.star.drawing.RectangleShape", position, size) 
    return shape 
 
def make_ellipse_shape(doc, position=None, size=None): 
    """Create a new EllipseShape with an optional position and size.""" 
    shape = make_shape( 
            doc, "com.sun.star.drawing.EllipseShape", position, size) 
    return shape 
  
def make_line_shape(doc, position=None, size=None): 
    """Create a new LineShape with an optional position and size.""" 
    shape = make_shape(
            doc, "com.sun.star.drawing.LineShape", position, size) 
    return shape 
 
def make_text_shape(doc, position=None, size=None): 
    """Create a new TextShape with an optional position and size.""" 
    shape = make_shape(
            doc, "com.sun.star.drawing.TextShape", position, size) 
    return shape 
  
def find_shape_by_name(oShapes, cShapeName): 
    """
    Find a named shape within an XShapes interface. 
    oShapes can be a drawing page, which supports the XShapes interface. 
    Thus, you can find a named shape within a draw page, or within a grouped 
    shape, or within a selection of several shapes. 
    """ 
    nNumShapes = oShapes.getCount() 
    for i in range( nNumShapes ): 
        shape = oShapes.getByIndex( i ) 
        cTheShapeName = oShape.getName() 
        if cTheShapeName == cShapeName: 
            return shape 
    return None 
 
def make_shape(doc, cShapeClassName, position=None, size=None): 
    """
    Create a new shape of the specified class. 
    Position and size arguments are optional. 
    """ 
    shape = doc.createInstance(cShapeClassName) 
 
    if position != None: 
        shape.Position = position 
    if size != None: 
        shape.Size = size 
 
    return shape 
 
 
#------------------------------------------------------------------------------ 
#   Color manipulation 
#------------------------------------------------------------------------------ 
def rgb_color(nRed, nGreen, nBlue): 
    """Return an integer which represents a color. 
    The color is specified in RGB notation. 
    Each of nRed, nGreen and nBlue must be a number from 0 to 255. 
    """ 
    return (int(nRed) &255) << 16 | (int(nGreen) &255) << 8 | (int(nBlue) &255) 

def red_color(color): 
    """Return the Red component of a color as an integer from 0 to 255. 
    nColor is an integer representing a color. 
    This function is complimentary to the rgbColor function. 
    """ 
    return (int(color) >> 16) & 255 
 
def green_color(color): 
    """Return the Green component of a color as an integer from 0 to 255. 
    nColor is an integer representing a color. 
    This function is complimentary to the rgbColor function. 
    """ 
    return (int(color) >> 8) & 255 
 
def blue_color(nColor): 
    """Return the Blue component of a color as an integer from 0 to 255. 
    nColor is an integer representing a color. 
    This function is complimentary to the rgbColor function. 
    """ 
    return int(nColor) & 255 
 

#------------------------------------------------------------------------------ 
#   Miscellaneous - Reserved for future use
#------------------------------------------------------------------------------ 
def createframe(doc,text,cursor):
    '''Two lines of text in a frame'''
    textFrame = doc.createInstance("com.sun.star.text.TextFrame")
    textFrame.setSize(Size(15000,400))
    # Done in import stage
    #from com.sun.star.text.TextContentAnchorType import AS_CHARACTER
    textFrame.setPropertyValue("AnchorType" , AS_CHARACTER)

    text.insertTextContent(cursor, textFrame, 0)

    textInTextFrame = textFrame.getText()
    cursorInTextFrame = textInTextFrame.createTextCursor()
    textInTextFrame.insertString(cursorInTextFrame, 
        "The first line in the newly created text frame.", 0)
    textInTextFrame.insertString(cursorInTextFrame,
        "\nWith this second line the height of the frame raises.",0)
    text.insertControlCharacter(cursor, PARAGRAPH_BREAK, 0)

    cursor.setPropertyValue("CharColor", 65536)
    cursor.setPropertyValue("CharShadowed", uno.Bool(0))


#------------------------------------------------------------------------------ 
#   Draw a house
#------------------------------------------------------------------------------ 
def draw_sky(doc):    
    '''Draw sky'''
    shape_position = Point() # from com.sun.star.awt import Point
    shape_position.X = 1000
    shape_position.Y = 1000
    shape_size = Size() # from com.sun.star.awt import Size
    shape_size.Width= 27700
    shape_size.Height= 19000 
    #print(dir(oDoc.DrawPages.page1))
    rectangle = make_rectangle_shape(doc, shape_position, shape_size)
    # Set colours
    #print(dir(rectangle)) 
    #print(len(dir(rectangle))) # 255 properties and methods for the rectangle
    rectangle.FillColor = 0x00c0ff 
    rectangle.LineColor = 0xffc0ff
    doc.DrawPages.page1.add(rectangle)

def draw_grass(doc):
    '''Draw the grass'''
    shape_position = Point()
    shape_position.X = 1000
    shape_position.Y = 15000
    shape_size = Size()
    shape_size.Width= 27700
    shape_size.Height= 5000 
    rectangle = make_rectangle_shape(doc, shape_position, shape_size)
    rectangle.FillColor = 0x00c000 
    rectangle.LineColor = 0x00c000    
    doc.DrawPages.page1.add(rectangle)

def draw_sun(doc):
    '''Draw the sun'''
    shape_position = Point() 
    shape_position.X = 3000
    shape_position.Y = 2000
    shape_size = Size() 
    shape_size.Width= 2000
    shape_size.Height= 2000 
    ellipse = make_ellipse_shape(doc, shape_position, shape_size)
    ellipse.FillColor = 0xffff00 
    ellipse.LineColor = 0xffff00    
    doc.DrawPages.page1.add(ellipse)
    
def draw_house_base(doc):
    ''' Draw House Base'''
    shape_position = Point()
    shape_position.X = 8000
    shape_position.Y = 8000
    shape_size = Size()
    shape_size.Width= 14000
    shape_size.Height= 10000 
    rectangle = make_rectangle_shape(doc, shape_position, shape_size)
    rectangle.FillColor = 0xff8000 
    rectangle.LineColor = 0xff8000    
    doc.DrawPages.page1.add(rectangle) 

def draw_house_door(doc):
    '''Draw House Door'''
    shape_position = Point()
    shape_position.X = 10000
    shape_position.Y = 10000
    shape_size = Size()
    shape_size.Width= 4000
    shape_size.Height= 8000 
    rectangle = make_rectangle_shape(doc, shape_position, shape_size)
    rectangle.FillColor = 0x0000ff 
    rectangle.LineColor = 0x0000ff   
    doc.DrawPages.page1.add(rectangle)        
    
def draw_house_doorknob(doc):
    '''Draw doorknob'''    
    shape_position = Point()
    shape_position.X = 13500
    shape_position.Y = 14000
    shape_size = Size()
    shape_size.Width= 300
    shape_size.Height= 300 
    circle = make_ellipse_shape(doc, shape_position, shape_size)
    circle.FillColor = 0xe0e000 
    circle.LineColor = 0xe0e000    
    doc.DrawPages.page1.add(circle) 

def draw_house_window(doc):  
    '''Draw House Window'''
    shape_position = Point()
    shape_position.X = 16000
    shape_position.Y = 10000
    shape_size = Size()
    shape_size.Width= 4000
    shape_size.Height= 3000 
    rectangle = make_rectangle_shape(doc, shape_position, shape_size)
    rectangle.FillColor = 0xc0c0c0 #0x0000ff 
    rectangle.LineColor = 0xc0c0c0 #0x0000ff   
    doc.DrawPages.page1.add(rectangle)  

def draw_house_window_frame(doc):
    '''French windows - 5 x vertical and 4 x horizontal lines.'''
    # Draw the vertical lines
    for i in range(5):
        shape_position = Point()
        shape_position.X = 16000 + i * 1000
        shape_position.Y = 10000
        shape_size = Size()
        shape_size.Width= 0
        shape_size.Height= 3000 
        line = make_line_shape(doc, shape_position, shape_size)
        line.LineColor = 0xffffff
        line.LineWidth = 100
        doc.DrawPages.page1.add(line) 

    # Draw the horizontal lines
    for i in range(4):
        shape_position = Point()
        shape_position.X = 16000 
        shape_position.Y = 10000 + i * 1000
        shape_size = Size()
        shape_size.Width= 4000
        shape_size.Height= 0 
        line = make_line_shape(doc, shape_position, shape_size)
        line.LineColor = 0xffffff
        line.LineWidth = 100
        doc.DrawPages.page1.add(line)

def draw_house_roof(doc): 
    '''Draw House Roof'''
    shape_position = Point()
    shape_position.X = 7000
    shape_position.Y = 6000
    shape_size = Size()
    shape_size.Width= 16000
    shape_size.Height= 2000 
    rectangle = make_rectangle_shape(doc, shape_position, shape_size)
    rectangle.FillColor = 0xff0000 
    rectangle.LineColor = 0xff0000   
    doc.DrawPages.page1.add(rectangle)  
    
def draw_border(doc):
    '''Draw border'''
    shape_position = Point()
    shape_position.X = 1000
    shape_position.Y = 1000
    shape_size = Size()
    shape_size.Width= 27700
    shape_size.Height= 19000 
    rectangle = make_rectangle_shape(doc, shape_position, shape_size)
    rectangle.FillStyle = NONE
    rectangle.FillTransparence = 100 
    rectangle.LineColor = 0x808080
    #rectangle.LineStyle = SOLID #<-- cant reuse SOLID used by FillStyle
    rectangle.LineWidth = 200
    doc.DrawPages.page1.add(rectangle)     

def draw_heading(doc):
    '''Add the heading text. Warning: Steps below must be performed in order'''
    # Step1: Create the text box shape
    shape_position = Point()
    shape_position.X = 8000
    shape_position.Y = 1500
    shape_size = Size()
    shape_size.Width= 16000
    shape_size.Height= 1000
    textbox = make_text_shape(doc, shape_position, shape_size)
    # Step 2: Add the shape to the draw document
    doc.DrawPages.page1.add(textbox)
    # Step 3: get the object getText() and pass the heading string         
    textboxtext = textbox.getText()
    textboxtext.setString("Python House")
    # Make modifications to the text    
    textboxtext.TextAutoGrowHeight = True
    textboxtext.TextAutoGrowWidth = True
    #textboxtext.CharFontName = "Times New Roman"
    #textboxtext.CharFontName = "Purisa"    
    #textboxtext.CharHeight = 80
    #textboxtext.CharColor = 0xff00ff
    # Alternative method of setting properties
    textboxtext.setPropertyValue("CharFontName", "Purisa")    
    textboxtext.setPropertyValue("CharHeight", 80)
    textboxtext.setPropertyValue("CharColor", 0xff00ff)    
    textboxtext.setPropertyValue("CharShadowed", uno.Bool(1))
                 
def draw_text(doc):
    '''Add message. Warning: Steps below must be performed in order'''
    # Step1: Create the text box shape
    shape_position = Point()
    shape_position.X = 1500
    shape_position.Y = 18200
    shape_size = Size()
    shape_size.Width= 26000
    shape_size.Height= 1000
    textbox = make_text_shape(doc, shape_position, shape_size)
    # Step 2: Add the shape to the draw document
    doc.DrawPages.page1.add(textbox)
    # Step 3: get the object getText() and pass the heading string         
    textboxtext = textbox.getText()
    label = ("The python program establishes a connection to libreoffice " \
            "and creates a draw document. The draw document is set to A4 " \
            "landscape. Drawing shapes are added to the document.")
    
    textboxtext.setString(label)
    # Make modifications to the text    
    #textboxtext.TextAutoGrowHeight = True
    #textboxtext.TextAutoGrowWidth = True
    #textboxtext.CharFontName = "Times New Roman"
    textboxtext.CharFontName = "Purisa"    
    textboxtext.CharHeight = 12
    textboxtext.CharColor = 0x000000
    textboxtext.CharColor = 0xffffff    
    textboxtext.CharWeight = 200  

def draw_sign(doc):
    '''Add sign. Warning: Steps below must be performed in order'''
    # Step1: Create the text box shape
    shape_position = Point()
    shape_position.X = 8500
    shape_position.Y = 8300
    shape_size = Size()
    shape_size.Width= 13000
    shape_size.Height= 1000
    textbox = make_text_shape(doc, shape_position, shape_size)
    # Step 2: Add the shape to the draw document
    doc.DrawPages.page1.add(textbox)
    # Step 3: get the object getText() and pass the heading string         
    textboxtext = textbox.getText() 
    textboxtext.setString("Hamilton Python User Group")
    # Make modifications to the text    
    textboxtext.CharFontName = "FreeSans"
    textboxtext.CharHeight = 24
    textboxtext.CharColor = 0x000000   
    textboxtext.CharWeight = 200
    textboxtext.FillStyle = SOLID  #<-- FillStyle is using SOLID
    textboxtext.FillBackground = 0xffffff
    textboxtext.FillTransparence = 0     
    textboxtext.LineStyle = lsSOLID  #<-- Cant use SOLID. Used for FillStyle
    textboxtext.LineColor = 0x000000
    textboxtext.LineTransparence = 0        
    textboxtext.LineWidth = 80
    textboxtext.TextHorizontalAdjust = CENTER
      
def draw_sign_uni(doc):
    '''Add sign. Warning: Steps below must be performed in order'''
    # Step1: Create the text box shape
    shape_position = Point()
    shape_position.X = 10000
    shape_position.Y = 10000
    shape_size = Size()
    shape_size.Width= 4000
    shape_size.Height= 5000
    textbox = make_text_shape(doc, shape_position, shape_size)
    # Step 2: Add the shape to the draw document
    doc.DrawPages.page1.add(textbox)
    # Step 3: get the object getText() and pass the heading string         
    textboxtext = textbox.getText()
    textboxtext.setString("Waikato\nUniversity\n\nMS4.G.02")
    # Make modifications to the text    
    textboxtext.CharFontName = "FreeSans"
    textboxtext.CharHeight = 16
    textboxtext.CharColor = 0xffffff   
    textboxtext.CharWeight = 200
    textboxtext.FillStyle = NONE  
    #textboxtext.FillBackground = 0xffffff
    #textboxtext.FillTransparence = 0     
    textboxtext.LineStyle = lsNONE
    textboxtext.LineColor = 0x000000
    #textboxtext.LineTransparence = 0        
    #textboxtext.LineWidth = 80
    #textboxtext.TextHorizontalAdjust = CENTER      
    textboxtext.ParaAdjust = paCENTER  #<-- Cant use CENTER need paCENTER
    
#------------------------------------------------------------------------------ 
#   Main
#------------------------------------------------------------------------------ 
if __name__ == "__main__":
    '''
    Connect to Libreoffice and return the desktop object
    Create a new Draw document 
    Set Draw page to A4 dimensions and Landscape 
    The document is given a Title
    Shapes are added to the document
    '''
    # Establish connection to LibreOffice 
    oDesktop = connection_to_libreoffice()

    # Create a new Document
    #oDoc = make_writer_document(oDesktop)
    #oDoc = make_calc_document(oDesktop)
    oDoc = make_draw_document(oDesktop)
    #oDoc = make_impress_document(oDesktop)

    # Set the page dimensions in 1/100th's of mm
    # TODO: Add check if Draw/Impress application. Investigate writer/calc 
    set_page_dimensions(oDoc, PAGE_WIDTH, PAGE_HEIGHT, PAGE_ORIENTATION)
    
    # Give the Draw document a title / file name 
    #print(oDoc.Title) # Initially is "Untitled1"
    oDoc.setTitle(TITLE)

    # Define object DrawPages
    #oDrawpages = oDoc.DrawPages

    # Draw shapes and add text to the Draw document
    sleep(3.0) # Allow adjustment
    draw_sky(oDoc)    
    draw_grass(oDoc)
    draw_sun(oDoc)      
    draw_house_base(oDoc)
    draw_house_door(oDoc)
    draw_house_doorknob(oDoc)
    draw_house_window(oDoc)
    draw_house_window_frame(oDoc)       
    draw_house_roof(oDoc)
    draw_border(oDoc)   
    draw_text(oDoc)          
    draw_sign(oDoc)
    draw_sign_uni(oDoc)
    sleep(1.0)
    draw_heading(oDoc)       
'''
Notes:
Duplicated Enumerated Constants
When SOLID is imported for FillStyle, then SOLID will fail for LineStyle

Traceback (most recent call last):
  File "pythonhouse.py", line 555, in <module>
    draw_sign(oDoc)
  File "pythonhouse.py", line 507, in draw_sign
    textboxtext.LineStyle = SOLID
__main__.CannotConvertException: value cannot be converted to demanded ENUM!

Can not import both with the same constant name.

Work-around to avoid conflict...
from com.sun.star.drawing.FillStyle import NONE, SOLID, GRADIENT, HATCH, BITMAP

from com.sun.star.drawing.LineStyle import NONE as lsNONE
from com.sun.star.drawing.LineStyle import SOLID as lsSOLID 
from com.sun.star.drawing.LineStyle import DASH as lsDASH

then the following works...
    textboxtext.FillStyle = SOLID     
    textboxtext.LineStyle = lsSOLID

Duplicated enumerated constants can also be overcome by using classes.

===

Note Unable to exract the numeric value of the Enum...
print(LEFT) # <uno.Enum com.sun.star.drawing.TextHorizontalAdjust ('LEFT')>
print(type(LEFT)) # <class 'uno.Enum'>
print(repr(LEFT)) # <uno.Enum com.sun.star.drawing.TextHorizontalAdjust ('LEFT')>

'''    
    
