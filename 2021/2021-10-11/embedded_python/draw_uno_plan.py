#!/usr/bin/env python3
#
# draw_uno_plan.py
#
# Objective: Interact with LibreOffice Draw using Python.
#
# Requires: python3-uno. i.e. import uno.
#
# On Linux system, locate this python file resides in:
# ~/.config/libreoffice/4/user/Scripts/python/draw_uno_plan.py
#
# Initially launch a LibreOffice application as follows:
# $ libreoffice --calc --accept="socket,host=localhost,port=2002;urp;StarOffice.ServiceManager"
# $ libreoffice --draw --accept="socket,host=localhost,port=2002;urp;StarOffice.ServiceManager"
#
# TODO: Launch LibreOffice application with socket connection from within this code.
#
# Launch program with:
# $ python ~/.config/libreoffice/4/user/Scripts/python/draw_uno_plan.py
# OR:
# Tools--> Macro--> Run Macros --> Library: My Macros --> draw_uno_plan --> 
# Macro Name: main --> Run
#
# Ian Stewart - 2021-07-17
#
#import socket  # <-- only needed on win32-OOo3.0.0
import uno
import sys
import time

# Constants
LABEL = "A4 Landscape. Scale 1:80" # Label in bottom rectangle.
M1 = 1250  # grid points
# Pile dimensions are 200mm x 200mm. 100mm = 125 points	
PILE_X_SIZE = 250
PILE_Y_SIZE = 250

# Get UNO structures.
from com.sun.star.awt import Size
from com.sun.star.awt import Point

from com.sun.star.drawing.FillStyle import SOLID
from com.sun.star.drawing.LineJoint import MITER
from com.sun.star.awt.FontWeight import NORMAL
from com.sun.star.drawing.LineStyle import DASH	
from com.sun.star.awt.MessageBoxType import MESSAGEBOX

def main_initialize():
    # get the uno component context from the PyUNO runtime
    localContext = uno.getComponentContext()
    # create the UnoUrlResolver
    resolver = localContext.ServiceManager.createInstanceWithContext(
	    "com.sun.star.bridge.UnoUrlResolver", localContext )
    # connect to the running office
    ctx = resolver.resolve( 
        "uno:socket,host=localhost,port=2002;urp;StarOffice.ComponentContext" )
    # https://wiki.openoffice.org/wiki/Documentation/DevGuide/ProUNO/Characteristics_of_the_Interprocess_Bridge
    # "uno:socket,host=localhost,port=2002;urp,Negotiate=0,ForceSynchronous=0;StarOffice.ServiceManager"
    smgr = ctx.ServiceManager
    # get the central desktop object
    desktop = smgr.createInstanceWithContext( "com.sun.star.frame.Desktop",ctx)
    # access the current document. i.e. the model
    doc = desktop.getCurrentComponent()
    return desktop, doc
    

def calc_initialize(model):
    # FYI: Code used if activating a Calc spreadsheet. 
    # access the active sheet
    active_sheet = model.CurrentController.ActiveSheet  # AttributeError: ActiveSheet
    # access cell C4
    cell1 = active_sheet.getCellRangeByName("C4")
    # set text inside
    cell1.String = "Hello world"
    # other example with a value
    cell2 = active_sheet.getCellRangeByName("E6")
    cell2.Value = cell2.Value + 1


def draw_initialize(oDoc):
    """ Initialize first page for use with Draw"""
    oPage = oDoc.DrawPages[0]
    #pages = oDoc.DrawPages
    #print(pages.Count) # 1
    #page = pages.getByIndex(0)
    oLM = oDoc.getLayerManager()
    return oPage, oLM


def draw_clear_page(oPage):
    """ 
    Clear all elements off the drawing, except the Control buttons. 
    Work backwards to 0 (-1), step -1. So removal does not impact the indexing.
    """
    for i in range(oPage.Count-1, -1, -1):
        element = oPage.getByIndex(i)
        if element.LayerID == 8:  #<--- change to 3 to keep button controls
            pass
        else:
            # Warning "remove" is case sensitive.
            #oPage.Remove(element) <-- AttributeError: Remove
            oPage.remove(element)

        
