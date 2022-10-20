#!/usr/bin/env python3
#
# pyside6-assistant.py
#
# Ian Stewart - ©CC0 
DATE = "2022-10-07"
#
# TODO: Add zoom to textedit / Pyside Information - Strange it doesn't work?
# 
# Installations to get some example programs to run...
# $ pip install matplotlib
# $ pip install opencv-python  # import cv2
# $ pip install numpy
# $ pip install PyOpenGL
# $ pip install pandas
# $ pip install scipy
# $ pip install matplotlib opencv-python nump PyOpenGL pandas scipy
import sys
import time

import contextlib
from io import StringIO

from pathlib import Path, PurePath, PosixPath

from pygments import formatter, highlight
from pygments.lexers import PythonLexer
from pygments.formatters.html import HtmlFormatter
from pygments.styles import get_style_by_name

from subprocess import run

error_stop = False
try:
    import PySide6.Qt3DAnimation as Qt3DAnimation
    import PySide6.Qt3DCore as Qt3DCore
    import PySide6.Qt3DExtras as Qt3DExtras
    import PySide6.Qt3DInput as Qt3DInput
    import PySide6.Qt3DLogic as Qt3DLogic
    import PySide6.Qt3DRender as Qt3DRender
    import PySide6.QtBluetooth as QtBluetooth
    import PySide6.QtCharts as QtCharts
    import PySide6.QtConcurrent as QtConcurrent
    import PySide6.QtCore as QtCore
    import PySide6.QtDataVisualization as QtDataVisualization
    import PySide6.QtDBus as QtDBus
    import PySide6.QtDesigner as QtDesigner
    import PySide6.QtGui as QtGui
    import PySide6.QtHelp as QtHelp
    import PySide6.QtMultimedia as QtMultimedia
    import PySide6.QtMultimediaWidgets as QtMultimediaWidgets
    import PySide6.QtNetwork as QtNetwork
    import PySide6.QtNetworkAuth as QtNetworkAuth
    import PySide6.QtNfc as QtNfc
    import PySide6.QtOpenGL as QtOpenGL
    import PySide6.QtOpenGLWidgets as QtOpenGLWidgets
    import PySide6.QtPositioning as QtPositioning
    import PySide6.QtPrintSupport as QtPrintSupport
    import PySide6.QtQml as QtQml
    import PySide6.QtQuick as QtQuick
    import PySide6.QtQuick3D as QtQuick3D
    import PySide6.QtQuickControls2 as QtQuickControls2
    import PySide6.QtQuickWidgets as QtQuickWidgets
    import PySide6.QtRemoteObjects as QtRemoteObjects
    import PySide6.QtScxml as QtScxml
    import PySide6.QtSensors as QtSensors
    import PySide6.QtSerialPort as QtSerialPort
    import PySide6.QtSql as QtSql
    import PySide6.QtStateMachine as QtStateMachine
    import PySide6.QtSvg as QtSvg
    import PySide6.QtSvgWidgets as QtSvgWidgets
    import PySide6.QtTest as QtTest
    import PySide6.QtUiTools as QtUiTools
    import PySide6.QtWebChannel as QtWebChannel
    import PySide6.QtWebEngineCore as QtWebEngineCore
    import PySide6.QtWebEngineQuick as QtWebEngineQuick
    import PySide6.QtWebEngineWidgets as QtWebEngineWidgets
    import PySide6.QtWebSockets as QtWebSockets
    import PySide6.QtWidgets as QtWidgets
    import PySide6.QtXml as QtXml
except ModuleNotFoundError as e:
    print(e)
    error_stop = True

# version
VERSION = DATE
PYTHON_VERSION = sys.version.split(" ")[0]
# Qt version
QT_VERSION = "{}".format(QtCore.qVersion())
# Provide the column header with a heading.
HEADING = 'PySide6 Modules'
# Welcome message
WELCOME = """
Welcome to PySide6 Assistant. 
Version:{}
Python:{} 
Qt Version:{}
App:{}
Select a Help Category and then an item within the category.
""".format(VERSION, PYTHON_VERSION, QT_VERSION, sys.argv[0])

# Programs to be excluded from examples tree as they do not run.
BAD_LIST = [
"/axcontainer/axviewer/axviewer.py",  # QAxContainer module is a Windows-only extension.
"/bluetooth/btscanner/main.py",  # QtBluetooth requires at least BlueZ version 5.
"/macextras/macpasteboardmime/macpasteboardmime.py", # Only runs on macOS
]

