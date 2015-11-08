import urllib2
import re
import glob
import time
import os

def geturl(url,agent=None):
    headers = { 'User-Agent': agent }
    req = urllib2.Request(url,None,headers)
    html = urllib2.urlopen(req).read()
    return html

def getbetween(body, start, end):
    strs = re.findall( re.escape(start) + "(.*?)" + re.escape(end), body, re.DOTALL)
    return strs

ONLINE = True
OUTPUT_DIR = "saved"
SLEEP_TIME = 0.5 # in seconds

prefix = "http://www.lyricsfreak.com/m/metallica"
page = geturl("http://www.lyricsfreak.com/m/metallica/")
links = getbetween(page, '<td class="colfirst"><a href="', '"')
new_links = []
for link in links:
    if prefix in link:
        new_links.append(link)

if ONLINE:
	for i,v in enumerate(new_links):
		page = geturl(v)
		# see if the "saved" folder exists first
		if not os.path.exists(OUTPUT_DIR):
			os.makedirs(OUTPUT_DIR)
		f = open(OUTPUT_DIR + os.sep + str(i) + ".html", "wb")
		f.write(page)
		f.flush()
		f.close()
		time.sleep(SLEEP_TIME)

files = glob.glob(OUTPUT_DIR + os.sep + "*.html")
for filename in files:
    body = open(filename).read()
    lyrics = getbetween(body, "<div id='content_h' class='dn'>", "</div>")[0]
    lyrics = lyrics.replace("\r","").replace("<br>"," ")
    print lyrics
