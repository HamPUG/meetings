import urllib2
import re
import glob

def geturl(url,agent=None):
    headers = { 'User-Agent': agent }
    req = urllib2.Request(url,None,headers)
    html = urllib2.urlopen(req).read()
    return html

def getbetween(body, start, end):
    strs = re.findall( re.escape(start) + "(.*?)" + re.escape(end), body, re.DOTALL)
    return strs


prefix = "http://www.lyricsfreak.com/m/metallica"
page = geturl("http://www.lyricsfreak.com/m/metallica/")
links = getbetween(page, '<td class="colfirst"><a href="', '"')
new_links = []
for link in links:
    if prefix in link:
        new_links.append(link)

"""
for i,v in enumerate(new_links):
    page = geturl(v)
    f = open("saved/" + str(i) + ".html", "wb")
    f.write(page)
    f.flush()
    f.close()

    print v
"""

files = glob.glob("saved/*.html")
for filename in files:
    body = open(filename).read()
    lyrics = getbetween(body, "<div id='content_h' class='dn'>", "</div>")[0]
    lyrics = lyrics.replace("\r","").replace("<br>"," ")
    print lyrics
