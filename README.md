# course-scheduler
I'm pretty sure a few CS students at Stevens have tried something like this already, but I'm doing it anyway. This is a tool to take all the classes you need to take and look at the xml that the calendar runs off, then show you your possible schedules

##Background
So at Stevens the only way to reasonably figure out your schedule for future semesters is to use the course scheduler available [here](https://web.stevens.edu/scheduler/). You can search for classes and see different offerings, and work out a schedule that works.

Tha annoying part is when one class is offered at 4 different times, one is only offered at one time, 2 others ones have 2 sessions, and they all meet a few times a week at different times. Oh yeah and a few need recitations too. And on top of all that there's no way I want 8am classes.

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
