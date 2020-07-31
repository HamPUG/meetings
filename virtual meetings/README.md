# Virtual Meetings - Hamilton User Groups experiences

Draft document by Ian Stewart. Please email Ian if you have anything you wish to add or correct, etc. 


## Introduction

During the Covid pandemic level 2 to 4 periods in 2020, IT User Groups in New Zealand were unable to continue having their regular meetings. In Hamilton, this impacted for three months at least the following IT groups:

* Hamilton Python User Group ~ [HamPUG](https://github.com/HamPUG/) 
* Waikato Linux Users Group ~ [WLUG](http://www.wlug.org.nz/)
* Hamilton Computer Club ~ [HCC](http://hamiltoncomputerclub.org.nz/)

As a work-around *HamPUG* and *WLUG* held virtual monthly meetings. One meeting used [Google Hangouts](https://hangouts.google.com/), the other five used the [BigBlueButton](https://bigbluebutton.org/) instance, kindly made available by the NZ Open-Source Society ~ [NZOSS](https://bbb.nzoss.nz/b). Most presentations were performed by presenters in Hamilton, with two exceptions of presenters delivering from Kerikeri and Arapuni.

During this lockdown period some experimenting was performed to see if a server located in Hamilton could be easily setup to provide open-source web conferencing. One attempt was with [Jitsi](https://jitsi.org/) another with [BBB](https://bigbluebutton.org/)


This document includes: 

* Highlighting experiences and providing recommendations in using web conferencing for virtual meetings using the BBB server.
* Consideration of future regular meetings to also include being online as a virtual meeting.
* Consideration of approaching a Community Centre in Hamilton with regard to providing an open-source web conference server.


## BBB Virtual Meeting Guidelines

A BBB Virtual Meeting involves people in three different roles:

* Attendees
* Moderator
* Presenter

Also to be considered are general guidelines for your computer, web-camera, microphone, etc. 

The following are guidelines for each of the above.

### General Guidelines:

#### Hardware and Setup

* Computer. A 3GHz, Quad Core, CPU with 8GB RAM.
* Internet connection. Normally able to receive data at 1MB/s.
* A quiet room. No sound from a TV in the background.
* Web-cam is positioned so when you look at your screen you are looking at the camera.
* No lighting behind you is in camera view. i.e. Webcam is not pointing at a light bulb just above your head.
* Microphone position not more than 1 meter from your mouth. Avoid *off-mic* effect.
* Microphone not too close to mouth to avoid *popping* effect.
* Know how to adjust the volume of your microphone.
* Headphone or a single earphone rather than using your speakers. Avoid feedback when you talk in a BBB session.

#### BBB Usage

Familiarise yourself in BBB with:

* Log in 15 minutes before the meeting starts.
* Log in with your microphone and camera enabled.
* You may need to wait 30+ seconds before you can perform the BBB microphone test.
* On completing the microphone test and connection into the classroom identify yourself to the moderator.
* Perform a microphone sound level check with the moderator.
* Adjust your microphone level via your computers operating system audio utility.
* Use BBB to mute your microphone. Be familiar with BBB muting and un-muting facility. 
* Use BBB to turn off your camera, unless you are a presenter.
* Be familiar with BBB turning on and off your Webcam.
* Open the chat panel and perform a test chat with the moderator.
* Open a new page on a text editor on your computer. 
* Test copying from the chat panel to your text page. Note that any information in the chat panel is lost when the BBB session is over.

#### Notes on BBB Slide shows

The BBB server accepts a slide show from a presenter to be uploaded and then the presenter controls the displaying of the slides. Notes:

* When the moderator hands control to you as the presenter, then upload your slide show.
* Your slide show should have a 4:3 aspect ratio. If you created, say, a 16:9 aspect ratio slide show, then the right hand-side of each slide is truncated.
* Your slide show may be uploaded as a .pdf file or a .odp file.
* If you upload a .odp file then it gets converted to .pdf by the BBB server.
* Fancy slide transitioning features will be lost.
* When delivering your slide show, then your mouse appears like a laser pointer light beam on the slide.
* If you do not expand to your view of the slide show to full screen, then you can also look at any comments that get added into the chat panel while performing the slide show.
* The presenter does not get a *next slide preview*.
* It is possible, but not recommended, to run a slide show from your computer and share your computers desktop so others can see the slides. Unfortunately your mouse pointer is not displayed to the attendees. Also you can not monitor any comments attendees may make.



### Attendees

* Default to leaving your microphone and camera off.
* Turn on mic when you intend to ask a question. Moderator can see your mic has been turned on, and interrupt the presenter to allow you to ask a question, etc
* Watch your mouse. When the presenter is using the BBB slide show feature, then your mouse, if moved across the presentation, will show on the slide show. 
* If applicable use your mouse when asking a question about a BBB slide show.
* Enter questions or feedback into the chat panel. The moderator will be monitoring.

### Moderator

#### Practice Session

* The day before the presentation request each presenter to join for a brief practice session.
* Do a test of all resources that each presenter will use. E.g. BBB slide show, console terminal session on their computer, editor on their computer to display code, and Web site links.
* Ensure text in all media is of a font size that is legible.
* Test upload of slide show is quick.
* Discuss with each presenter on the format for interruptions for questions to be asked. E.g. After every two slides.
* If this is the first time for a presenter on BBB then allow 30 minutes to an hour for their practice session.


#### Session

* Vet each attendee.
* Check each attendees microphone level.
* Advise each attendee to default to turning off their mic when the presentations start.
* Ensure presenters have all material available.
* Pass permission to whomever has the role of presenter.
* Monitor the chat panel and attendee microphones being turning on.
* Interrupt the presenter to takes questions or discuss points raised in the chat.
* Thank the presenter for their presentation.

### Presenter

#### Practice Session

Attend a practice session and ensure:
* Familiar with BBB screen and icons and switching between sharing different screen applications.
* Upload slide show
* Practice presenting.
* Check microphone and headphones are working OK.
* If this is the first time you are delivering a presentation on BBB then allow 30 minutes to an hour for this practice. 

#### Session

* Have a glass of water next to you in case you start coughing.
* Paste links to your presentation material of slides show and programs, etc. into the chat session.
* Upload slide show
* Pause after each slide to review what is in the chat panel, or take questions from attendees, or rapport with moderator. 
* Copy all the chat messages after the presentation.



## Experimenting with Open-Source Web Conferencing

Experimenting was performed on open-source web conferencing server software.

### Jitsi

This was found to be easy to install. However the server it was installed onto did not have a registered domain name or an SSL certificate which are mandatory for Jitsi. As a result it could not be tested.

* Jitsi [Download](https://jitsi.org/downloads/)
* Self Hosting Installation [Guide](https://jitsi.github.io/handbook/docs/devops-guide/devops-guide-start)

### BBB

The initial install took some fiddling before it was working OK. After adding the TLS there were problems.

* BigBlueButton [documentaton](https://docs.bigbluebutton.org/)
* BigBlueButton [install](https://docs.bigbluebutton.org/2.2/install.html)
* BigBlueButton [install-script](https://github.com/bigbluebutton/bbb-install)
 

## Future Meetings

HamPUG and WLUG are investigating the possibility that their future meetings that are currently publicly held in a classroom at Waikato University will also be presented simultaneously on a web conferencing server.

The benefits of this additional Virtual Meeting should be:

* More people may join the meetings. 
* Avoiding, for some, their long travel times to the Hamilton meetings.
* Provide for those unable to attend evening meetings due to lack of public transport. 
* Potential for a presenter to present remotely from their home.

When the Presenter is in the classroom it is envisaged that this would require:

* Continued ability to use NZOSS BBB server or a server provided by the Hamilton community.
* Presenter in the classroom logged into the BBB server running their slide show or demonstrating their code, etc.
* The presenters computer connected to the video projector in the classroom.
* The presenter wearing a radio-mic that is feed into the computer.
* An attendee performing the role of the *moderator* of the BBB session.
* The *moderator* monitoring the BBB session to relay questions from attendees, etc.
* A web camera in the classroom to display what gets written on the whiteboard. Web camera is connected by USB cable to presenters computer.

When the Presenter is at home delivering a BBB presentation it is envisaged that this would require in the classroom:

* The *moderators* computer is connected to the classrooms video projector and audio system.
* The radio-mic is connected to the moderators computer. 
* The radio-mic is passed around to anyone in the audience who wants to ask the presenter a question. Potential audio feedback problems will exist.
* Attendees in the classroom could use their mobile phone to connect to the BBB session and ask questions from their mobile phone. May help avoid the feedback issue.

## Hamilton Based Open-Source Web Conferencing Server.

Providing Web Conferencing may be considered as a service that should be provided to the community. Thus there may be a community centre in Hamilton with the IT infra-structure in place that would be prepared to host this service. 



 

End of document. All ideas, comments and enhancements welcome.
