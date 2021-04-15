# Intro to GTK

Presented by: Ian Stewart.

GTK is one of the GUI tookits available for python. 
The presentation included 13 python programs in which the GUI is progressively developed.

This should be helpful to anyone developing a GTK program.

A summary of the progessions in each of the 13 programs is as follows:
```
1. Minimum window
2. Provide a title <-- Not recommended. Probably be deprecated.
   Set size request to make it bigger
   Use dir to get the Window (self) attributes.
3. Add the title field when instantiating the Window. <-- Recommended
4. Add a grid.
   Place a frame in the grid.
5. In the frame add another grid.
   Create a list of buttons and place them into the frames grid.
6. Add connect to each button to call routine.
   When buttons are clicked perform action to update label.
7. Add an identifier field to the buttons.
   On callback use identifier.
8. Add CSS function and call it on launching application.
   Set style context for label to use CSS. 
9. Add CSS for Frame and buttons.
10. Add CSS Colour to buttons and label.
11. Add Fav icon in the system tray. Not on the title bar with Ubuntu mate.
    Replacement Header Bar supporting sub-title.
12. Add a Message box and its response when button 0 is clicked.
13. Add an icon to the header bar.
```

A .odp file commences with two slides related to the GTK programs. This is also avaialble as a pdf file.

This presentation was delivered in conjunction with the 64-bit Alpha Instruction Set. 
A GUI program is being  developed in GTK to aid with building instructions.


