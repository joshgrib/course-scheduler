# course-scheduler
I'm pretty sure a few CS students at Stevens have tried something like this already, but I'm doing it anyway. This is a tool to take all the classes you need to take and look at the xml that the calendar runs off, then show you your possible schedules

##Background
So at Stevens the only way to reasonably figure out your schedule for future semesters is to use the course scheduler available [here](https://web.stevens.edu/scheduler/). You can search for classes and see different offerings, and work out a schedule that works.

Tha annoying part is when one class is offered at 4 different times, one is only offered at one time, 2 others ones have 2 sessions, and they all meet a few times a week at different times. Oh yeah and a few need recitations too. And on top of all that there's no way I want 8am classes.

##Approach
So using [the scheduler API](https://www.thegreatco.com/projects/scheduler-api/), which I'm surprised is documented as well as it is for anyone to use, you can request the xml for any semester. The problem is I know pretty much nothing about using xml, much less getting nested data from it and how to figure out all the schedules.

None-the-less I'm going to try it out. I just dumped the ~6000 lines of xml for fall 2015 into Sublime Text 2, then narrowed it down to the ~60 lines I need that have the all possible sessions for the classes I'm taking in the fall. Theres 23 course sections available to fill 6 classes. A few are only offered at one time, a few have recitations, and a few meet at different times on different days, so it's definitely quite a bit of a challenge. This is in my2015f.xml