def draw_a4_landscape(oPage):
	""" Setup A4 landscape/ working area of 28500 x 19800."""
	oPage.BorderLeft = 600
	oPage.BorderRight = 600
	oPage.BorderTop = 600
	oPage.BorderBottom = 600	
	oPage.Width = 29700 
	oPage.Height = 21000
	
	
def draw_border_text_field(oDoc, oPage):
    """
    Add a border line at the bottom to make a text field.
    Text field is to the right, so buttons can be to the left
    Use rectangle
    """    
    RectangleShape = oDoc.createInstance("com.sun.star.drawing.RectangleShape")
    RectangleShape.LayerID = 5
    RectangleShape.setPosition( Point(10000, 19500) ) 
    #RectangleShape.setPosition( Point(600, 19500) ) # For total width    
    RectangleShape.setSize( Size(19100, 900) )
    #RectangleShape.setSize( Size(28500, 900) )  # For total width          
    RectangleShape.LineColor = 0
    RectangleShape.LineWidth = 10
    RectangleShape.CharColor = 0
    RectangleShape.FillStyle = SOLID #com.sun.star.drawing.FillStyle.SOLID
    RectangleShape.LineJoint = MITER #com.sun.star.drawing.LineJoint.MITER
    RectangleShape.Name = "Page Label"
    RectangleShape.FillTransparence = 50
    RectangleShape.FillColor = 0x00FF00
    #RectangleShape.setFillColor( RGB(255,0,0)) #<-- RGB() doesn't work
    # Also work OK...
    #RectangleShape.setPropertyValue( "FillColor", 13421823 )
    #RectangleShape.setPropertyValue( "FillColor", 0xFF0000 )
    oPage.add(RectangleShape)
    # The text can only be inserted after the drawing object has been added to the drawing page.
    # RectangleShape.String = "A4 Landscape. Scale 1:500"
    # Give it a name so it can be found and changed
    RectangleShape.Name = "Page Label"
    RectangleShape.String =	"Page Information"
    RectangleShape.CharWeight = NORMAL #com.sun.star.awt.FontWeight.NORMAL  #BOLD
    RectangleShape.CharFontName = "FreeSans"  #"Arial"
    RectangleShape.CharHeight = 14	


def draw_border_line(oDoc, oPage):
    """ Draw a border at 600. Polygon more simple than drawing individual lines."""
    PolyPolygonShape = oDoc.createInstance("com.sun.star.drawing.PolyPolygonShape")
    PolyPolygonShape.LayerID = 5		
    PolyPolygonShape.LineColor = 0
    PolyPolygonShape.LineWidth = 10
    PolyPolygonShape.FillTransparence = 100
    oPage.add(PolyPolygonShape) #Page.add must take place before the coordinates are set    
    # Must be an array within an array. In case there are multiple PolyPolygon shapes.
    position_list = [Point(600, 600),  #Top LH
                    Point(29100, 600),  #Top RH
                    Point(29100, 20400),  #Bot RH
                    Point(600, 20400) ]  #Bot LH 
    # That way multiple arrays.
    position_list_2 = [Point(800, 800),  #Top LH
                    Point(28900, 800),  #Top RH
                    Point(28900, 20200),  #Bot RH
                    Point(800, 20200) ]  #Bot LH     
    PolyPolygonShape.PolyPolygon = [position_list,]
    #PolyPolygonShape.PolyPolygon = [position_list, position_list_2] 


def draw_update_page_label_string(oPage, sLabel="Updated Page Label"):
    """ Update the Page Label in bottom of A4 rectangle. """  
    for i in range(oPage.Count):   
        #print(i)
        element = oPage.getByIndex(i)
        if element.Name == "Page Label":
            element.String = sLabel 


def draw_remove_layer(oLM):
    """
    Remove any layers higher than 4.
        Layers that remain...
        0 layout
        1 background
        2 backgroundobjects
        3 controls
        4 measurelines
    """
    #print(oLM.Count)
    for i in range(oLM.Count -1, 4, -1):
        oLM.remove(oLM.getByIndex(i))

