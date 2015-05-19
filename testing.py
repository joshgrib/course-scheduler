'''
http://web.stevens.edu/scheduler/cor  2015F/sched_plus_crsemtg.txt
Got there by going back to the "core" part of the url then going to that text file (plus course meeting?)
'''

#heres the courses as on big dictionary
courses = {\
    'BT  353A' : ["M","1300","1350"] , \
    'BT  353A' : ["W","1100","1240"] , \
    'BT  353B' : ["M","1500","1640"] , \
    'BT  353B' : ["W","0900","0950"] , \
    'BT  353C' : ["T","1500","1640"] , \
    'BT  353C' : ["R","1100","1150"] , \
    'BT  353D' : ["T","1500","1640"] , \
    'BT  353D' : ["R","1100","1150"] , \
    'BT  353E' : ["M","1815","2045"] , \
    'CS  115A' : ["MWF","1200","1250"] , \
    'CS  115B' : ["MRF","1300","1350"] , \
    'CS  115LA' : ["R","0900","1040"] , \
    'CS  115LB' : ["R","1100","1240"] , \
    'CS  115LC' : ["R","1500","1640"] , \
    'CS  115LD' : ["R","1500","1640"] , \
    'CS  115LE' : ["F","1000","1140"] , \
    'CS  115LF' : ["F","1600","1740"] , \
    'CS  135A' : ["MWF","1000","1050"] , \
    'CS  135LA' : ["F","1100","1240"] , \
    'CS  135LB' : ["F","1300","1440"] , \
    'CS  146A' : ["TWF","0900","0950"] , \
    'CS  146B' : ["MTR","1400","1450"] , \
    'D   110A' : ["T","1700","1805"] , \
    'HHS 468EV' : ["M","1815","2045"]\
    }

uniqueCourses = []

print "Accessing different parts of dictionary and keys testing:"
for x in courses:
    #print x + " String length:" + str(len(x))
    #print "Course number: " + x[4:9]
    #print ""
    y = x[4:7]
    if (uniqueCourses.count(y) == 0):
        uniqueCourses.append(y)
    print uniqueCourses

collapsable_comments = [
    '''
    String idexes 4-6 have the course numbers
    20 sections total
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

#simple comparison for two classes in the format above - only compares for one day right now
def isAllowed(classList1, classList2):
    '''
    isAllowed():
                    |----------------|                      interval 1
    |----------|                                            end2<start1         True
                                            |-------|        end1<start2         True
    |------------------|                                  end2 !< start1      False
                                |---------------|          end1 !< start2      False
                |-------------------------|             end2 !< start1      False
                                                         &  end1 !< start2       False
                        |--------|                          end2 !< start1
                                                         &  end1 !< start2       False
    '''
    if (classList2[2] < classList1[1]) or (classList1[2] < classList2[1]):
        print 'No conflict!'
    else:
        print 'Conflict!'

print ""
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

print ""
print "Nested dictionaries testing:"
print coursesNested
print coursesNested["CS  146"]
print coursesNested["CS  146"]["A"]
#len(coursesNested["CS  146"]["A"][0]) could be a good way to figure out how many days each thing fits in then get the index of that string, then sort to that day
print coursesNested["CS  146"]["A"][0] + "are the days of the week this course is at this same time"
print str(len(coursesNested["CS  146"]["A"][0])) + " days of the week at the same time"

#possible schedule format
schedules = {\
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
