# covid19_monitor
A Simple script to advise of changes on the covidlive.com.au site for daily new cases being updated. 

just update the state vriable with the state in question and you're good to go. 

I also have a cron job which deletes the logs at 4am each day. 

I save a version of the file for each state and run from CRON.d - see below.
* * * * * ~/covidchecker/covidchecker.qld.py >>~/covidchecker/QLD.log
0 4 * * * rm -f ~/covidchecker/*.log >/dev/null 2>&1

it checks every minutes - I would like to make it check every 5 minutes outside of the 8am-12.30pn each day - when most updates happen. 

I'm usinging Pushover for notifications - it's far and away better and more suited to the task than TXT/SMS or email : https://pushover.net/