def draw_add_layer(oLM):
    """All layer above index 4 have been deleted. Proceed to add layers """
    oLM.insertNewByIndex(5).Name = "Borders"
    oLM.insertNewByIndex(6).Name = "Grid"
    oLM.insertNewByIndex(7).Name = "Piles"
    for i in range(5, 8):
        oLM.getByIndex(i).IsVisible = True
        oLM.getByIndex(i).IsPrintable = True
    
    #print("oLM.Count:", oLM.Count)
    for i in range(oLM.Count):
        pass
        #print("ID:", str(i), "Name:", oLM.getByIndex(i).Name)
    

def draw_add_grid(oDoc, oPage):
    """ 1 meter grid over the main floor area """
    x = 3000
    y = 4000

    for i in range(13):
        # Vertical Grid lines
        LineShape = oDoc.createInstance("com.sun.star.drawing.LineShape")
        LineShape.setPosition(Point(x + (i * M1), y))
        LineShape.setSize( Size(0, 12500) )
        LineShape.LayerID = 6		
        LineShape.LineColor = 0
        LineShape.LineWidth = 10
        LineShape.LineStyle = DASH  # com.sun.star.drawing.LineStyle.DASH		
        # Create a new DashLine object
        LineShape.LineDash.Style = 1 # 0 = Dashes 1 & 4 = dots 2 = None huh?
        LineShape.LineDash.Dots = 2
        LineShape.LineDash.DotLen = 1
        LineShape.LineDash.Dashes = 1
        LineShape.LineDash.DashLen = 100
        LineShape.LineDash.Distance = 50        
        oPage.add(LineShape)				

    for i in range(11):
        # Horizontal Grid Lines
        LineShape = oDoc.createInstance("com.sun.star.drawing.LineShape")
        LineShape.setPosition(Point(x, y + (i * M1)))
        LineShape.setSize( Size(15000, 0))
        LineShape.LayerID = 6		
        LineShape.LineColor = 0
        LineShape.LineWidth = 10		
        LineShape.LineStyle = DASH  #com.sun.star.drawing.LineStyle.DASH		
        # Create a new DashLine object       
        LineShape.LineDash.Style = 1 # 0 = Dashes 1 & 4 = dots 2 = None huh?
        LineShape.LineDash.Dots = 2
        LineShape.LineDash.DotLen = 1
        LineShape.LineDash.Dashes = 1
        LineShape.LineDash.DashLen = 100
        LineShape.LineDash.Distance = 50          		        
        oPage.add(LineShape)	

def draw_add_grid_supplement(oDoc, oPage):
    """ 1 meter grid over the suplemental floor area """
    x = 18000
    y = 4000

    for i in range(1, 8):
        # Vertical Grid lines
        LineShape = oDoc.createInstance("com.sun.star.drawing.LineShape")
        LineShape.setPosition(Point(x + (i * M1), y))
        LineShape.setSize( Size(0, 5000) )
        LineShape.LayerID = 6		
        LineShape.LineColor = 0
        LineShape.LineWidth = 10
        LineShape.LineStyle = DASH  # com.sun.star.drawing.LineStyle.DASH		
        # Create a new DashLine object
        LineShape.LineDash.Style = 1 # 0 = Dashes 1 & 4 = dots 2 = None huh?
        LineShape.LineDash.Dots = 2
        LineShape.LineDash.DotLen = 1
        LineShape.LineDash.Dashes = 1
        LineShape.LineDash.DashLen = 100
        LineShape.LineDash.Distance = 50        
        oPage.add(LineShape)				

    for i in range(5):
        # Horizontal Grid Lines
        LineShape = oDoc.createInstance("com.sun.star.drawing.LineShape")
        LineShape.setPosition(Point(x, y + (i * M1)))   
        LineShape.setSize( Size(8750, 0))
        LineShape.LayerID = 6		
        LineShape.LineColor = 0
        LineShape.LineWidth = 10		
        LineShape.LineStyle = DASH  #com.sun.star.drawing.LineStyle.DASH		
        # Create a new DashLine object       
        LineShape.LineDash.Style = 1 # 0 = Dashes 1 & 4 = dots 2 = None huh?
        LineShape.LineDash.Dots = 2
        LineShape.LineDash.DotLen = 1
        LineShape.LineDash.Dashes = 1
        LineShape.LineDash.DashLen = 100
        LineShape.LineDash.Distance = 50          		        
        oPage.add(LineShape)	


