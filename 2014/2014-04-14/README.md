# 2014-04-14
#### 3

## Introduction

Yesterday I did a talk on using Python to scrape all the song lyrics from a particular artist (from lyricsfreak.com) and then create a word cloud from all those lyrics using either using [Wordle](http://www.wordle.net/) or using R's `wordcloud` package. The idea was to get a visual representation of the words that were said the most by a particular band or artist.

The two main methods for doing this were through `geturl()` and `getbetween()`. `geturl()` is self-explanatory, and `getbetween()` allows us to find all strings that are in between two strings, for a particular body of text. So we use this method to basically wrangle data out of the HTML. As I mentioned in the talk, this way of doing things is kind of crude - it's good for quick one-offs or if you don't care about anything apart from getting the data. But there are nicer ways of doing this, such as using [BeautifulSoup]('http://www.crummy.com/software/BeautifulSoup/') where you can navigate the DOM of the HTML. Hell, I should probably use that more often too!

As mentioned at the start, we used both Wordle and R to generate our wordclouds. Wordle makes nicer wordclouds but it may be less accessible from a programmatic standpoint. R makes reasonably good looking wordclouds but it involves a lot of fiddling with parameters!

Usage
---

```
python get.py > output/out.txt
```

Note that there is a boolean flag in the script called `ONLINE` - if it's set to true, then it will download the .html files (that correspond to lyrics from each song) and save them to a folder called `saved` in the same directory as the script. Otherwise if the boolean is set to false it will assume you already have the .html files in that folder and then do everything locally. I have also made other improvements to the script since the presentation, such as having the script create the output directory for you if it doesn't exist, etc.

Then you can copy and paste the contents of `out.txt` into Wordle or use the R script `create-cloud.R` (if you know R!).

Useful links
---

* [PDF printer for extracting Wordle clouds (Ubuntu)](http://ubuntuportal.com/2012/04/easy-way-to-create-pdf-printer-in-ubuntu-12-04.html)
* [BeautifulSoup](http://www.crummy.com/software/BeautifulSoup/)
    * `sudo pip install BeautifulSoup`
* [R wordcloud library](http://cran.r-project.org/web/packages/wordcloud/wordcloud.pdf)
