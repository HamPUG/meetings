import requests
from datetime import datetime

# documentation
# http://www.meetup.com/meetup_api/docs/:urlname/events/#list
# try it:
# https://secure.meetup.com/meetup_api/console/?path=/:urlname/events
print("requesting next meeting...")
url = "https://api.meetup.com/nzpug-hamilton/events?&sign=true&photo-host=public&page=1"
r = requests.get(url, data={})
print("\nresponse in json\n")
j = r.json()
print(j)
print("\nDescription of first event\n")
print(j[0]["description"])
print("\nLink\n")
print(j[0]["link"])
print("\nTime\n")
print(datetime.fromtimestamp(j[0]["time"] / 1000))
print("\nDuration\n")
print(str(j[0]["duration"] / 1000 / 3600) + " hours")