def draw_ruler(X, Y, W, H, oDoc, oPage, MDL=1000, MBRE = False):
    """ 
    Routine to draw measurment lines as layer 4 on a page.
    MDL = MeasureLineDistance. Offset of line from the two points
    MBRE = MeasureBelowReferenceEdge. Above or below the two points.
    """
    MeasureShape = oDoc.createInstance("com.sun.star.drawing.MeasureShape")
    MeasureShape.setPosition( Point(X, Y) )     
    MeasureShape.setSize( Size(W, H) )
    oPage.add(MeasureShape)
    # Changes to font must be after adding to the page
    MeasureShape.LayerID = 4		
    MeasureShape.LineColor = 0
    MeasureShape.LineWidth = 5
    MeasureShape.MeasureLineDistance = MDL
    MeasureShape.MeasureBelowReferenceEdge = MBRE
    MeasureShape.CharWeight = NORMAL  #com.sun.star.awt.FontWeight.NORMAL #BOLD	
    MeasureShape.CharFontName = "FreeSans" #"Ubuntu Mono"
    MeasureShape.CharHeight = 12				


def draw_compass(oDoc, oPage):
    """ Draw an arrow pointing in North direction. Put it in a circle."""
    # Draw and Arrow
    LineShape = oDoc.createInstance("com.sun.star.drawing.LineShape")
    LineShape.setPosition( Point(28000, 18000) )     
    LineShape.setSize( Size(0, 1000) )    
    LineShape.LayerID = 6		
    LineShape.LineColor = 0x0000FF
    LineShape.LineWidth = 50
    oPage.add(LineShape)	
 
    LineShape.LineStartWidth = 200
    LineShape.LineStartName = "Arrow"
    LineShape.RotateAngle = 3000 # 3000 = 30 degrees anti clockwise 
    							 #  from horizontal east to west	

    # Place a circle around the arrow
    EllipseShape = oDoc.createInstance("com.sun.star.drawing.EllipseShape")
    EllipseShape.setPosition( Point(28000 - 500, 18000) )
    EllipseShape.setSize( Size(1000, 1000) )
    oPage.add(EllipseShape)
    EllipseShape.LineColor = 0
    EllipseShape.FillColor = 0x00FF00
    EllipseShape.LineWidth = 5
    EllipseShape.FillTransparence = 80

    # Add N for North
    TextShape = oDoc.createInstance("com.sun.star.drawing.TextShape")
    TextShape.setPosition( Point(28000 - 350, 18000 + 200) )
    TextShape.setSize( Size(500, 500) )    
    oPage.add(TextShape)
    TextShape.String = "N"
    TextShape.CharColor = 0xFF0000	
    TextShape.CharFontName = "FreeSans" #"Ubuntu Mono"
    TextShape.CharHeight = 12


def add_control(oDoc, oPage):
    """ Add the control command buttons. Provide a Name and Label. """   
    aName = ["B0", "B1", "B2"]
    aLabel = ["6m x 5m", "4m x 5m", "4m x 3.33m"]   
    for i in range(3):
        create_button(oDoc, oPage, aName[i], aLabel[i], i)

    # Doesn't change the Form design mode. Have to use Tools--> Forms-->..
    #oDoc.ApplyFormDesignMode = False 
    # Give it a rattle and it seems to then work...
    c = oDoc.getCurrentController()
    c.setFormDesignMode(False)
    c.setFormDesignMode(True)
    c.setFormDesignMode(False)    


