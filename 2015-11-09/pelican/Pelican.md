# Pelican

Pelican is a static site generator, written in Python.

Content is written in 

* reStructuredText
* Markdown
* AsciiDoc

And then compiled into HTML.

## Links

* Homepage http://blog.getpelican.com/
* Documentation http://docs.getpelican.com/en/
* Themes https://github.com/getpelican/pelican-themes/

## Installation

**NB:** Best to do this in a virtualenv!

* setup virtualenv

  ```
  mkdir pelican
  virtualenv --system-site-packages pelican
  cd pelican
  source bin/activate
  ```

* install via pip

  ```
  pip install pelican
  ```

* install Markdown support

  ```
  pip install Markdown
  ```

## First project

* Use the Pelican wizard
  
  ```
  pelican-quickstart
  ```

* The content of the website goes into `content` sub-directory

* *Pages* go into special sub-directory `content/pages`, get added to menu using their title.

* *Articles*, as in blog post, just get stored anywhere in `content`. *Category* of article is menu item.

* Create first article (`content/first.md`)

  ```
  Title: First post
  Date: 2015-11-09 10:20
  Category: Blog

  This is my first post
  ```

* Reference an image using the `{filename}` placeholder as reference for path

  ```
  ![alt text]({filename}/images/theimage.png)
  ```

* Generate HTML

  ```
  pelican content
  ```

* run webserver

  ```
  cd output
  python -m pelican.server
  ```

* open browser with http://localhost:8000/


## Install and use a theme

* clone the theme that you like

  ```
  git clone https://github.com/DandyDev/pelican-bootstrap3.git
  ```

* install the theme

  ```
  pelican-theme -i ~/some/where/pelican-bootstrap3
  ```

* use theme by setting the `THEME` property

  ```
  THEME = 'pelican-bootstrap3'
  ```
 
* re-generate the HTML

  ```
  pelican content
  ```

