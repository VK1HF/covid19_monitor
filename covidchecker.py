#!/usr/bin/python
# Author - Ian Gilchrist - VK1HF - ian@gilian.net
# Version 1.0
# My Python Version : 2.7.16

import urllib2
import os
import re
import time
import clicksend_client
import datetime


month_day = datetime.datetime.now()
base_url = "https://covidlive.com.au/report/daily-cases/"
state = "nsw"
url =  base_url + state
filename = "covidcases." + state
actual_time = int(time.time())
case_count_difference = 0
hysteresis = 60 # number of seconds to delay noticing any changes

os.system('clear')
month_day = datetime.datetime.now()
print (str(month_day.strftime("\nBEGIN >> @ %a %d-%b-%y %H:%M:%S\n")))

#Load data file - if doesn't exist set value to 0,0 - load dat (Unix Time) of last load and number of last update.

try:
    data_file = open(filename, "r")
    lines = data_file.readlines()
    last_lines = str(lines[-1:])
    data_file.close()
    file_data = re.search('(\d+),\w{2,3},(\d{1,9999})', last_lines, re.IGNORECASE)
    load_date = int(file_data.group(1))
    load_cases = int(file_data.group(2))
except:
    print("\n** file load failed - must not exist, all good\n")
    load_date = (0)
    load_cases = (0)

print "Last file save(secs).....: ",load_date
print "Last Cases count.........: ",load_cases
print "Current Time(secs).......: ",actual_time

if int(actual_time) > (int(load_date) + hysteresis):
    send_notifications = 1
    print "\n..Greater than " + str(hysteresis / 60) + " minutes diff between data change?  : Yes"
else:
    send_notifications = 0
    print "\n..Greater than " + str(hysteresis / 60 ) + " minutes diff between data change?  : No"
    month_day = datetime.datetime.now()
    print("...exiting...")
    print (str(month_day.strftime("\nEND << @ %a %d-%b-%y %H:%M:%S\n")))
    exit()


# Get Web data from covidlive.com.au

try:
  response = urllib2.urlopen(url)
  webpage_raw = response.read()
  extract_i_want = re.search('DAILY-CASES.+\n.+\n.+DATE\">(.{6}).*NEW\".+</td><td class=\"COL3 CASES\">.+</td><td class=\"COL4 VAR\"><span class=\".+\">&nbsp;</span></td><td class=\"COL5 NET\"><span class=\".+\">(.{1,5})</span></td></tr>', webpage_raw, re.IGNORECASE)
  #print(webpage_raw)

except:
  print("something went wrong with the Web call")
  exit()

if extract_i_want:
    print "\n..Matching extract found.. standby for extracted data"
    extract_date = extract_i_want.group(1)
    extract_new_cases = extract_i_want.group(2).replace(",","")
    print "    Date.......:",extract_date,"\n    State......:",state.upper(),"\n    New Cases..:",extract_new_cases
    new_cases = int(extract_new_cases)
    if new_cases != load_cases:
        case_count_difference = 1
        file_data = str(actual_time) + "," + state + "," + extract_new_cases + "\n"
        text_file = open(filename, "a")
        print ("\n..Writing File...\n")
        text_file.write(file_data)
        text_file.close()

        #Prune the file to stay at 100 lines long max 
        command = "cat covidcases." + state + " | tail -100 > covidcases." + state + ".new ; mv -f covidcases." + state + ".new covidcases." + state
        os.system(command)
else:
    print "\n..No Valid Web data (or not a number) so will now exit\n"
    exit()


if (send_notifications == 1 and case_count_difference == 1):
    print("\n..Sending notifications..\n ")

    #The Variables that matter are below..;
    #extract_date = "02 Sep"
    #extract_new_cases = "12"
    #state = "nsw"             # (lower cases - use 'state.upper()' for upper case.
    message_body = "COVID19 Update..:\nState : " + state.upper() + "\nNew Cases today : " + extract_new_cases + "\nDate Published : " + extract_date
    #print "+++\n" + message_body + "+++\n"
    import httplib, urllib
    conn = httplib.HTTPSConnection("api.pushover.net:443")
    conn.request("POST", "/1/messages.json",
      urllib.urlencode({
        "token": "REPLACE_ME",
        "user": "REPLACE_ME",
        "message": message_body,
      }), { "Content-type": "application/x-www-form-urlencoded" })
    conn.getresponse()

else:
    print("\n..not sending any nofications..\n")
        # Send SMS messages here.? why not. After data file update and prune. 


month_day = datetime.datetime.now()
print (str(month_day.strftime("\nEND << @ %a %d-%b-%y %H:%M:%S\n")))