def create_button(oDoc, oPage, sName, sLabel, index):
    """ 
    Dynamically create a button.
    https://forum.openoffice.org/en/forum/viewtopic.php?f=20&t=66707&p=296638&hilit=CreateButton#p296638
    Requires routines: AssignAction, AddNewButton, GetIndex, ButtonPushEvent
    """
    # Change to be a file. required by "AssignAction(). ScriptEventDescriptor.ScriptCode"    
    sScriptURL = "vnd.sun.star.script:draw_uno_plan.py$button_push_event?language=Python&location=user"
    # Displays in Design Mode, Button Right click, Control Properties... Events... 
    # draw_uno_plan.py$button_push_event (user, Python)
    
    oButtonModel = add_new_button(sName, sLabel, oDoc, oPage, index)    
    
    oForm = oPage.getForms().getByIndex(0)
    # Find index inside the form container
    nIndex = get_index(oButtonModel, oForm)
    #print(str(nIndex)) # -1
    
    assign_action(nIndex, sScriptURL, oForm, oDoc)

    
def add_new_button(sName, sLabel, oDoc, oPage, index):
    """ Add push buttons to select different pile layouts"""
    oControlShape = oDoc.createInstance("com.sun.star.drawing.ControlShape")
    x = 1000 + (3000*index)
    y = 19700
    width = 2500
    height = 600
    oControlShape.setPosition( Point(x,y) )
    oControlShape.setSize( Size(width,height) )
    #oButtonModel = oDoc.createUnoService("com.sun.star.form.component.CommandButton")  
    oButtonModel = oDoc.createInstance("com.sun.star.form.component.CommandButton")
    #ctx = uno.getComponentContext()
    #oButtonModel = ctx.ServiceManager.createInstanceWithContext( "com.sun.star.form.component.CommandButton", ctx )
    oButtonModel.Name = sName
    oButtonModel.Label = sLabel       
    oControlShape.setControl(oButtonModel)
    oPage.add(oControlShape)
    # Layer 3 is the Controls Layer for Form widgets.
    oControlShape.LayerID = 3
    return oButtonModel


def get_index(oControl, oForm):
    """ 
    Get the index of the form.
    Work-around index increments be one each time so get count-1
    """
    nIndex = -1
    nIndex = oForm.getCount() -1
    return nIndex
    
    """
    # This is probabably trying to fill an holes in index numbering???
    # print(oForm.getCount())
    for i in range(oForm.getCount() - 1):
        #if EqualUnoObjects(oControl, oForm.getByIndex(i)):
        #if oControl is oForm.getByIndex(i):
        if oControl == oForm.getByIndex(i): #<-- Doesn't seem to work as EqualUnoObjects  
            nIndex = i
            break
    return nIndex
    """
    
def assign_action(nIndex, sScriptURL, oForm, oDoc):
    """
    Assign sScriptURL event as css.awt.XActionListener::actionPerformed.
    Event is assigned to the control described by the nIndex in the 
    oForm container
    """
    aEvent = uno.createUnoStruct("com.sun.star.script.ScriptEventDescriptor")  
    #<-- OK with create not Create. Below fails...
    #aEvent = uno.CreateUnoStruct("com.sun.star.script.ScriptEventDescriptor")  

    aEvent.AddListenerParam = ""
    aEvent.EventMethod = "actionPerformed"
    aEvent.ListenerType = "XActionListener"
    aEvent.ScriptCode = sScriptURL
    aEvent.ScriptType = "Script"

    oForm.registerScriptEvent(nIndex, aEvent) 
    

def button_push_event(button):
    """
    All push buttons handled by this call-back function
    Execute Action: draw_uno_plan.py$button_push_event (user, Python)
    # TODO: Get oDOC and oPage
    """    

    desktop, doc = main_initialize()
    #calc_initialize(doc)
    page, lm = draw_initialize(doc)     
    #print( str(page.getCount()))  
    clear_pile(doc, page)
      
    if button.Source.Model.Name == "B0":
        #print("B0")
        add_pile_0(doc, page)
        
    elif button.Source.Model.Name == "B1":
        #print("B1")
        add_pile_1(doc, page) 
        
    elif button.Source.Model.Name == "B2":
        #print("B2")
        add_pile_2(doc, page)

    else:
        print("Button Name not found")

