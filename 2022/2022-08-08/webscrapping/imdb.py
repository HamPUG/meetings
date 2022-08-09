import json
import requests
import sys
from bs4 import BeautifulSoup


# retrieve page
url = "https://www.imdb.com/title/tt0071853/"
r = requests.get(url)
if r.status_code != 200:
    print("Failed to retrieve page: %s" % url)
    sys.exit(1)

# parse page and retrieve information
soup = BeautifulSoup(r.content, "html.parser")
for script in soup.findAll("script", type="application/ld+json"):
    print(script)

    # parse json
    j = json.loads(script.text)

    # output information
    print("Title:", j["name"])
    print("Plot:", j["description"])
    if "genre" in j:
        print("Genre:", j["genre"])
    print("Published:", j["datePublished"])
    if "image" in j:
        print("Downloading image:", j["image"])
        r = requests.get(j["image"], stream=True)
        if r.status_code == 200:
            with open("./image.jpg", 'wb') as f:
                for chunk in r:
                    f.write(chunk)


