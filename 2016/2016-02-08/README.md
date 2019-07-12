#### M#22

### IPython

Lawrence D'Oliveiro delivered a presentation on IPython. Lawrence provided two ipynb files, 
*Exponential Series.ipynb* and *Solid Angle Of A Circle.ipynb*.

The file *Exponential Series.ipynb* may be launched using the binder Jupyter kernel by 
clicking on the following icon...

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/HamPUG/meetings/master?filepath=2016%2F2016-02-08%2FExponential%20Series.ipynb)

The file *Exponential Series v4.ipynb* may be launched using the binder Jupyter kernel by 
clicking on the following icon...

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/HamPUG/meetings/master?filepath=2016%2F2016-02-08%2FExponential%20Series%20v4.ipynb)

The file *Solid Angle Of A Circle.ipynb* may be launched using the binder Jupyter kernel 
by clicking on the following icon...

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/HamPUG/meetings/master?filepath=2016%2F2016-02-08%2FSolid%20Angle%20Of%20A%20Circle.ipynb)

### Presentation Notes

IPython is an interactive shell, originally for Python. Though it is now being generalized, via the Jupyter project, to handle other languages on an equal basis.

IPython interfaces to the language implementation via its own “kernel” process. Separate from the kernel is the front end, of which there are three: one based on a character terminal, one built with the Qt GUI toolkit, and the web-based notebook interface. Of the three, the notebook interface is the most powerful, it’s the only one I have much experience with, and it is the one I will talk about here. If you’ve used Mathematica, the notebook concept will be very familiar.

The kernel process maintains a context for script programs that is preserved for as long as the kernel remains running. Thus, you can feed a command to define a variable or open a file, and then later send another command to access that variable or do something with that file. When the kernel is terminated, all such context is lost.

The notebook server is a custom web server, so the user interface can be provided via any modern web browser. A notebook file (extension “.ipynb”) is actually a text file in JSON format. Its content is a sequence of cells. Each cell can contain program-language text (in Python, in this case) to be executed by the kernel, or text that is only to be read by the user of the notebook, which can be nicely formatted using Markdown markup. The latter text can also include mathematical formulas in the appropriate subset of LATEX markup, implemented by the MathJax library, which is written in JavaScript and does all its actual rendering in the web browser.

Program cells can generate text or graphical output, which is displayed immediately following the cell when it is executed. They can also generate Markdown or mathematical markup by using the appropriate API calls, allowing the convenient display of dynamically-generated formatted text or mathematical formulas as well as more general graphics.

Not only that, but program code can also define simple interactive “widgets” (e.g. sliders, text-input fields) to create a very basic custom GUI that allows the user to interact with the cell output.

The notebook file saves the original cell content, along with the formatted representation of non-program cells. Remember that the in-memory program context (variables, open files etc) lives only in the kernel process, not the notebook front-end.

There is no command that simply saves the current notebook under its current name. There is a “Save and Checkpoint” command, which saves the notebook and also makes a time-stamped “checkpoint” copy in the “.ipynb_checkpoints” subdirectory. Also the notebooks is periodically autosaved, at an interval that defaults to 2 minutes. Alternatively, you can simply close the notebook window/tab; if there are unsaved changes, you get prompted whether you really want to leave the page. Regardless of what you select here, the notebook will be saved.

What about security? First of all, a notebook can execute arbitrary code. The notebook server, and the kernel, make no attempt to constrain the kinds of programs that can be executed. The assumption is that these are running on machines under the user’s control, executing code specified by the user. Therefore it is not their job to limit what the user can do.

There is another issue, that of receiving a notebook from another (possibly untrusted) source and executing arbitrary code from that. IPython doesn’t prevent you from doing this. But it will not automatically execute JavaScript from cached cell output, unless the notebook signature is verified against a key known to the user <https://ipython.org/ipython-doc/3/notebook/security.html>. Normally each user generates their own key, but it is possible to share keys with trusted colleagues.

IPython lets you set up multiple profiles, and easily switch between them. These let you create different sets of custom default settings for different usages. Profiles can also be used to isolate trust between different groups that you work with.