def add_pile_0(oDoc, oPage):
    """
    Add a grid of piles 6 meters apart horizontal and 5m apart vertical for a
    total of 9 piles. Calls pile subroutine to draw. 1m = M1 = 1250
    """
    for i in range(3):
        for j in range(3): 
            pile(oDoc, oPage, i*6*M1 + 2900, j*5*M1 + 3900)    
   
    # element = oPage.getByName("Page Label")
    for i in range( oPage.getCount() -1):
        element = oPage.getByIndex(i)
        #print(element.Name)   
        if element.Name == "Page Label":
            element.String = "6m x 5m. 9 piles. " + LABEL
            break


def add_pile_1(oDoc, oPage):
    """
    Add a grid of piles 4 meters apart horizontal and 5m apart vertical for a 
    total of 12 piles. Calls pile subroutine. 1m = M1 = 1250 """
    for i in range(4):
        for j in range(3): 
            pile(oDoc, oPage, i*4*M1 + 2900, j*5*M1 + 3900)    

    # element = oPage.getByName("Page Label")
    for i in range( oPage.getCount() - 1):
        element = oPage.getByIndex(i)    
        if element.Name == "Page Label":
            element.String = "4m x 5m. 12 piles. " + LABEL
            break


def add_pile_2(oDoc, oPage):
    """
    Add a grid of piles 4 meters apart horizontal and 3.33m apart vertical for a
    total of 16 piles Calls pile subroutine. 1m = M1 = 1250.
    """
    for i in range(4):
        for j in range(4):
            pile(oDoc, oPage, i*4*M1 + 2900, j*3.333*M1 + 3900)    

    # element = oPage.getByName("Page Label")
    for i in range( oPage.getCount() - 1):
        element = oPage.getByIndex(i)    
        if element.Name == "Page Label":
            element.String = "4m x 3.33m. 16 piles. " + LABEL
            break


def clear_pile(oDoc, oPage):
    """ Clear any previous piles which are on Layer 7. Clear from the top down. """
    for i in range(oPage.getCount()-1, -1, -1):
        element = oPage.getByIndex(i)
        if element.LayerID == 7:
            oPage.remove(element)
            
            
def pile(oDoc, oPage, x, y):
    # Create a pile of 200mm x 200mm starting at x, y
    # Need to positioning offset if pile size is changed
    # Layer 7 is for piles.
        
    # 100mm = 125 points. pile is 200mm x 200mm
    RectangleShape = oDoc.createInstance("com.sun.star.drawing.RectangleShape")
    RectangleShape.setPosition( Point(x, y) )
    RectangleShape.setSize( Size(PILE_X_SIZE, PILE_Y_SIZE) )

    RectangleShape.LineColor = 0
    RectangleShape.LineWidth = 10
    RectangleShape.LayerID = 7
    RectangleShape.FillStyle = SOLID

    RectangleShape.FillTransparence = 20
    RectangleShape.FillColor = 0x0000FF     
    oPage.add(RectangleShape)

    
def main():
    """ Main menu to launch program. """       
    desktop, doc = main_initialize()
    #calc_initialize(doc)

    page, lm = draw_initialize(doc)    
    #print("doc.DrawPages.Count: ", doc.DrawPages.Count)
    #print("page.Count:", page.Count)
    
    draw_clear_page(page) 

    time.sleep(2)
    
    draw_remove_layer(lm)
    
    draw_add_layer(lm)       
     
    # Setup of borders and label box 
    draw_a4_landscape(page)

    draw_border_text_field(doc, page)

    draw_border_line(doc, page)
    
    # Add command buttons for piles
    add_control(doc, page)    
    
    draw_update_page_label_string(page, "A4 Landscape")

    draw_compass(doc, page)

    draw_add_grid(doc, page)
    
    draw_add_grid_supplement(doc, page)

    # Measurment lines:	
    # House horizontal. Pile centers
    draw_ruler(3000, 4000, M1 *12, 0, doc, page, 1500, False)
    # Grid square of 1 meter 
    draw_ruler(3000, 4000, M1, 0, doc, page, 800, False)
    # House vertical. Pile centers
    draw_ruler( 3000, 4000, 0, M1 * 10, doc, page, 800, True)
    # Overall house horizontal
    draw_ruler(3000, 4000, M1*19, 0, doc, page, 2200, False)
    # Additional Grid on RHS
    draw_ruler(3000+M1*19, 4000, 0, M1*4, doc, page, 1000, False)
    # House vertical outside of pile
    draw_ruler(3000, 4000-125, 0, (M1*10)+(125*2), doc, page, 1600, True)		
    # House horizontal outside of pile
    draw_ruler(3000-125, 4000 + M1*10 + 125, (M1*12)+(125*2), 0, doc, page, 1500, True) 

    # A messagebox is available. Only displays strings. Place anywhere to debug code
    #omsgbox("My message")
    #dir_list = dir(uno)
    #omsgbox((", ").join(dir_list), "Python dir() Listing")

