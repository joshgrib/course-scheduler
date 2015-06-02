import copy
'''
http://web.stevens.edu/scheduler/cor  2015F/sched_plus_crsemtg.txt
Got there by going back to the "core" part of the url then going to that text file (plus course meeting?)
'''

coursesNestedBetter = {\
    "BT  353":{\
        "A":[\
            ["M","1300","1350"],\
            ["W","1100","1240"]\
            ],\
        "B":[\
            ["M","1500","1640"],\
            ["W","0900","0950"]\
            ],\
        "C":[\
            ["T","1500","1640"],\
            ["R","1100","1150"]\
            ],\
        "D":[\
            ["T","1500","1640"],\
            ["R","1100","1150"]\
            ],\
        "E":[["M","1815","2045"]]\
        },\
    "CS  115":{\
        "A":[\
            ["M","1200","1250"],\
            ["W","1200","1250"],\
            ["F","1200","1250"]\
            ],\
        "B":[\
            ["M","1300","1350"],\
            ["R","1300","1350"],\
            ["F","1300","1350"]\
            ]\
        },\
    "CS  115L":{\
        "A":[["R","0900","1040"]],\
        "B":[["R","1100","1240"]],\
        "C":[["R","1500","1640"]],\
        "D":[["R","1500","1640"]],\
        "E":[["F","1000","1140"]],\
        "F":[["F","1600","1740"]]\
        },\
    "CS  135":{\
        "A":[\
            ["F","1000","1050"],\
            ["W","1000","1050"],\
            ["F","1000","1050"]\
            ]\
        },\
    "CS  135L":{\
        "A":[["F","1100","1240"]],\
        "B":[["F","1300","1440"]]\
        },\
    "CS  146":{\
        "A":[\
            ["T","0900","0950"],\
            ["W","0900","0950"],\
            ["F","0900","0950"]\
            ],\
        "B":[\
            ["M","1400","1450"],\
            ["T","1400","1450"],\
            ["R","1400","1450"]\
            ]\
        },\
    "D   110":{\
        "A":[["T","1700","1805"]]\
        #double brackets used to maintain consistent schema
        },\
    "HHS 468":{\
        "EV":[["M","1815","2045"]]\
        }\
    }

#possible schedule format
ex_schedules = {\
    "sched1":{\
        "M":["course1","course2","course3"],\
        "T":["course1","course2","course3"],\
        "W":["course1","course2","course3"],\
        "R":["course1","course2","course3"],\
        "F":["course1","course2","course3"]\
        },\
    "sched2":{\
        "M":["course1","course2","course3"],\
        "T":["course1","course2","course3"],\
        "W":["course1","course2","course3"],\
        "R":["course1","course2","course3"],\
        "F":["course1","course2","course3"]\
        }\
    }
schedules = {}
def scheduleMakerTesting():
    '''This is used to make a new "branch" of schedules. When theres a few possibilities, a new branch will be made for each one, then from there each addition will be checked with each branch.'''
    base_schedule = {"M":[],"T":[],"W":[],"R":[],"F":[]} #time to branch
    new_sched = {}#new empty dictionary

    print "base: " + str(base_schedule)
    print "new: " + str(new_sched)

    new_sched = copy.deepcopy(base_schedule)#fill the new one with a copy of the old one
    #this has to be used to make a new dictionary, otherwise they just point to the same obejct, deepcopy goes to nested dictionaries
    new_sched.update({"new":"true"})#add a new key-value to the new dictionary

    print "base: " + str(base_schedule)
    print "new: " + str(new_sched)

#comparison for two meeting times to check for conflicts
def isAllowed(classList1, classList2):
    '''
    isAllowed():
                    |----------------|                      interval 1
    |----------|                                            end2<start1         True - No conflict
                                            |-------|        end1<start2         True - No conflict
    |------------------|                                  end2 !< start1      False - Conflict
                                |---------------|          end1 !< start2      False - Conflict
                |-------------------------|             end2 !< start1      False - Conflict
                                                         &  end1 !< start2       False - Conflict
                        |--------|                          end2 !< start1
                                                         &  end1 !< start2       False - Conflict
    '''
    if (classList2[2] < classList1[1]) or (classList1[2] < classList2[1]):
        #print 'No conflict!'
        return True
    else:
        #print 'Conflict!'
        return False

