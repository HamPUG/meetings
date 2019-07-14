# 2019/07/08 - Jupyter kernels

* [xeus-cling](https://github.com/QuantStack/xeus-cling) - Jupyter kernel for C++
* Available through [Anaconda](https://www.anaconda.com/distribution/)
* [Installation](https://xeus-cling.readthedocs.io/en/latest/installation.html)


### Jupyter Notebook

Jupyter Notebook (formerly IPython Notebooks) is a web-based interactive computational environment for creating, executing, and visualizing Jupyter notebooks. By default Jupyter Notebook ships with the IPython kernel to provide execution of Python code.

Project Jupyter's name is a reference to the three core programming languages supported by Jupyter, which are Julia, Python and R, and also an homage to Galileo's notebooks recording the discovery of the moons of Jupiter.

Jupyter notebook is normally installed as a local application. For example:

sudo apt install python3-notebook jupyter jupyter-core python-ipykernel 

It is launched from a console command line with $ jupyter-notebook

The notebook files that are created have the extension .ipynb

### Binder

This is a web-site that provides an on-line Jupyter notebook executable environment. 

Your .ipynb files may be placed in a repository where you have an account, like: GitHub, Gist, GitLab.com, Git repository, Zenodo DOI.

By going to the Binder home directory, https://gke.mybinder.org/ you can build a URL that will launch and execute your ipynb file in your repository.

For example the URL field is: 

https://github.com/HamPUG/meetings/

and the Path to a notebook file (optional): 

2019/2019-07-08/jupyter_kernels/test.ipynb

Binder will produce a URL of:

https://mybinder.org/v2/gh/HamPUG/meetings/master?filepath=2019%2F2019-07-08%2Fjupyter_kernels%2Ftest.ipynb

On opening a browser tab with the above URL then binder will provide an executable session of the test.ipynb notebook.

Additionally the binder web-site provides markdown or restructured text code so that an icon may be embedded into the README to launch the executable session.

For example the markdown code to produce the launch binder icon is:

`[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/HamPUG/meetings/master?filepath=2019%2F2019-07-08%2Fjupyter_kernels%2Ftest.ipynb)`


### C++ and Binder

The language C++ normally requires its code to be compiled and then it can be executed.  

The project cling https://root.cern.ch/cling provides an interactive C++ interpreter.

The project xeus-cling is a Jupyter kernel for C++ based on the C++ interpreter cling and the native implementation of the Jupyter protocol xeus.

Xeus-cling is installed using the anaconda package manager.

https://xeus-cling.readthedocs.io/en/latest/installation.html


On scrolling down the README at the xeus-cling github site https://github.com/QuantStack/xeus-cling you will see that you can launch Binder. This will provide an run Jupyter C++ online.