def omsgbox(oMessage='', oTitle='Title', oBtnType=1,):
    """ Provide a Message box"""
    desktop, doc = main_initialize()
    frame = desktop.getCurrentFrame()
    window = frame.getContainerWindow()
    toolkit = window.getToolkit()
    msgbox = toolkit.createMessageBox(window, MESSAGEBOX, oBtnType, oTitle, oMessage)
    return msgbox.execute()


if __name__=="__main__":

    main()

"""
Notes:

1.  Be aware of case sensitivity.

2.  References: 
    http://christopher5106.github.io/office/2015/12/06/openoffice-libreoffice-automate-your-office-tasks-with-python-macros.html
    https://wiki.documentfoundation.org/Macros/Python_Guide/Introduction
    https://wiki.documentfoundation.org/Macros/Python_Design_Guide
    https://www.scribd.com/document/75405001/OpenOffice-org-Developer-s-Guide-Professional-UNO    
    https://wiki.openoffice.org/wiki/Python/Transfer_from_Basic_to_Python  
    https://wiki.openoffice.org/wiki/Python/Transfer_from_Basic_to_Python#Script_Context
    https://forum.openoffice.org/en/forum/viewtopic.php?f=20&t=66707&p=296638&hilit=CreateButton#p296638
     
3.  This code uses uno module rather than XSCRIPTCONTEXT. See...
    https://wiki.openoffice.org/wiki/PyUNO_samples - TableSample.py

4.  Change to be a file. required by "AssignAction()  ScriptEventDescriptor.ScriptCode"
    Typical BASIC...
    sScriptURL = "vnd.sun.star.script:Standard.Module1.ButtonPushEvent?language=Basic&location=document"
    
    Some other link...
    sScriptURL = "vnd.sun.star.script:ScriptBindingLibrary.MacroEditor?location=application"
    above equales:  ScriptBindingLibrary.MacroEditor (application, )
    
    For program: ~/.config/libreoffice/4/user/Scripts/python/draw_uno_plan.py
    Function: button_push_event(button):
    sScriptURL = "vnd.sun.star.script:draw_uno_plan.py$button_push_event?language=Python&location=user"
    Events, Execute Action: draw_uno_plan.py$button_push_event (user, Python)
 
5.  aEvent = uno.createUnoStruct("com.sun.star.script.ScriptEventDescriptor")
    aEvent has these structures...
    ListenerType:	listener type as string, same as listener-XIdlClass.getName().  
    EventMethod:	event method as string.  
    AddListenerParam:	data to be used if the addListener method needs an additional parameter.  
    ScriptType:	    type of the script language as string; for example, "Basic" or "StarScript".  
    ScriptCode:	    script code as string (the code has to correspond with the language defined by ScriptType).          
     
   
6.  The BASIC msgbox does not work with python. A messagebox function omsgbox() 
    is available. It only displays strings. Place anywhere to help debug code. E.g.
    dir_list = dir(uno)
    omsgbox((", ").join(dir_list), "Python dir() Listing")


7.  Program control of "Design Mode" is suspect. May need to be toggled a few times.
    Example for BASIC
    Global b as Boolean
    Sub toggleFormDesignMode()
        c = ThisComponent.getCurrentController()
        c.setFormDesignMode(b)
        b = Not b
    End Sub
    
"""