def findAllConflicts():
    '''This will loop through each section and find all conflicts with all other sections. Basically a combination of the function to print all courses sections and meeting times, and the one to check for conflicts between 2 meeting times. This will have to check 1122 meeting times so seeing the speed will be interesting too.'''
    count = 0
    conflicts = 0
    for course1 in coursesNestedBetter:
        for section1 in coursesNestedBetter[course1]:
            for class_time1 in coursesNestedBetter[course1][section1]:#go through all meeting times in all sections in all courses
                for course2 in coursesNestedBetter:
                    if (course1 == course2):#dont compare courses to themselves
                        print "---"
                        print "Same course(" + str(course1) + "), only need one of those you fool!"
                    else:
                        for section2 in coursesNestedBetter[course2]:
                            for class_time2 in coursesNestedBetter[course2][section2]:#see if the sections conflict
                                check1 = coursesNestedBetter[course1][section1]
                                check2 = coursesNestedBetter[course2][section2]
                                print "---"
                                print "Comparing " + course1 + section1 + " to " + course2 + section2
                                for meeting1 in check1:
                                    for meeting2 in check2:
                                        if meeting1[0] == meeting2[0]:
                                            print "* Meeting 1: " + str(meeting1)
                                            print "* Meeting 2: " + str(meeting2)
                                            if (isAllowed(meeting1,meeting2) == True):
                                                print "  * No conflict"
                                            else:
                                                print "  * Conflict"
                                                conflicts = conflicts + 1
                                            count = count + 1
                                        else:
                                            print "* Different days"
    print ""
    print "-----SUMMARY-----"
    print "checked for " + str(count) + " conflicts"
    print "found " + str(conflicts) + " conflicts"

#findAllConflicts()

def findAllGoodSchedules():
    '''This will loop through each section and compare each to a section of another course. If there is no conflict then it will continue into a section of the next course. If there is a conflict then the loop ends, and a comparison with the next section starts. Recursion could probably be used within the list of sections, I don't really know what memoization is yet but that could probably help stop a lot of repetition.'''
    count = 0
    conflicts = 0
    for course1 in coursesNestedBetter:
        for section1 in coursesNestedBetter[course1]:
            for class_time1 in coursesNestedBetter[course1][section1]:#go through all meeting times in all sections in all courses
                print "I think I need recursion"
    print "But I might be able to figure it out"

'''
Adding new schedules:
Use a list of dictionaries, or maybe a dictionary of dictionaries. The big one will hold all the schedules, each schedule with be a dictionary of 5 keys, one for each day, then the value will be a list of course numbers/sections on that day. Adding a new course is just appending to the list for that day, adding a new schedule is making deep copy of the previous dictionary then appending it to the list of dictionaries. A for loop can go through the list of schedules and some more for loops will check everything for conflicts.
Scaling, even on this small level, is a puzzle.
'''
'''
Resources:
https://www.etsu.edu/reg/documents/PDF/Use%20Schedule%20Builder%20to%20create%20a%20class%20schedule%20in%20the%20most%20efficient%20way%20possible.pdf
https://www.myedu.com/class-schedule/
http://sourceforge.net/projects/classschedulege/
https://code.google.com/p/schedule-generator/
http://www.softpedia.com/get/Office-tools/Diary-Organizers-Calendar/Class-Schedule-Generator.shtml
https://mubert.marshall.edu/csg/csg.php
http://www.collegescheduler.com/
http://www.uwec.edu/Registrar/upload/Schedule-Builder-Instructions.pdf
https://vsb.mcgill.ca/vsb/criteria.jsp
    This is a good one
http://www.collegeruled.com/
http://www.researchgate.net/profile/Tarek_Sobh3/publication/256456000_Course_Scheduler_An_Automated_Schedule_Generator/links/004635257164a77d4e000000.pdf
'''

'''
What if I loop through one at  time until I find a conflict, probably recursively. If a conflict is hit you stop. If not, then go through all courses and save that schedule, then start the next one
'''

'''
Read this too:
http://stackoverflow.com/questions/464864/python-code-to-pick-out-all-possible-combinations-from-a-list
'''