class MainWindow(QtWidgets.QMainWindow):
    """
    Main Window setup.
    """
    #def __init__(self, *args, **kwargs):
    #    super(MainWindow, self).__init__(*args, **kwargs)

    def __init__(self, dictionary, listing, code_dict, example_list, example_path) -> None:
        super().__init__()

        # Main Window setup...
        self.setWindowTitle("PySide6 Assistant")
        self.setWindowIconText("PySide6")
        # Add QT icon to System Tray Display.
        pixmapi = getattr(QtWidgets.QStyle.StandardPixmap, "SP_TitleBarMenuButton")
        icon = self.style().standardIcon(pixmapi)
        self.setWindowIcon(icon)                
        self.resize(1400,800)  
        
        # Split Main Window horizontally
        splitter_h = QtWidgets.QSplitter()
        splitter_h.setOrientation(QtCore.Qt.Orientation.Horizontal)
        # splitter_h horizontal is attached to the MainWindow
        self.setCentralWidget(splitter_h)
        
        # splitter_v vertical panel in the rhs horizontal panel.
        splitter_v = QtWidgets.QSplitter()
        splitter_v.setOrientation(QtCore.Qt.Orientation.Vertical)    
        
        # Create the text edit for the 1st tab in the splitter_h
        self.textedit = QtWidgets.QTextEdit()
        self.textedit.setStyleSheet("""
                font: 12pt Monospace;
                border-width: 1px;
                """) # margin: 5px;
        self.textedit.setText("")  
        self.textedit.setText("This is in the textedit tab. for Pyside6 Info.")
 
        # TODO: Strange doesn't work
        #  Provide keyboard shortcut zooming of the textedit.
        # Conflicts with web-browser zooming if + and - are used. Use Ctrl i and o
        QtGui.QShortcut("Ctrl+i", self, activated=lambda: self.textedit.zoomIn())
        QtGui.QShortcut("Ctrl+o", self, activated=lambda: self.textedit.zoomOut())         
             

        ##### Create the Browser for displaying the code in html form  #####
        self.code_browser = QtWebEngineWidgets.QWebEngineView()
        self.code_browser.setPage(CustomWebEnginePage(self))        
        self.code_browser.setZoomFactor(1.2)
      
        #  Provide keyboard shortcut zoom-in -out -reset of the WebEngineView.
        QtGui.QShortcut("Ctrl++", self, activated=lambda:
                  self.code_browser.setZoomFactor(self.code_browser.zoomFactor() + 0.2))
        QtGui.QShortcut("Ctrl+-", self, activated=lambda:
                  self.code_browser.setZoomFactor(self.code_browser.zoomFactor() - 0.2))
        QtGui.QShortcut("Ctrl+0", self, activated=lambda: self.code_browser.setZoomFactor(1))
        # Quit. Shortcut.
        QtGui.QShortcut("Ctrl+q", self, activated=lambda: self.close())          
        
        # Test load data to the Browser
        #url = QtCore.QUrl.fromLocalFile(Path.cwd().as_posix() + "/test_pig_1.html")        
        #print(url) # PySide6.QtCore.QUrl('file:///home/ian/pyside6/test_pig_1.html')
        #self.code_browser.load(url)
        self.code_browser.setHtml("Use the search to locate desired string in python code.")
        
        # Add tabs to the left horizontal splitter panel.
        self.tabs = QtWidgets.QTabWidget()
        self.tabs.addTab(self.textedit, "PySide6 Information")          
        self.tabs.addTab(self.code_browser, "Python Code")   
        
        #  Provide keyboard shortcut zooming of the textedit.
        # Conflicts with web-browser zooming if + and - are used. Use Ctrl i and o
        #QtGui.QShortcut("Ctrl+i", self, activated=lambda: self.textedit.zoomIn())
        #QtGui.QShortcut("Ctrl+o", self, activated=lambda: self.textedit.zoomOut())              
        
        splitter_h.addWidget(self.tabs)
        # Add v splitter on rhs of h splitter
        splitter_h.addWidget(splitter_v) 
        
        ##### Inserted from  pyside6-help ######      
        label = QtWidgets.QLabel()
        label.setText("Search PySide6...")
        splitter_v.addWidget(label)        
        search_field = QtWidgets.QLineEdit()
        search_field.setClearButtonEnabled(True) 
        search_field.setPlaceholderText("Enter 4+ Characters...")
        # Use lambda to pass variables with the call.
        search_field.textChanged.connect(lambda x: self.search_changed(x, dictionary, listing))          
        splitter_v.addWidget(search_field)
        
        self.setStyleSheet("""
                margin: 1px;
                """)        
        '''
        splitter_v.setStyleSheet("""
                border-width: 15px;
                border-radius: 4px;
                background-color: red;
                """) # border-style: outset;
        splitter_h.setStyleSheet("""
                border-width: 15px;
                border-radius: 4px;
                """)
        '''                  
        self.list_widget = QtWidgets.QListWidget()
        self.list_widget.clicked.connect(self.search_list_clicked)
        splitter_v.addWidget(self.list_widget)

        tree_widget = QtWidgets.QTreeWidget()       
        splitter_v.addWidget(tree_widget)        
        tree_widget.clear()
        tree_widget.setHeaderLabel(HEADING)        
        tree_widget.setColumnCount(1)
        tree_widget.clicked.connect(self.treewidget_clicked)
        self.fill_tree_widget_item(tree_widget.invisibleRootItem(), dictionary)        

        # Create the examples tree and add it as bottom item on splitter_v
        for item in BAD_LIST:
            example_list.remove(item)        
        tree_dict = self.create_example_tree_dict(example_list)
              
        tree_example = QtWidgets.QTreeWidget() 
        #tree_example = QTreeWidget() 
        #tree_example.setMinimumHeight(500) #resize(200,500)             
        splitter_v.addWidget(tree_example)        
        #tree_example.clear()
        tree_example.setHeaderLabel("Run Example Programs")        
        tree_example.setColumnCount(1)
        #tree_example.clicked.connect(self.tree_example_clicked)
        tree_example.clicked.connect(lambda x: self.tree_example_clicked(x, example_path))       
        self.fill_tree_example_item(tree_example.invisibleRootItem(), tree_dict)         
        #self.setCentralWidget(tree_example)

        splitter_h.setStretchFactor(0,4)
        splitter_h.setStretchFactor(1,3) 
 
        splitter_v.setStretchFactor(0,1)
        splitter_v.setStretchFactor(1,1)       
        splitter_v.setStretchFactor(2,1)
        splitter_v.setStretchFactor(3,1)
                
        self.textedit.setText(WELCOME + MESSAGE_1 + MESSAGE_2)       

        # Statusbar
        self.find_text = ""
        self.match_position = 0
        self.match_total = 0
        #True        
        
        self.sb = QtWidgets.QStatusBar()
        self.setStatusBar(self.sb)
        # HBox doesn't work on Status bar.
        #hbox = QtWidgets.QHBoxLayout()
        #self.sb.addWidget(hbox)
        # TypeError: 'PySide6.QtWidgets.QStatusBar.addWidget' called with wrong argument types:
        #PySide6.QtWidgets.QStatusBar.addWidget(QHBoxLayout)
        self.find = QtWidgets.QLineEdit()
        self.find.setClearButtonEnabled(True)  
        self.find.setPlaceholderText("Find...")
        self.find.setStyleSheet("""
                width: 150px;
                max-width: 160px;
                """)
                #border-width: 10px;
                #padding-bottom: 5px;
                #""")
                   
        self.find.textChanged.connect(lambda x: self.find_changed(x)) #, dictionary, listing))         
        self.sb.addWidget(self.find)

        sb_up = QtWidgets.QPushButton()
        sb_up.clicked.connect(self.sb_up_clicked)
        pixmapi = getattr(QtWidgets.QStyle.StandardPixmap, "SP_ArrowUp")
        icon = self.style().standardIcon(pixmapi)
        sb_up.setIcon(icon)               
        self.sb.addWidget(sb_up)

        sb_down = QtWidgets.QPushButton()
        sb_down.clicked.connect(self.sb_down_clicked)
        pixmapi = getattr(QtWidgets.QStyle.StandardPixmap, "SP_ArrowDown")
        icon = self.style().standardIcon(pixmapi)
        sb_down.setIcon(icon)        
        self.sb.addWidget(sb_down) 
        
        self.sb_checkbox = QtWidgets.QCheckBox()
        self.sb_checkbox.setText("Case Sensitive")
        self.sb_checkbox.clicked.connect(self.sb_match_case_changed)
        self.case_sensitive = self.sb_checkbox.isChecked() 
        
        self.sb.addWidget(self.sb_checkbox)
        
        self.sb_label = QtWidgets.QLabel()
        self.sb_label.setText("{} of {} matches".format(self.match_position,self.match_total))  
        self.sb.addWidget(self.sb_label)             
        #self.addWidget(self.sb)
        #splitter_v.addWidget(self.sb)
        
        # Display Icons included with PySide6
        # https://www.pythonguis.com/faq/built-in-qicons-pyqt/
        self.sb_button = QtWidgets.QPushButton()
        self.sb_button.setText("Icon View")
        #self.sb_button.clicked.connect(self.sb_button_icon_view)
        self.sub_window = SubWindow()
        self.sb_button.clicked.connect(self.sub_window.show)   
        self.sb.addWidget(self.sb_button)

        # Add a spacer to right justify the Search widgets. Not supported
        #spacer = QtWidgets.QSpacerItem(2, 4, QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.MinimumExpanding)
        #self.spacer = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        #self.sb.addWidget(self.spacer)
        #TypeError: 'PySide6.QtWidgets.QStatusBar.addWidget' called with wrong argument types:
        #PySide6.QtWidgets.QStatusBar.addWidget(QSpacerItem)

        # Add a label to pack toward the right:
        self.sb_label_2 = QtWidgets.QLabel()
        self.sb_label_2.setText("Search in Python code:")  
        self.sb.addWidget(self.sb_label_2) 
                
        ##### Search for code examples to list 10 lines of in code tab window. #####        
        self.search = QtWidgets.QLineEdit()
        self.search.setClearButtonEnabled(True)  
        self.search.setPlaceholderText("Find...")
        self.search.setStyleSheet("""
                width: 150px;
                max-width: 160px;
                """)
                #border-width: 10px;
                #padding-bottom: 5px;
                #""")
                   
        self.search.textChanged.connect(lambda x: self.search_str_changed(x, code_dict)) 
        #self.search_str.textChanged.connect(lambda x: self.search_str_changed(x, dictionary, listing)) 
        #, dictionary, listing))         
        self.sb.addWidget(self.search)
        
        # Add a message label to pack toward the right:
        self.sb_label_3 = QtWidgets.QLabel()
        self.sb_label_3.setText("")  
        self.sb.addWidget(self.sb_label_3)             
        
    ##### Functions that are part of the MainWindow #####
    ##### 3 x Methods for tree examples to run programs
    
    def create_example_tree_dict(self, example_list):
        """
        Using example_list, create a dictionary to feed to the Tree Widget
        Tree normally has two levels of dictionary and then a list of programs.
        E.g. 30 items in top level.
        """    
        tree_dict = {}
        for index, path_file in enumerate(example_list):
            path_file_list = path_file.split("/")
            # Remove the None field at the begining...
            path_file_list.pop(0)
            # Get the top-level key
            key = path_file_list.pop(0)
            
            # Remove the last item, python filename.
            python_file = path_file_list.pop(-1)
          
            # Create the sub-key from the remaining items in the list.             
            path_file_str = "/".join(path_file_list)

            # Commence building the tree_dict. Add the primary keys
            if not key in tree_dict:
                tree_dict[key] = {}
            # Add the sub-keys    
            if path_file_str not in tree_dict[key]:
                tree_dict[key].update({path_file_str:[]})
            # Append the list of python files.
            tree_dict[key][path_file_str].append(python_file) 
        
        # Restore tree_dict to string           
        #print(tree_dict)
        count = 0
        for key, value_dict in tree_dict.items():
            #print(key, value_dict)
            for sub_key, value_list in value_dict.items():
                for python_file in value_list:
                    if sub_key == "":
                        string = "/" + key + "/" + python_file 
                    else:
                        string = "/" + key + "/" + sub_key + "/" + python_file
                    #print(string)
                    # Checks...
                    count += 1
                    #if string not in example_list:
                    #    print("Missing:", string)       
        #print(count) # 284       
        return tree_dict

        """
        # Check: Restore tree_dict to string           
        #print(tree_dict)
        count = 0
        for key, value_dict in tree_dict.items():
            #print(key, value_dict)
            for sub_key, value_list in value_dict.items():
                for item in value_list:
                    if sub_key == "":
                        string = "/" + key + "/" + item 
                    else:
                        string = "/" + key + "/" + sub_key + "/" + item 
                    print(string)
                    # Checks...
                    count += 1
                    if string not in example_list:
                        print("Missing:", string)       
        print(count) # 284
        """

    def fill_tree_example_item(self, invisible_root_item, dictionary):
    
        for top_key, sub_dict in dictionary.items():
            
            # Dictionaries: 'QDomText': ['EncodingPolicy', 'NodeType', ...'toText']}
        
            parent = QtWidgets.QTreeWidgetItem([str(top_key)])
            #parent = QTreeWidgetItem([str(top_key)])            
            parent.setFlags(parent.flags() & ~ QtCore.Qt.ItemFlag.ItemIsSelectable) 
            #parent.setFlags(parent.flags() & ~ Qt.ItemFlag.ItemIsSelectable)            
            # In qt6, .flags() replaced by pyqtEnum(enum) ???
            
            invisible_root_item.addChild(parent) 
                                                              
            for sub_key, python_file_list in sub_dict.items(): 
                child = QtWidgets.QTreeWidgetItem([str(sub_key)])
                #child = QTreeWidgetItem([str(sub_key)])
                child.setFlags(child.flags() & ~ QtCore.Qt.ItemFlag.ItemIsSelectable) 
                #child.setFlags(child.flags() & ~ Qt.ItemFlag.ItemIsSelectable)                 
                parent.addChild(child) 
                       
                #print(len(python_file_list))
                for method in python_file_list:
                    # The Python files are defaulted to ItemIsSelectable.
                    grandchild = QtWidgets.QTreeWidgetItem([str(method)])
                    #grandchild = QTreeWidgetItem([str(method)])                    
                    child.addChild(grandchild)

                #print(dictionary[top_key][sub_key])
                   
    def tree_example_clicked(self, model_index, example_path):
        """
        The parent, child or grand-child has been clicked in QListWidget.
        Build a list
        """
        #print(model_index) 
        #print(model_index.flags().value) # 60 parent or 61 child        
        # Check is ItemIsSelectable based on model_index.flags()
        if not model_index.flags() & QtCore.Qt.ItemFlag.ItemIsSelectable:
        #if not model_index.flags() & Qt.ItemFlag.ItemIsSelectable:        
            #print("Item is not selectable")
            return
            
        item_list = []
        item_list.append(model_index.data())
        
        # Potential for between 1 to 3 levels above.
        try:
            parent = model_index.parent()
            if parent.data():
                item_list.insert(0, parent.data())
        except:
            pass

        try:            
            grandparent = parent.parent()
            if grandparent.data():
                item_list.insert(0, grandparent.data())
        except:
            pass
         
        #print(item_list) 
        item_str = "/" + "/".join(item_list)
        #print(item_str)
        
        # Full path and program name
        program = example_path + item_str        
       
        # Remove the filename form the itemlist
        python_file = item_list.pop(-1)

        directory = example_path + "/" + "/".join(item_list)        
        dir_path = Path(directory)
        files = dir_path.rglob('*') 
        # files.sort() # AttributeError: 'generator' object has no attribute 'sort'
        # print(type(files)) # <class 'generator'>

        # Convert from generator list to normal list.
        # Remove __pycache__ related files.
        file_list = []
        for file in files:
            if "__pycache__" not in file.as_posix():         
                file_list.append(file.as_posix())
        file_list.sort()     
           
        #print(file_list)
        #print(type(file_list))
        #print(len(file_list))
    
        # Build the html string of code for displaying by the web_browser.    
        html_str = "" 
        for file in file_list:
            if file.endswith(".py"):
                #print(file)
                lexer = PythonLexer()

                #style = get_style_by_name('friendly') 
                #style = get_style_by_name('github-dark')     
                #style = get_style_by_name('paraiso-dark')
                #style = get_style_by_name('tango')  
                #style = get_style_by_name('native')
                #style = get_style_by_name('colorful')
                style = get_style_by_name('default')
                #style = get_style_by_name('algol')
                
                formatter = HtmlFormatter(full=True, style=style, linenos=True)
                
                with open(file, "r") as fin:
                    python_code = fin.read()

                # Add to html string the path and filename, and the code.
                html_str += "<h4 style='color:chartreuse;'>{}</h4>".format(file) 
                html_str += highlight(python_code, lexer, formatter)

        # Add the list of files for this example program.
        html_str += "<h4>Files in example directory:</h4>"
        html_str += "<p style='color:chartreuse;font-size:12px;'>{}</p>".format(example_path)              
        for file in file_list:
            html_str += "<p style='color:yellow;font-size:12px;'>{}</p>".format(file)       

        # TODO: The follow 2 lines of code appear to run in reverse order!
        # Update the code_browser with the html string.    
        self.code_browser.setHtml(html_str)
        # Use subprocess to run the example program.
        run(['python', program])
             
    ##### Search #####        
    def search_str_changed(self, search_str, code_dict):
        """
        Search dictionary code for match.
        Build a string. 
        Convert to pigmented html
        Display in a seperate window.
        """        
        #print(search_str)
        # Make the search string global.  Huh? 
        self.search_str = search_str
        
        if len(search_str) < 3:
            self.sb_label_3.setText("")
            return    
        
        document = self.search_code_dict(code_dict, search_str)
        #print(document)
        document_list = document.split("\n")
        #print("len(document_list)):", len(document_list), "len(document_list)/12:", (len(document_list)-1)//12)
        if (len(document_list)-1)//12 > 100:
            # TODO: Add label with search result status        
            #print("Refine search: {} matches".format((len(document_list)-1)//12))
            self.sb_label_3.setText("Refine search: {} matches".format((len(document_list)-1)//12))
            return
        
        # Convert the document. to HTML
        #print("Search: '{}' has {} matches".format(search_str, (len(document_list)-1)//12))
        self.sb_label_3.setText("{} matches".format((len(document_list)-1)//12))        
        self.convert_search_results_to_html(document)
        return
        
        
        
    def convert_search_results_to_html(self, document):        
        """
        Convert the document to html data for displaying in WebEngineView browser.
        """            
        lexer = PythonLexer()

        #style = get_style_by_name('friendly')        
        #style = get_style_by_name('native')
        #style = get_style_by_name('colorful')
        style = get_style_by_name('default')
        
        formatter = HtmlFormatter(full=True, style=style, linenos=True, 
                title="Python Code Examples")
 
        # Create the html, but it will not have correct navigation links to the html files.
        document_html_draft = highlight(document, lexer, formatter)
            
        # Edit the html to create the navigation links
        document_html = self.add_html_navigation_links(document_html_draft)
        
        self.code_browser.setHtml(document_html)
                
    def add_html_navigation_links(self, draft_html):
        prefix = '<a href="file:///'
        suffix = '</a>'
                
        draft_html_list = draft_html.split("\n")
        final_html_list = []
        for line in draft_html_list:
            #print(line)

            if line.startswith('<span class="c1"># '):
                #print(line[:-1])
                # <span class="c1"># charts/areachart/areachart.py</span>
                # .py needs to be changed to .html
                beginning = line.split(" ")[0] + " " + line.split(" ")[1] + " "
                link_click = line.split(" ")[2]
                link_click, _, _ = link_click.partition("</span>") # link_click.split("</span>")[0]
                # .py is changed to .html
                link_click = link_click[:-2] + "html"
                ending = "</span>"
                #print(beginning)
                #print(link_click)
                #print(ending)           
                full_path = "/home/ian/pyside6/example_html/"
                new_line = beginning + ending + prefix + full_path + link_click + '">' + link_click + "</a>"
                
                #print(new_line)
                final_html_list.append(new_line)

            else:
                final_html_list.append(line)
        
        final_html_str = "\n".join(final_html_list)
        return final_html_str
                 

    def search_code_dict(self, code_dict, search_string):
        """
        Search all code for match of a string. 
        Display: File name, link to file name, code line, and 5 lines preceeding and after.
        Maintain an 11 line buffer 0 to 4 preceeding lines, 5 is focus line, 6 to 10 post lines
        """
        global python
        
        document = ""
        for file, code_list in code_dict.items():
            #print(file)
            
            # Run a 10 line buffer.
            buffer_list = []
            code_line_total = len(code_list)
            #print("code_line_total:", code_line_total)
            for index, line in enumerate(code_list):
                buffer_list.append(line)
                #TODO build this up. start at 5 lines for match in first line.
                if index < 9:
                    continue
                if index == 9:
                    # search lines 0 to 4
                    for i in range(5):
                        string = self.search_line(buffer_list, file, search_string, i)

                #if index > 9 and index <= code_line_total - 1: # 10 to 35 out of 40
                if index > 9 and index < code_line_total: # 10 to 35 out of 40            
                    buffer_list.pop(0) # keep list length at 10
                    # search line 5th line, index of 4
                    if index < code_line_total:
                        string = self.search_line(buffer_list, file, search_string, 4) 
                    
                    # Last search when index has reached max
                    if index == code_line_total -1: # This is the last loading of the buffer
                        #print("reach code line total")
                        # Wind this down
                        # check the search string in the last 5 lines of the buffer_list              
                        for i in range(5):           
                            buffer_list.pop(0)
                            string = self.search_line(buffer_list, file, search_string, 4)
                if string:
                    pass
                    #print(string)
                if string:    
                    document += string
                    
                    """
                    # OK with both TextEdit and TextBrowser
                    python.moveCursor(QtGui.QTextCursor.MoveOperation.End, 
                        QtGui.QTextCursor.MoveMode.MoveAnchor)  # Moves cursor to the end OK.
                    print(python.insertPlainText(string)) # 
                    print("done") # This is quick
                                    
                    # TODO: Pass strinf each time and append QTextEdit - still slow
                    # Try and Html window. can include links.
                    """
        #print(document) # pass document to highlighter.
        #print(type(python)) # <class 'PySide6.QtWidgets.QTextEdit'>

        return document

    def search_line(self, buffer_list, file, search_string, focus_line_index):
        """
        Build the string of the 10 line code samples.
        """
        string = ""
        if search_string in buffer_list[focus_line_index]:
            #print("Found in line:", focus_line_index, buffer_list[focus_line_index], buffer_list[0], buffer_list[-1], len(buffer_list))
            
            string += ("#" + "="*80 + "\n")
            string += ("# " + file + "\n") # + " ~ Searching for: " + search_string + "\n")
            for line in buffer_list:        
                string += line + "\n"
                
                

            #print(string)        
            return string
            #print(string)
            
            """
            print("="*80)
            print(file) # + " ~ Searching for: " + search_string)
            print()        
            for line in buffer_list:
                print(line)
            """
            
    ##### End of building 11 line string #####    


    def sb_match_case_changed(self, is_checked):
        """
        Case sensitive checkbox default to passing to callback its boolean status.
        """
        if is_checked:
            self.case_sensitive = True
        else:
            self.case_sensitive = False
        
        # Call a refresh of the matching statistics.   
        self.find_changed(self.find_text)           
        
    def perform_search(self, find_text, is_case_sensitive=False, is_backward=False):
        """
        Perform a search of self.text_edit, dependent on search directiom and if 
        search is case sensitive.
        Return status of the success of the search. Bool.
        Notes:       
        FindBackward = <FindFlag.FindBackward: 1>
        FindCaseSensitively = <FindFlag.FindCaseSensitively: 2>
        FindWholeWords = <FindFlag.FindWholeWords: 4>        
        """        
        if is_case_sensitive and is_backward:
            find_status = self.textedit.find(self.find_text, 
                    QtGui.QTextDocument.FindFlag.FindBackward | 
                    QtGui.QTextDocument.FindFlag.FindCaseSensitively )
        elif is_backward: # and case insensitive
            find_status = self.textedit.find(self.find_text, 
                    QtGui.QTextDocument.FindFlag.FindBackward)              
        elif is_case_sensitive: # and search forwards
            find_status = self.textedit.find(self.find_text,
                    QtGui.QTextDocument.FindFlag.FindCaseSensitively )            
        else: # Case insensitive and search farwards
            find_status = self.textedit.find(self.find_text)        
         
        return find_status 

    def sb_up_clicked(self, button):
        """
        Callback when clicked on Up Arrow icon in Status Bar search. 
        """
        self.backward = True
        if self.perform_search(self.find_text, self.case_sensitive, self.backward):
            self.match_position -= 1                          
            self.sb_label.setText("{} of {} matches".format(self.match_position, 
                    self.match_total))  
        else:
            #print("Not found")
            # Wrap around to the start 
            self.textedit.moveCursor(QtGui.QTextCursor.MoveOperation.End, 
                    QtGui.QTextCursor.MoveMode.MoveAnchor )
            #find_status = self.textedit.find(self.find_text)
            self.match_position = self.match_total
            
            if self.perform_search(self.find_text, self.case_sensitive, self.backward):              
                self.sb_label.setText("{} of {} matches".format(self.match_position, 
                        self.match_total)) 
            else:
                # NO MATCH EXISTS
                self.sb_label.setText("{} of {} matches".format(self.match_position, 
                        self.match_total)) 
                return                
      
    def sb_down_clicked(self, button):
        """
        Callback when clicked on Down Arrow icon in Status Bar search.
        """ 
        if self.perform_search(self.find_text, self.case_sensitive):
            self.match_position += 1                          
            self.sb_label.setText("{} of {} matches".format(self.match_position, 
                    self.match_total))         
        else:
            #print("Not found")
            # Wrap around to the start 
            self.textedit.moveCursor(QtGui.QTextCursor.MoveOperation.Start, 
                    QtGui.QTextCursor.MoveMode.MoveAnchor )
            #find_status = self.textedit.find(self.find_text)
            self.match_position = 0  
            if self.perform_search(self.find_text, self.case_sensitive):
                self.match_position += 1            
              
                self.sb_label.setText("{} of {} matches".format(self.match_position, 
                        self.match_total)) 
            else:
                # NO MATCH EXISTS
                self.sb_label.setText("{} of {} matches".format(self.match_position, 
                        self.match_total)) 
                return                
    
    def find_changed(self, find_text):
        """
        Call-back for each time a character is entered in sb_find - QLineEdit
        find_text in self.textedit and count total number of matches.
        Calls perform_search to advance search to next match.
        Establishes: self.match_total, self.match_position, self.find_text
        """
        # Make the search string global.   
        self.find_text = find_text
        
        if len(find_text) < 2:
            return
        
        self.match_total = 0
        self.match_position = 0
        
        # Move cursor to Start. - Test with KeepAnchor
        self.textedit.moveCursor(QtGui.QTextCursor.MoveOperation.Start, 
                QtGui.QTextCursor.MoveMode.MoveAnchor) 

        # Count the total number of matches.
        #position_list = []  # For testing the matching.       
        while True:

            if self.perform_search(find_text, self.case_sensitive):
                self.match_total += 1
                #position_list.append(self.textedit.textCursor().position()) 
            else:
                # Reached last match at bottom of the text
                break

        # Return to start / top of text.
        self.textedit.moveCursor(QtGui.QTextCursor.MoveOperation.Start, 
                QtGui.QTextCursor.MoveMode.MoveAnchor) 

        # Update the matches label. match_position is 0
        self.sb_label.setText("{} of {} matches".format(self.match_position, 
                self.match_total))         
        #print("Position list:", position_list)  # Position list: [160, 294]

        # Find first match, going forward from start / top of text.                    
        if self.perform_search(find_text, self.case_sensitive):
            self.match_position += 1            
        
        # Update the matches label. match_position should be 1
        self.sb_label.setText("{} of {} matches".format(self.match_position, 
                self.match_total))            

        
    def search_changed(self, search_text, dictionary, listing): 
        """
        Callback for when characters are enterd in primary search QLineEdit. 
        """
        # Passed the dictionary (qt6_dict) and listing (qt6_list)       
        # Don't do any searches until 4th character is entered.
        if len(search_text) <= 3:
            return  
    
        self.list_widget.clear()

        # Case insensitive search.        
        # Search the listing. If search string contains a "."
        if "." in search_text:
            for string in listing:
                if search_text.lower() in string.lower():
                    self.list_widget.addItem(string)
        
        # Search in dictionary seperately in modules, classes and methods.
        else:
            # 1st level search - Modules. (Under PySide6 library)
            for module, class_dict in dictionary.items():        
                if search_text.lower() in module.lower():
                    self.list_widget.addItem("PySide6." + module)
                    
                # 2nd Level search - Classes
                for class_name, method_list in class_dict.items():
                    if search_text.lower() in class_name.lower():
                        self.list_widget.addItem("PySide6." + module + "." + class_name)
                                
                    # 3rd level search - Methods
                    for method in method_list:
                        if search_text.lower() in method.lower(): 
                            self.list_widget.addItem("PySide6." + module + "." +
                                class_name + "." + method)                        
                
          
    def search_list_clicked(self, model_index):
        """
        Callback when click on item in QListWidget
        """
        item = model_index.data()
        item_list = item.split(".")
        self.setWindowTitle("PySide6 Help - Selection: {}".format(item)) 

        string_1 = ""
        if len(item_list) > 2:
            string_1 = "\n\nfrom PySide6.{} import {}\n".format(item_list[1], item_list[2])

        # get the help data         
        string_2 = display_pyside6_help(item_list)
        
        self.textedit.setText(item + string_1 + string_2)       

        #string = display_pyside6_help(item_list) 
        #self.textedit.setText(string)         
                      
    def fill_tree_widget_item(self, invisible_root_item, dictionary):
        for top_key, class_dict in dictionary.items():
            
            # Dictionaries: 'QDomText': ['EncodingPolicy', 'NodeType', ...'toText']}
        
            parent = QtWidgets.QTreeWidgetItem([str(top_key)])
            #parent.setFlags(parent.flags() & ~ QtCore.Qt.ItemFlag.ItemIsSelectable) 
            # In qt6, .flags() replaced by pyqtEnum(enum) ???
            invisible_root_item.addChild(parent) 
            
                                                   
            for class_name, method_list in class_dict.items(): 
                child = QtWidgets.QTreeWidgetItem([str(class_name)])
                #child.setFlags(child.flags() & ~ QtCore.Qt.ItemFlag.ItemIsSelectable) 
                parent.addChild(child) 
                       
                #print(len(method_list))
                for method in method_list:
                    grandchild = QtWidgets.QTreeWidgetItem([str(method)])
                    child.addChild(grandchild)

                #print(dictionary[top_key][class_name])
                   
    def treewidget_clicked(self, model_index):
        """
        The parent, child or grand-child has been clicked in QListWidget.
        Build a list
        """
        #print(model_index) # PySide6.QtCore.QModelIndex object
        #print(model_index.flags().value) # 60 parent or 61 child        
        # Check is ItemIsSelectable based on model_index.flags()
        if not model_index.flags() & QtCore.Qt.ItemFlag.ItemIsSelectable:
            #print("Item is not selectable")
            return
            
        item_list = []
        item_list.append(model_index.data())
        
        # Potential for between 1 to 3 levels above.
        try:
            parent = model_index.parent()
            if parent.data():
                item_list.insert(0, parent.data())
        except:
            pass

        try:            
            grandparent = parent.parent()
            if grandparent.data():
                item_list.insert(0, grandparent.data())
        except:
            pass
                
        # Insert the root of the tree
        item_list.insert(0, "PySide6")
        item_str  = ".".join(item_list)
        
        self.setWindowTitle("PySide6 Help - Selection: {}".format(item_str))        
        
        string_1 = ""
        if len(item_list) > 2:
            string_1 = "\n\nfrom PySide6.{} import {}\n".format(item_list[1], item_list[2])

        # get the help data         
        string_2 = display_pyside6_help(item_list)
        
        self.textedit.setText(item_str + string_1 + string_2) 


 

class CustomWebEnginePage(QtWebEngineCore.QWebEnginePage):
    """
    Links in the WebEngineView Browser, "code_browser", are to HTML files. 
    Open a WebEngineView, "html_window", and display the html file.  
    """
    # Store second window.
    html_window = None
    def acceptNavigationRequest(self, url,  _type, isMainFrame):
        #print(url, _type, isMainFrame)
        # PySide6.QtCore.QUrl('file:///home/ian/pyside6/test_pig_1.html') 
        # PySide6.QtWebEngineCore.QWebEnginePage.NavigationType.NavigationTypeTyped 
        # True        
        #html_window = None
            
        if _type == QtWebEngineCore.QWebEnginePage.NavigationTypeLinkClicked:
        
            if not self.html_window:
                self.html_window = QtWebEngineWidgets.QWebEngineView()

            self.html_window.setUrl(url)
            self.html_window.setZoomFactor(1.4)
            #print(type(self.html_window))
            #print(dir(self.html_window)) 
            self.html_window.resize(1000,600)
            # Position of widgets when launched.
            self.html_window.move(500,200)           
            
            #  Provide keyboard shortcut zooming of the WebEngineView.
            QtGui.QShortcut("Ctrl++", self.html_window, activated=lambda:
                      self.html_window.setZoomFactor(self.html_window.zoomFactor() + 0.2))

            QtGui.QShortcut("Ctrl+-", self.html_window, activated=lambda:            
                      self.html_window.setZoomFactor(self.html_window.zoomFactor() - 0.2))

            QtGui.QShortcut("Ctrl+0", self.html_window, activated=lambda: self.html_window.setZoomFactor(1))
            # Quit. Shortcut. Doesn't work. screws up shortcuts
            #QtGui.QShortcut("Ctrl+q", self.html_window, activated=lambda: self.html_window.close())             
            
            self.html_window.show()
                        
            return False

        return super().acceptNavigationRequest(url,  _type, isMainFrame) 


class SubWindow(QtWidgets.QWidget):
    """
    Open a window and display the Qt6 supplied icons with their names in a grid.
    """
    def __init__(self):
        super(SubWindow, self).__init__()
        self.setWindowTitle("PySide6 Icons")
        self.setWindowIconText("Icons")
        pixmapi = getattr(QtWidgets.QStyle.StandardPixmap, "SP_TitleBarMenuButton")
        icon = self.style().standardIcon(pixmapi)
        self.setWindowIcon(icon)        
        
        icons = sorted([attr for attr in dir(QtWidgets.QStyle.StandardPixmap) 
                if attr.startswith("SP_")])
        
        layout = QtWidgets.QGridLayout()

        #TODO: Add title to window, icon, close button, and textbox to explain.
        text_edit = QtWidgets.QTextEdit()
        text_edit.setText(ICON_MESSAGE)
        text_edit.setMinimumHeight(140)
        layout.addWidget(text_edit, 0,0,1, 4)  # row, col, rowspan, colspan, Qt.AlignmentFlag

        for n, name in enumerate(icons):
            btn = QtWidgets.QPushButton(name)

            pixmapi = getattr(QtWidgets.QStyle.StandardPixmap, name)
            icon = self.style().standardIcon(pixmapi)
            btn.setIcon(icon)
            layout.addWidget(btn, (n+4) // 4, (n+4) % 4)

        self.setLayout(layout)


# Functions shared by both Window classes and initial launch code.
def display_pyside6_help(item_list):
    """
    Build the string that is displayed in the textview panel.
    Only provide two levels of help. Current and one above.
    """
    level_current = ".".join(item_list)
    #print(level_current)
    
    item_list.pop()
    level_1_up = ".".join(item_list)
    #print(level_1_up)    
            
    # Get the help information strings
    level_current_str = get_help(level_current)
    level_1_up_str = get_help(level_1_up)
                 
    # Build text and display
    string = "\n" + "=" * 100 + "\n"
     
    string += level_current + ":\n"
    string += "\n" + level_current_str
    string += "\n" + "=" * 100 + "\n"

    string += level_1_up + ":\n"
    string += "\n" + level_1_up_str
    string += "\n" + "=" * 100 + "\n"    
    
    return string
    
    
def get_help(func):
    """
    Write the output of help() to a text buffer and return as text string.
    Usage example: get_help("PySide6.QtCore")
    Requires: contextlib and io.StringIO
    """
    output = StringIO()
    with contextlib.redirect_stdout(output):
        help(func)       
    contents = output.getvalue()
    output.close()
    return contents
        
        
# Initial setup of html files.
def convert_example_files_to_html(code_dict):
    """
    Create a /examples_html/ folder off the cwd.
    Get PySide example python files and convert to html.
    Place in subdirectories off the /examples_html/ folder.
    
    Requires:
    from pathlib import Path, PurePath
    from pygments import formatter, highlight
    from pygments.lexers import PythonLexer
    from pygments.formatters.html import HtmlFormatter
    from pygments.styles import get_style_by_name    

    Also needed, for locating example files...
    import PySide6.QtCore as QtCore    
    """
    print("If required, converting python example files to html files...")      
    # Use QtCore.__file__ to get the main path, then add examples
    py_path = PurePath(QtCore.__file__).parent.as_posix() + "/examples"
    #print(py_path)
    # /home/ian/venv-pyside6/lib/python3.10/site-packages/PySide6/examples            
    folder = "example_html"

    # Create sub directory off cwd for html files.     
    Path(folder).mkdir(parents=True, exist_ok=True)
 
        
    # Creqte the full path for the copy from...
    for path_file, code_list in code_dict.items():
        #print(path_file) 
        
        # Output_path is required to later create it is not already exists
        output_path = folder + Path(path_file).parent.as_posix()

        # Create destination path and filename, with .py extension replaced with .html
        path_file_html = path_file[:-3] + ".html"        
        
        # Create source path and .py file and destination path and .html file
        source = py_path + path_file
        destination = folder + path_file_html     
        #print("Source:", source)
        #print("Destination:", destination)           
        # Source: /home/ian/venv-pyside6/lib/python3.10/site-packages/PySide6/examples/xml/dombookmarks/dombookmarks.py
        # Destination: example_html/xml/dombookmarks/dombookmarks.html
        
        # Check if destination already exists. If so, then do not create it again.
        if not Path(destination).is_file():
            #with open(source) as fin:
            #    python_code = fin.read() 
            
            python_code = "\n".join(code_list)    
            #lexer = lexers.get_lexer_by_name('python')
            lexer = PythonLexer()

            #style = get_style_by_name('friendly')        
            #style = get_style_by_name('native')
            #style = get_style_by_name('colorful')
            style = get_style_by_name('default')
            
            formatter = HtmlFormatter(full=True, style=style, linenos=True, 
                    title="Python Code Examples")
            
            # Create the output directory path        
            Path(output_path).mkdir(parents=True, exist_ok=True)
            
            # Convert .py file to .html highlighted python file.           
            with open(destination, 'w') as fout:
                highlight(python_code, lexer, formatter, outfile=fout)        
            
            # 492 items, totalling 10.2 MB (10.8 MB on disk)        
        else:
            pass
            #print("Path and file already existed")


def get_full_path():
    """
    Build the full path to get to the examples files.
    Use QtCore as way of getting the root folder, which /examples/ is off.
    """    
    path = Path(QtCore.__file__).parent.as_posix()
    path += "/examples/"
    #print(path)
    return path


def is_examples_exist(example_path):
    return Path(example_path).exists()

 
def get_code_dict_using_path(full_path):
    """
    Given the full path and file names to all the example python files, return a 
    dictionary of the code. 
    The dictionary keys are the sub-path and file name.
    The dictionary values are a list of the lines of code.
    The code has had the copyright information lines striped from it.
    The python files with "_rc" or "rc_" in the name are not included.
    """
    code_dict = {}

    p = Path(full_path)
    #path_list = [x for x in p.iterdir() if x.is_dir()]
    #path_list.sort()
    
    #print(path_list)
    #print(len(path_list)) 
       
    count_1 = 0
    count_2 = 0   
    
    # Create a list of all python files. Note: list is PosixPath()  
    file_list = list(p.glob('**/*.py')) # 304
    file_list.sort()
    #print(file_list)
    
    # Remove the _rc or rc_ files from the file_list.    
    length = len(file_list)
    #print(length) #304
    for index, file in enumerate(reversed(file_list)):
        file_name = PurePath(file).name
        if "_rc" in file_name or "rc_" in file_name:
            #print(file_name)
            file_list.pop((length -1) - index)
    #print(len(file_list)) # 284 - removed 20 x rc files from list.
    
    # For each file add it to the dictionary
    #print(file_list)
    for file in file_list:
        count_1 +=1
        #print(file)
        #TODO: Make this independent of Pyside6 installation:
        #position = len("/home/ian/venv-pyside6/lib/python3.10/site-packages/PySide6/examples")
        position = len(full_path)        
        #print(position)
        file_path = Path(file).as_posix()  # Strip PosixPath() off the path
        file_path = "/" + file_path
        #print(file_path[position:])
        #print(PurePath(file).name)
        
        file_name = PurePath(file).name
        #file_name = "/" + file_name
        count_3 = 0
        
        code_list = []      
        with open(file, "r") as fin:
            temp_list = fin.readlines()                
            for temp_line in temp_list:
                # Build the lines of code, but remove copyright lines
                if not temp_line.startswith("#"):   
                    code_list.append(temp_line[:-1]) # strip off extra \n
                                    
            #count_2 += len(temp) # 304 3,209,120
            #print(count_1, len(temp_list), count_2, count_3)

        # Add key as truncated path/filename code as a list to the dictionary.    
        code_dict[file_path[position:]] = code_list                
    #print(count_1, len(temp_list), count_2, count_3)

    #print(len(file_list), count_2)
    
    return code_dict

# End of html files setup
# Initial setup / data collection routines, etc.
def build_dictionary(module_list):
    """
    Build the dictionary
    """
    count_0 = 0
    count_1 = 0
    count_2 = 0
    count_3 = 0

    qt6_dict = {}
    for module in module_list:
        if module.startswith("Qt"): 
            count_0 += 1 # 46
            qt6_dict[module] = {}      
    #print(len(qt6_dict))
    #print(qt6_dict)

    for module, classes in qt6_dict.items():
        classes_list = dir(eval(module))
        #print(classes_list)

        for subgroup in classes_list:
            count_1 += 1  # 1174
            qt6_dict[module].update ( {subgroup: None} ) 
            module_subgroup_str = module + "." + subgroup
            
            method_list = (dir(eval(module_subgroup_str)))
            count_2 += len(method_list)  # 107896
            qt6_dict[module][subgroup] = method_list        
            
    # Are the method_lists still attached, and dict is not independent.
    #print("Initial Dictionary. Modules:", count_0, "SubGroups:", count_1, 
    #       "Methods:", count_2) 
    #Initial Dictionary. Modules: 46 SubGroups: 1576 Methods: 177815                 
    return qt6_dict


def remove_classes_double_underscore(qt6_dict):
    """
    Remove any subgroup that starts with a double under. 
    E.g. QtBluetooth.__spec__  or QtCore.__doc__
    Notes: 
    No Group level starts with __
    This Works OK: print(qt6_dict['QtBluetooth']['__doc__'])
    RuntimeError: dictionary changed size during iteration <-- Therefore make a list 
    of deletions to make to the dictionary and then implement the list.            
    """
    count_0 = 0
    count_1 = 0

    for module, classes_list in qt6_dict.items():
        
        #if module.startswith("__"): #<-- Nothing at group level starts with __
            #print(module) # Nothing
        
        methods_to_delete_list = []
          
        for subgroup, method_list in classes_list.items():
            count_0 += 1  # 1174

            if subgroup.startswith("__"):
                # Build a list of subgroup to be deleted
                methods_to_delete_list.append(subgroup)
                count_1 += 1  # 175
                
        #print(methods_to_delete_list) # ['__doc__', '__file__', ... '__spec__']
        for item in methods_to_delete_list:
            del qt6_dict[module][item]
             
    #print("Double Unders Classes removed. SubGroups:", count_0, "Subgroups removed:", 
    #        count_1, "Remain:", count_0 - count_1)
    #Double Unders Classes removed. SubGroups: 1576 Subgroups removed: 280 Remain: 1296
    return qt6_dict
    

def remove_methods_double_underscore(qt6_dict):
    """
    Remove and the double_under from the methods list's. 
    Need to do reverse list popping
    """
    count_0 = 0
    count_1 = 0

    for group, classes in qt6_dict.items():
        for subgroup, method_list in classes.items():
            length = len(method_list)
            for index, method in enumerate(reversed(method_list)):
                count_0 += 1  #       
                if method.startswith("__"):
                    count_1 += 1  # 
                    method_list.pop((length-1) - index)

    #print("Double Unders removed from Methods. Initial:", count_0, "Removed", count_1, 
    #        "Remain:", count_0 - count_1)
    # Double Unders removed from Methods. Initial: 162093 Removed 34278 Remain: 127815
    return qt6_dict

    
def remove_methods_single_underscore(qt6_dict):    
    """
    Remove and the single_under from the methods list's
    """
    count_0 = 0
    count_1 = 0

    for group, classes in qt6_dict.items():
        for subgroup, method_list in classes.items():
            string = group + "." + subgroup
            #print(key, subkey, len(item_list), type(eval(string)))
            length = len(method_list)
            for index, method in enumerate(reversed(method_list)):
                count_0 += 1  # 
                string_1 = group + "." + subgroup + "." + method
                #print(string_1)        
                if method.startswith("_"):
                    count_1 += 1  # 
                    method_list.pop((length-1) - index)
    #print(qt6_dict)
    #print("Single Unders removed from Methods. Initial:", count_0, "Removed", count_1, 
    #        "Remain:", count_0 - count_1)
    # Single Unders removed from Methods. Initial: 127815 Removed 2 Remain: 127813
    return qt6_dict
 
        
def remove_no_type(qt6_dict):
    """
    Remove the items that don't have a type()
    """
    count_0 = 0
    count_1 = 0
    count_2 = 0
    count_3 = 0
    bad_type_list = []

    for key, value in qt6_dict.items():
        #print("\n" + key)
        for subkey, item_list in value.items():
            string = key + "." + subkey
            #print(type(eval(string)))
            
            length = len(item_list)
            for index, item in enumerate(reversed(item_list)):
                count_0 += 1
                string_1 = key + "." + subkey + "." + item
                #print(string_1)        
                try:
                    x = type(eval(string_1))
                    #print(string_1, x)
                except Exception as e:
                    #print(string_1)
                    count_1 += 1
                    #print(string_1, ":",  e)
                    
                    # Pop the failure from the list
                    item_list.pop((length-1) - index)
                    
                    bad_type_list.append(string_1)
                                   
    #print("No type() methods removed. Initial: ", count_0, "Removed:", count_1, 
    #            "Remain:", count_0 - count_1) 
    # No type() methods removed. Initial:  127813 Removed: 2 Remain: 127811
    #print(bad_type_list) 
    # ['QtMultimedia.QAudioDecoder.error.overload', 'QtWebSockets.QWebSocket.error.overload']
    return qt6_dict


def convert_dict_to_list(qt6_dict):
    """
    Provide a list from the dictionary so that a search can include a "." delimiter
    """    
    search_list = []
    for module, class_dict in qt6_dict.items():
        for class_name, methods_list in class_dict.items():
            for method in methods_list:
                search_list.append("PySide6." + module + "." + class_name + "." + method )                
    return search_list
    

def analyse_dictionary(qt6_dict):

    module_count = dir(qt6_dict)
    
    count_0 = 0
    count_1 = 0
    count_2 = 0
    for classes, classes_dict in qt6_dict.items():
        count_0 += 1
        for methods, method_list in classes_dict.items():        
            count_1 += 1
            count_2 += len(method_list)

    return "Modules:{} Classes:{} Total Attributes:{}".format(count_0, count_1, count_2)

def modify_example_list(example_list):
    """
    See which folders have a main.py and make this the only file in the folder
    available to have its code launched.
    """
    check_list = []
    for item in example_list:
        if item.endswith("main.py"):
            check_list.append(item)
    #print(check_list)
    #print(len(check_list))  # 51     
     
    # Remove other items in the folder with main.py 
    # Strip main.py
    for item in check_list:
        temp_list = item.split("/")
        file_name = temp_list.pop(-1)
        item_str = "/".join(temp_list)
        
        length = len(example_list)       
        for index, path in enumerate(reversed(example_list)):
            if item_str in path:
                example_list.pop((length-1) - index)
                
    #print(example_list)
    for item in example_list:
        pass
        #print(item)
    #print(len(example_list)) #150
    
    # Add back into example_list the main.py files...
    example_full_list = example_list + check_list
    example_full_list.sort()
    for item in example_full_list:
        pass
        #print(item)
        
    #print(len(example_full_list)) # 201   
    return example_full_list


# Messages...           
def fail_to_import_modules():
    return """    
    Detected that PySide6 modules are not installed.
    
    To install PySide6 in a virtual environment on a Linux system:

    :~$ python3 -m venv venv-pyside6   
    :~$ source venv-pyside6/bin/activate
    (venv-pyside6) :~$ cd venv-pyside6/  
    (venv-pyside6) :~/venv-pyside6$ python -m pip install -U pip setuptools wheel 
    (venv-pyside6) :~/venv-pyside6$ pip install PySide6 

    
    # For a list of modules that are installed:
    (venv-pyside6) :~/venv-pyside6$ ls -1 ./lib/python3.10/site-packages/PySide6/include/

    # Run program:
    (venv-pyside6) :~/pyside6$ python pyside6-help.py
    
    """

def module_message():
    return """\n
PySide6 References: 
https://wiki.qt.io/Qt_for_Python   
https://pypi.org/project/PySide6/ 

PySide6 utilities installed:
(venv-pyside6) :~$ pyside6-
pyside6-assistant         pyside6-lrelease          pyside6-qmllint
pyside6-designer          pyside6-lupdate           pyside6-qmltyperegistrar
pyside6-genpyi            pyside6-metaobjectdump    pyside6-rcc
pyside6-linguist          pyside6-project           pyside6-uic


To Launch Qt Designer
(venv-pyside6) :~/pyside6$ pyside6-designer
(venv-pyside6) :~/pyside6$ ~/venv-pyside6/lib/python3.10/site-packages/PySide6/designer 
Refer:
https://www.badprog.com/python-3-pyside2-setting-up-and-using-qt-designer 
 
  
The following Modules are installed as part of the $ pip install PySide6:

Qt3DAnimation - Classes that support animations in simulations
Qt3DCore - The core classes to support near-realtime simulation systems
Qt3DExtras - Pre-built elements for use with Qt3D
Qt3DInput - Classes to handle user input when using Qt3D
Qt3DLogic - Classes that enable frame synchronization
Qt3DRender - Classes that enable 2D and 3D rendering
QtBluetooth - Classes to support connectivity between Bluetooth enabled devices
QtCharts - Classes to support the creation of 2D charts
QtConcurrent - 
QtCore - The core Qt classes
QtDataVisualization - Classes to support the visualization of data in 3D
QtDBus - Classes to support IPC using the D-Bus protocol
QtDesigner - Classes to allow Qt Designer to be extended using Python
QtGui - The core classes common to widget and OpenGL GUIs
QtHelp - Classes for creating and viewing searchable documentation
QtMultimedia - Classes for multimedia content, cameras and radios
QtMultimediaWidgets - Provides additional multimedia related widgets and controls
QtNetwork - The core network classes
QtNetworkAuth - Classes for OAuth-based authorization to online services
QtNfc - Classes to support connectivity between NFC enabled devices
QtOpenGL - Classes for using OpenGL in PyQt user interfaces
QtOpenGLWidgets - Classes for rendering OpenGL in a widget
QtPositioning - Classes for obtaining positioning information from satellite, wifi etc.
QtPrintSupport - Classes to make printing easier and more portable
QtQml - Classes for integrating with the QML language
QtQuick - Classes for extending QML applications with Python code
QtQuick3D - Classes for rendering 3D Qt Quick content
QtQuickControls2 -
QtQuickWidgets - Classes for rendering a QML scene in traditional widgets
QtRemoteObjects - Classes for sharing the API of a QObject between processes or systems
QtScxml -
QtSensors - Classes for accessing a system's hardware sensors
QtSerialPort - Classes for accessing a system's serial ports
QtSql - Classes for integrating with SQL databases
QtStateMachine - 
QtSvg - Classes providing support for SVG
QtSvgWidgets - Classes for rendering SVG images in a widget
QtTest - Support for unit testing of GUI applications
QtUiTools - 
QtWebChannel - Classes for peer-to-peer communication between Python and HTML/JavaScript
QtWebEngineCore - The core Web Engine classes
QtWebEngineQuick - Classes for integrating QML Web Engine objects with Python
QtWebEngineWidgets - A Chromium based web browser
QtWebSockets - Classes that implement the WebSocket protocol
QtWidgets - Classes for creating classic desktop-style UIs
QtXml - Classes for supporting the DOM interface to XML

Note: Installed with PyQt6...
lupdate - Functions for handling translation files used by Qt Linguist
sip - Utilities for bindings developers and users
uic - Functions for handling the files created by Qt Designer    
QScintilla - $ pip install PySide6-QScintilla ???
    QScintilla - A source code editing software module - https://qscintilla.com/
"""


def icon_message():
    return """Qt includes Icons in that may be made use of. They are acquired from QtWidgets.QStyle.StandardPixmap. Their names all start with the letters "SP_". For example, to add the "Qt" icon so that it shows in the System Tray:
    pixmapi = getattr(QtWidgets.QStyle.StandardPixmap, "SP_TitleBarMenuButton")
    icon = self.style().standardIcon(pixmapi)
    self.setWindowIcon(icon)
    
The following are the icons available...
"""

                                     
if __name__=="__main__":

    # Qt Modules failed to load, so stop with a message.
    if error_stop:
        sys.exit(fail_to_import_modules()) 

    # get the full path to the PySide6 examples.
    example_path = get_full_path()
    print("example_path:", example_path)
    # example_path: /home/ian/venv-pyside6/lib/python3.10/site-packages/PySide6/examples/

    # Check if example_path exists???
    examples_exist = is_examples_exist(example_path)
    print("examples_exist:", examples_exist)    
    if not examples_exist:
        print("The Python/PySide6 example programs do not appear to be installed.")
        sys.exit("Terminating.")

    code_dict = get_code_dict_using_path(example_path)
    
    print("len(code_dict):", len(code_dict))  # 284

    # Create the examples list from the code_dict key
    example_list = []
    for key in code_dict.keys():
        example_list.append(key)   
        #print(key)        
    # Call routine to detect main.py in examples folders and remove other files.
    example_list = modify_example_list(example_list)


    # convert examples python files in code_dict to html files.
    convert_example_files_to_html(code_dict)

    # Building the qt6 help dictionary...
    module_list = dir()

    qt6_dict = build_dictionary(module_list)
    #print(len(qt6_dict)) # 46

    qt6_dict = remove_classes_double_underscore(qt6_dict)    
    
    qt6_dict = remove_methods_double_underscore(qt6_dict)
    
    qt6_dict = remove_methods_single_underscore(qt6_dict)

    qt6_dict = remove_no_type(qt6_dict)
    
    # For search facility.
    qt6_list = convert_dict_to_list(qt6_dict)
    #print(qt6_list)
    #print(len(qt6_list)) # 127811
    #print(qt6_dict)

    # Globally readable messages...    
    MESSAGE_1 = analyse_dictionary(qt6_dict)
    #print(MESSAGE_1) # Modules:46 Classes:1296 Methods:127811
    
    MESSAGE_2 = module_message()

    ICON_MESSAGE = icon_message()
    
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow(qt6_dict, qt6_list, code_dict, example_list, example_path)
    window.show()
    app.exec()
    
    
'''
https://zetcode.com/pyqt/qwebengineview/
https://pygments.org/docs/formatters/

https://stackoverflow.com/questions/7987881/ # How to zoom in and out

PySide...
https://www.pythonguis.com/faq/qwebengineview-open-links-new-window/

>>> import sys
>>> sys.executable
'/home/ian/venv-pyside6/bin/python'

https://stackoverflow.com/questions/984941/python-subprocess-popen-from-a-thread

import threading
#import subprocess

class MyClass(threading.Thread):
    def __init__(self):
        self.stdout = None
        self.stderr = None
        threading.Thread.__init__(self)

    def run(self):
        p = subprocess.Popen('rsync -av /etc/passwd /tmp'.split(),
                             shell=False,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)

        self.stdout, self.stderr = p.communicate()

myclass = MyClass()
myclass.start()
myclass.join()
print myclass.stdout 

styles...

default
emacs
friendly
friendly_grayscale
colorful
autumn
murphy
manni
material
monokai
perldoc
pastie
borland
trac
native
fruity
bw
vim
vs
tango
rrt
xcode
igor
paraiso-light
paraiso-dark
lovelace
algol
algol_nu
arduino
rainbow_dash
abap
solarized-dark
solarized-light
sas
staroffice
stata
stata-light
stata-dark
inkpot
zenburn
gruvbox-dark
gruvbox-light
dracula
one-dark
lilypond
nord
nord-darker
github-dark


[xcb] Extra reply data still left in queue
[xcb] This is most likely caused by a broken X extension library
[xcb] Aborting, sorry about that.
python: ../../src/xcb_io.c:673: _XReply: Assertion `!xcb_xlib_extra_reply_data_left' failed.
Aborted (core dumped)


xcb/jammy 2.4-8 amd64
  Manipulate X server cut and paste buffers/selections

(venv-pyside6) ian@hp:~/pyside6$ !xcb/jammy 2.4-8 amd64
  Manipulate X server cut and paste buffers/selections
bash: !xcb/jammy: event not found
Manipulate: command not found
(venv-pyside6) ian@hp:~/pyside6$ 
(venv-pyside6) ian@hp:~/pyside6$ sudo apt install xcb
[sudo] password for ian: 
Reading package lists... Done
Building dependency tree... Done
Reading state information... Done
The following NEW packages will be installed
  xcb
0 to upgrade, 1 to newly install, 0 to remove and 3 not to upgrade.
Need to get 22.3 kB of archives.
After this operation, 66.6 kB of additional disk space will be used.
Get:1 http://nz.archive.ubuntu.com/ubuntu jammy/universe amd64 xcb amd64 2.4-8 [22.3 kB]
Fetched 22.3 kB in 1s (35.9 kB/s)
Selecting previously unselected package xcb.
(Reading database ... 343469 files and directories currently installed.)
Preparing to unpack .../archives/xcb_2.4-8_amd64.deb ...
Unpacking xcb (2.4-8) ...
Setting up xcb (2.4-8) ...
Processing triggers for man-db (2.10.2-1) ...
(venv-pyside6) ian@hp:~/pyside6$ 

Problem still seems to happen.

https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=856469

> If I'm forcing the GDK_BACKEND to x11 it's working
>
> There are two solutions here I guess, either fix the code to not call
> X11 related functions when using wayland or to force the application to
> use X11 as a backend.
>
> The later and probably a workaround can be achieve with:
>
> gdk_set_allowed_backends ("x11");

(venv-pyside6) ian@dell:~/pyside6$ pip install matplotlib opencv-python numpy PyOpenGL pandas scipy
Collecting matplotlib
  Using cached matplotlib-3.6.1-cp310-cp310-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (11.8 MB)
Collecting opencv-python
  Downloading opencv_python-4.6.0.66-cp36-abi3-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (60.9 MB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 60.9/60.9 MB 3.0 MB/s eta 0:00:00
Collecting numpy
  Downloading numpy-1.23.3-cp310-cp310-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (17.1 MB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 17.1/17.1 MB 2.8 MB/s eta 0:00:00
Collecting PyOpenGL
  Downloading PyOpenGL-3.1.6-py3-none-any.whl (2.4 MB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 2.4/2.4 MB 4.1 MB/s eta 0:00:00
Collecting pandas
  Downloading pandas-1.5.0-cp310-cp310-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (12.1 MB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 12.1/12.1 MB 3.4 MB/s eta 0:00:00
Collecting scipy
  Downloading scipy-1.9.2-cp310-cp310-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (33.7 MB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 33.7/33.7 MB 867.5 kB/s eta 0:00:00
Collecting contourpy>=1.0.1
  Downloading contourpy-1.0.5-cp310-cp310-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (295 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 295.9/295.9 kB 2.9 MB/s eta 0:00:00
Collecting packaging>=20.0
  Downloading packaging-21.3-py3-none-any.whl (40 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 40.8/40.8 kB 1.3 MB/s eta 0:00:00
Collecting pillow>=6.2.0
  Downloading Pillow-9.2.0-cp310-cp310-manylinux_2_28_x86_64.whl (3.2 MB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 3.2/3.2 MB 583.9 kB/s eta 0:00:00
Collecting kiwisolver>=1.0.1
  Downloading kiwisolver-1.4.4-cp310-cp310-manylinux_2_12_x86_64.manylinux2010_x86_64.whl (1.6 MB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.6/1.6 MB 516.0 kB/s eta 0:00:00
Collecting cycler>=0.10
  Downloading cycler-0.11.0-py3-none-any.whl (6.4 kB)
Collecting python-dateutil>=2.7
  Downloading python_dateutil-2.8.2-py2.py3-none-any.whl (247 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 247.7/247.7 kB 3.0 MB/s eta 0:00:00
Collecting pyparsing>=2.2.1
  Downloading pyparsing-3.0.9-py3-none-any.whl (98 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 98.3/98.3 kB 3.0 MB/s eta 0:00:00
Collecting fonttools>=4.22.0
  Downloading fonttools-4.37.4-py3-none-any.whl (960 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 960.8/960.8 kB 1.7 MB/s eta 0:00:00
Collecting pytz>=2020.1
  Downloading pytz-2022.4-py2.py3-none-any.whl (500 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 500.8/500.8 kB 239.2 kB/s eta 0:00:00
Collecting six>=1.5
  Downloading six-1.16.0-py2.py3-none-any.whl (11 kB)
Installing collected packages: pytz, PyOpenGL, six, pyparsing, pillow, numpy, kiwisolver, fonttools, cycler, scipy, python-dateutil, packaging, opencv-python, contourpy, pandas, matplotlib
Successfully installed PyOpenGL-3.1.6 contourpy-1.0.5 cycler-0.11.0 fonttools-4.37.4 kiwisolver-1.4.4 matplotlib-3.6.1 numpy-1.23.3 opencv-python-4.6.0.66 packaging-21.3 pandas-1.5.0 pillow-9.2.0 pyparsing-3.0.9 python-dateutil-2.8.2 pytz-2022.4 scipy-1.9.2 six-1.16.0
(venv-pyside6) ian@dell:~/pyside6$ 
'''    
