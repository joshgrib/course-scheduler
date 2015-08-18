# course-scheduler

[Website](joshgrib.pythonanywhere.com) - not 100% functional as of commit 75

I'm pretty sure a few CS students at Stevens have tried something like this already, but I'm doing it anyway. This is a tool to take all the classes you need to take and look at the xml that the calendar runs off, then show you your possible schedules

##Background
So at Stevens the only way to reasonably figure out your schedule for future semesters is to use the course scheduler available [here](https://web.stevens.edu/scheduler/). You can search for classes and see different offerings, and work out a schedule that works.

To figure out your scheduler you basically just need to do trial and error until you find one that works and you're relatively happy with. I want to make it so you enter the courses you need to take, and you can see all the schedules you could have.

##Approach
So using [the scheduler API](https://www.thegreatco.com/projects/scheduler-api/), which I'm surprised is documented as well as it is for anyone to use, you can request the xml for any semester. I take the xml and a list of courses and pull out the info I need, and turn it into a big nested dictionary. Then I go through all the courses and sections, find all possible combinations, and check for conflicts. Any schedules with no conflicts are put into a new dictionary, and sent through flask to make the HTML to display them for the user.

###Python libraries
####flask
The web app framework I'm using to make the program run online and keep everything organized. It was annoying to learn but it was worth refactoring everything. Its much easier when everything is working the way it's supposed to
####xml.etree.ElementTree
For XML parsing. This library turn XML data into nested dictionaries. Then I can go through, edit them, and pull out what I need
####re
Regex
####itertools
For finding all possible combinations, and for finding all possible comparisons to make within a combination
####urllib
Gets the XML data from the API using the url
####pickle
Read/write local files

###Future development ideas (also see issues)
Fix the app so it works
I should be able to do this if I:
* Convert from pickle to json
* Remove files when after they're used
