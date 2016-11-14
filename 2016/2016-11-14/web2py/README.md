web2py + meetup.com
===================

* `meetup.py` uses the meetup.com API to retrieve the next upcoming meeting.

  * General API: http://www.meetup.com/meetup_api/
  * Events API: http://www.meetup.com/meetup_api/docs/:urlname/events/#list

* In the `default` controller in a web2py instance (eg, hosted on pythonanywhere.com)
  the default *flash* can be replaced with API calls outlined in the above script,
  displaying data retrieved from the API.

  ```python
  def next_meetup():
      """
      Retrieves the next meeting from meetup.com.
      """
      url = "https://api.meetup.com/nzpug-hamilton/events?&sign=true&photo-host=public&page=1"
      r = requests.get(url, data={})
      j = r.json()
      timestr = str(datetime.fromtimestamp((j[0]["time"] + j[0]["utc_offset"]) / 1000))
      return timestr

  def index():
      """
      example action using the internationalization operator T and flash
      rendered by views/default/index.html or views/generic.html
      if you need a simple wiki simply replace the two lines below with:
      return auth.wiki()
      """
      # replace the default "flash" with info about the next meeting
      #response.flash = T("Next HamPUG meeting - Monday 14 November 2016 at 7pm")
      response.flash = next_meetup()
      return dict(message=T('Welcome to the Hamilton Python User Group'))

  ```
