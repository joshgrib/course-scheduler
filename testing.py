import copy
'''
http://web.stevens.edu/scheduler/cor  2015F/sched_plus_crsemtg.txt
Got there by going back to the "core" part of the url then going to that text file (plus course meeting?)
'''

collapsable_comments = [
    '''
    String idexes 4-6 have the course numbers
    20 sections for 6 courses
    432 possibilities, low enough that blunt-force should work fine
    Start with classes where there's only one section, if theres a conflict there, stop and say the schedule isn't possibilities
    Then go to the next ones with 2 sections, then 3, etc
    If Any of those conflict with something with 1 section, remove it as a possibility and continue

    5 lists, on for every day of the week.
    There isn't a conflict as long as end1<start2 or end2<start1
    '''

    '''
    Talking through the code for scheduling:
    First get all the coursed ordered from most to least sections
    Anything with one section can be put right in
    Then starting with the least sections see what doesn't have conflicts and make a new schedule for every one that can be put it.
    For the next class all sections will need to be checked against all other schedules
    '''

    '''
    TODO eventually:
    figure out regex to go from xml, delete all classes that aren't needed, then format nice
    '''
]

def isAllowedTesting():
    print "isAllowed() testing:"
    isAllowed(courses['CS  115A'], courses['BT  353D'])     #no conflict
    isAllowed(courses['CS  115A'], courses['BT  353A'])     #conflict

#heres the courses as a big nested dictionary thing
coursesNested = {\
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
        "E":["M","1815","2045"]\
        },\
    "CS  115":{\
        "A":["MWF","1200","1250"],\
        "B":["MRF","1300","1350"]\
        },\
    "CS  115L":{\
        "A":["R","0900","1040"],\
        "B":["R","1100","1240"],\
        "C":["R","1500","1640"],\
        "D":["R","1500","1640"],\
        "E":["F","1000","1140"],\
        "F":["F","1600","1740"]\
        },\
    "CS  135":{\
        "A":["MWF","1000","1050"]\
        },\
    "CS  135L":{\
        "A":["F","1100","1240"],\
        "B":["F","1300","1440"]\
        },\
    "CS  146":{\
        "A":["TWF","0900","0950"],\
        "B":["MTR","1400","1450"]\
        },\
    "D   110":{\
        "A":["T","1700","1805"]\
        },\
    "HHS 468":{\
        "EV":["M","1815","2045"]\
        }\
    }
def nestedDictionaryTesting():
    print "Nested dictionaries testing:"
    print coursesNested
    print coursesNested["CS  146"]
    print coursesNested["CS  146"]["A"]
    #len(coursesNested["CS  146"]["A"][0]) could be a good way to figure out how many days each thing fits in then get the index of that string, then sort to that day
    print coursesNested["CS  146"]["A"][0] + "are the days of the week this course is at this same time"
    print str(len(coursesNested["CS  146"]["A"][0])) + " days of the week at the same time"

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

def courseLoopingTesting():
    '''This goes through all the stuff and gets down to the important info for each section'''
    #go through each course and print it
    for course in coursesNested:
        print course
        #go through each section in each course and print it
        for section in coursesNested[course]:
            print "    " + section
            #go through the info for each section
            for class_time in coursesNested[course][section]:
                #if it's just the days and times, print them
                if str(class_time) == class_time:
                    print "        " + str(class_time)
                #if its not (so its a list of 2 or more lists), then break it down again and then print the days and times
                else:
                    for other_day in class_time:
                        print "        " + str(other_day)

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


'''====================================================================================================='''

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

def theyChoseThatSchemaBecauseTheyHateMe():
    '''New nested course list makes schema more consistent because all sections have a list of lists regardless of how many meetings there are or if they all meet at the same time each day. From here I should be able to go through and get the values of class_time[1] and class_time[2] as the start and end times, then I can put them into the conflict-checker function and make some schedules!!!'''
    count = 0
    for course in coursesNestedBetter:
        print course
        #go through each section in each course and print it
        for section in coursesNestedBetter[course]:
            print "    " + section
            #go through the info for each section
            for class_time in coursesNestedBetter[course][section]:
                #break it down again and then print the days and times
                print "        Day: " + class_time[0]
                print "        Start: " + class_time[1]
                print "        End: " + class_time[2]
            #print "Done with sections"
        #print "Done with courses"
    #print "Done with dictionary"

def checkTheseCoursesForConflicts():
    '''Given two course sections in the format of coursesNestedBetter[course][section], check for conflicts through all meetings for that section.'''
    #choose first course and section
    print "Choose course 1"
    for course in coursesNestedBetter:
        print course
    course1 = raw_input()
    print "Choose section of " + course1
    for section in coursesNestedBetter[course1]:
        print section
    section1 = raw_input()
    #get the meeting times
    check1 = coursesNestedBetter[course1][section1]

    #choose the second course and section
    print "Choose course 2"
    for course in coursesNestedBetter:
        print course
    course2 = raw_input()
    print "Choose section of " + course2
    for section in coursesNestedBetter[course2]:
        print section
    section2 = raw_input()
    #get the meeting times
    check2 = coursesNestedBetter[course2][section2]

    #pritn it nicely
    print course1 + section1 + ": " + str(check1)
    print course2 + section2 + ": " + str(check2)

    for meeting1 in check1:#loop through the first sections meeting times
        for meeting2 in check2:#loop through the second sections meeting times
            if meeting1[0] == meeting2[0]: #if meeting on the same day
                isAllowed(meeting1,meeting2)
            else:
                print "Different days, not a problem!"

#checkTheseCoursesForConflicts()

'''====================================================================================================='''

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
            for class_time1 in coursesNestedBetter[course1][section1]:
                for course2 in coursesNestedBetter:
                    for section2 in coursesNestedBetter[course2]:
                        for class_time2 in coursesNestedBetter[course2][section2]:
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
    print "checked for " + str(count) + " conflicts"
    print "found " + str(conflicts) + " conflicts"

findAllConflicts()


'''
Adding new schedules:
Use a list of dictionaries, or maybe a dictionary of dictionaries. The big one will hold all the schedules, each schedule with be a dictionary of 5 keys, one for each day, then the value will be a list of course numbers/sections on that day. Adding a new course is just appending to the list for that day, adding a new schedule is making deep copy of the previous dictionary then appending it to the list of dictionaries. A for loop can go through the list of schedules and some more for loops will check everything for conflicts.
Scaling, even on this small level, is a puzzle.
'''
