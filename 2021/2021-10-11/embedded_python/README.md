# Python embedded in LibreOffice or OpenOffice files.

Ian Stewart provided this presentation. His slide show is available as an odp or pdf file:

* Python Embedded Presentation.odp
* Python Embedded Presentation.pdf

By default, LibreOffice and OpenOffice include the ability to have BASIC scripts embedded within a document. This presentation introduces embedding Python scripts into a document. This is made easier by using the LibreOffice/OpenOffice extension **Alternative Python 
Script Organizer**, *APSO*.

The following Writer documents are provided to compare embedded BASIC and embedded Python.

* writer_basic_example.odt
* writer_python_example.odt

Originally Python was implemented as a seperate program that used a TCPIP port to communicate with LibreOffice or OpenOffice. An example of this is provided as the file:

* draw_uno_plan.py

This draws a house plan using the Draw application in which the intended layout of the piles may be modelled.

The following two documents contain either BASIC or Python embedded scripting to also demo the creation of a house plan on a Draw document in which the piling may be modelled.

* draw_embedded_basic_plan.odg
* draw_embedded_python_plan.odg

As another example the following two Calc documents contain either BASIC or Python embedded scripting to demo a spreadsheet and its chart show the amortization of a loan.

* calc_embedded_basic_amortization.ods
* calc_embedded_python_amortization.ods

The APSO extension to LibreOffice/OpenOffice includes a utility that provide Python with the capability to generate a Message box that is similar to the built-in Msgbox function in BASIC. The following Writer document, with embedded Python, demonstrates this Message box.

* writer_python_msgbox

Additional information is avaiable at Ian Stewart's github account: https://github.com/irsbugs/LO-OO-Macro-Programming

