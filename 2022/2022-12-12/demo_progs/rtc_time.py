# rtc_time.py
# Real Time Clock. 
# On Pico power-up it seems to automatically set time from host system via USB bus.
#
# print(rtc.datetime())
# RTC returns date/time as:
# (2022, 12, 4, 6,             10, 33, 15, 0)
# (YYYY, MM, D, Day-of-Week,   HH, MM, SS, ??)
# ?? In normal Python this is the day-of-the-year
#
# print(utime.localtime()) return date/time as:
# (2022, 12, 13, 12, 24, 9, 1,            347)
#  YYYY  MM  DD  HH  MM  SS  Day-of-week  Day-of-year

from machine import RTC

import utime
print("dir(utime):\n", dir(utime))
print()
print("utime.localtime():", utime.localtime())
print("utime.gmtime():", utime.gmtime())
print("utime.time():", utime.time()) #1670710288
print("utime.time_ns():", utime.time_ns())
print()

rtc = RTC()
print("rtc.datetime():", rtc.datetime())
# (2022, 12, 10, 5, 21, 43, 12, 0)

#print(dir(rtc)) # ['__class__', 'datetime']
#print(dir(rtc.datetime())) # ['__class__', 'count', 'index']

# Code to make time human readable...

(year, month, day, weekday, hour, minute, second, dunno) = rtc.datetime()
# dunno is day-of-year, but is given as 0.

days= {0:"Monday", 1:"Tuesday", 2:"Wednesday", 3:"Thursday",
       4:"Friday", 5:"Saturday", 6:"Sunday"}
       
months = {1:"January", 2:"February", 3:"March", 4:"April", 5:"May", 
          6:"June", 7:"July", 8:"August", 9:"September", 10:"October", 
          11:"November", 12:"December"}

print("{}, {} {} {}. {}:{:0>2}:{:0>2}".format(
        days[weekday], day, months[month], year,
        hour, minute, second))

#print("Today is {}".format(days[weekday]))
#print("The month is {}".format(months[month]))

"""
print(utime.time()) #1670710288
1670710288 #<-- Seconds since Linux Epoch 0 = Thu 01 Jan 1970 12:00:00 NZST

ian@dell:~$ date --date='@1670710288'
Sun 11 Dec 2022 11:11:28 NZDT # Was actually Sat 10 Dec 2022 22:11:28 NZST
"""

"""
print(utime.time()) #1670710288
1670710288 #<-- Seconds since Linux Epoch 0 = Thu 01 Jan 1970 12:00:00 NZST

ian@dell:~$ date --date='@1670710288'
Sun 11 Dec 2022 11:11:28 NZDT # Was actually Sat 10 Dec 2022 22:11:28 NZST
"""

