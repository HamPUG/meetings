# 2019-05-13
#### 59

## Presentation on Creating a Website

#### A static web-site, hosted on PythonAnywhere, with web-pages created using reStructuredText and the website generated by the Nikola application.

Presenter: Ian Stewart

The presention at the meeting held on 13 May 2019 covered the following:
- Obtaining a reStructuredText (reST) editor.
- Using the editor to create reST web-pages.
- Creating a python virtual environment
- Installing Nikola static website generator application in the virtual environment.
- Using Nikola to convert the reST web-pages into html files and generate the website.
- Creating a free beginners account on PythonAnywhere
- Uploading the web-site to the PythonAnywhere account.


In a somewhat recursive scenario, the presentation that Ian delivered is captured  in a website that he created. Please review the website http://hampug1.pythonanywhere.com

As part of the presentation Ian performed many linux bash commands to create the basic template for the web-site he built. These commands are attached as the file *presentation_history*.  You can replace your *~/.bash_history* file with this *presentation_history* file. By recalling your bash history in sequence with the bash history commands, !1, !2, !3, etc., you may repeat the delivery in the presentation and create your own template web-site. You may then modify the template to build your own web-site. As part of the presentation a modified Nikola *conf.py* file is used called *conf_quiet.py*. Please find this file in this repository and place it in your home folder. The conf_quiet.py file is the conf.py file with edits in four places. Search with the string Edited by Ian to see what the editing involved.

Attached are the files:
- presentation_history
- conf_quiet.py

The *presentation_history* file is installed on your linux laptop computer as follows: 
- Place the *presentation_history* file into your home folder. I.e. Your ~/ folder. 
- Open one console terminal window on your laptop. 
- Check that you have *.bash_history* file. ` $ ls -l .bash_history`
- Make a backup: `$ cp .bash_history bash_history_backup_$(date '+%Y%m%d-%H%M%S')`
- Overwrite the bash_history: `$ cp presentation_history .bash_history`
- Clear history currently in memory:  `$ history -c`
- Close the console terminal window.

- Open a console terminal window.  The history for this terminal will now contain the bash commands to learn about Nikola and create a template web-site. Execute the commands sequencially using the history recall as follows: `$ !1 `then `$ !2`  then `$ !3` etc.
  
  








































