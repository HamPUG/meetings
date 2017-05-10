## Google Text to Speech

This presentation provides an introduction to the Text to Speech facility that is available from Google.

The presentation is a LibreOffice Impress slide show.

The python3 program *google_talk_presenter.py* has been written to run this slide show. The program uses the uno module to communicate with Impress. This allows python to launch the slide show and change the slides, etc.

The program sends the text for each slide to Google's text to speech url. Google returns this as an mp3 audio stream of speech.

Additionally the program can access from local folders .wav or .mp3 files and play these local speech or music files.

In conjunction with the program and the slide show, there is a control file "google_talk_presentation.txt". This file contains the text to be converted to text and commands to be executed. Here is a snippet from this file...

```
[slide_show_file:google_talk_presentation.odp]  
     
[slide:1]

[music:entertainer.mp3]

[language:english]

Hello and welcome to this presentation on the text to speech facility
```

Commands are in brackets and comprise of a keyword and a value. For examples:
 
[language:english] sets the language for the following text to be in English.
The text that follows will be submitted to google and returned as English spoken text.

[slide:1]
This will cause the Impress slide show to display slide number 1.

[music:entertainer.mp3]
This will look in the current working directory for the file "entertainer.mp3". On retrieving this file the music will be played.

A line commencing with a # is a comment field.

For more information on how to use or write your own control file please read the commented section in the first 100 lines of the *google_talk_presentation.txt* file.


To install and run this presentation copy, create a sub-folder on your linux laptop with LibreOffice. Copy all these files to that folder. Ensure your laptop is on-line to the internet and you have a good quality / high-speed connection. Open a terminal window and set default to the sub-folder, then type:
```$ python3 google_talk_presenter.py```

It will launch the slide show. On launching it does an audio level check and prompts with:
```Audio level OK? [Yes]:```
Type "No" to perform the audio level check again.
Type "Yes" to start the slide show.
 

## Environment
This presentation was delived using this environment:
* Ubuntu Mate 16.04.2 64-bit / Mate 1.12.1
* LibreOffice Version: 5.1.6.2
* Python 3.5.2 (default, Nov 17 2016, 17:05:23) [GCC 5.4.0 20160609] on linux

## Installation
To install the python uno bridge to control the LibreOffice Impress slide show.

$ sudo apt-get install python3-uno

## Tar file distribution

The file *google_talk_presentation.tar.gz* on github contains the following files:
* entertainer.mp3
* espeak_1.wav
* espeak_2.wav
* google_talk_presentation.odp
* google_talk_presentation.txt
* google_talk_presenter.py
* pico_1.wav
* pico_2.wav
* README.md
* yakety_yak_solo.mp3

Download this file and unzip it.
