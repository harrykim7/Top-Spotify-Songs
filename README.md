### Spotify top songs playlist generator
This simple script creates a spotify playlist populated with top 50 songs from your last 4 weeks, 6 months, all time.  

It's set up so that the first time you run it, it'll create the playlist, and then every time from then, it'll just update the playlist. Don't delete 
the txt file that is created. 

First time you run it, it'll redirect you to spotify page for authorization.  

For Mac users - 
You can set the script as a cronjob so that it runs everyday or everyweek so that the playlist keeps updating automatically. 

Quick tutorial (Mac)
- if running on native Python3, replace first line (shebang) of script from #!/Users/harrykim/opt/anaconda3/bin/python to #!/usr/bin/env python3
or wherever the python is located. 
- Create a cronjob. Lot's of [tutorials online](https://towardsdatascience.com/how-to-schedule-python-scripts-with-cron-the-only-guide-youll-ever-need-deea2df63b4e)
- Note you don't need to specify the python path first since we are using the shebang. Mine looks like this
>> \* */5 * * * /folder-path-here/make_top_playlist.py 
- Another note that you probably need to [give cron Full Disk Access](https://apple.stackexchange.com/questions/378553/crontab-operation-not-permitted) in most cases (depending on where you stored the script). 

For Windows - 
There is the Windows Task Scheduler. Pretty sure it's easier but never used it. Hope it works. 
