import copy
import itertools
'''
http://web.stevens.edu/scheduler/core/2015F/sched_plus_crsemtg.txt
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

def findAllCombinations():
    '''This function goes through the nested courses, stores lists of all possible combinations of courses, and prints them'''
    bigList=[]
    goodCombos=[]
    badCombos=[]
    for course in coursesNestedBetter:
        courseList=[]
        for section in coursesNestedBetter[course]:
            courseList.append(str(course+section))
            #print courseList
        bigList.append(courseList)
    print "The big list of lists: " + str(bigList)

    combos=0
    allCombos = list(itertools.product(*bigList))
    for combo in allCombos:
        print combo
        combos=combos+1
        checkCombination(combo)
        if checkCombination(combo) == True:
            print "NO CONFLICT HERE!!!"
            goodCombos.append(combo)
        else:
            print "WOAH FOUND A CONFLICT!!!"
            badCombos.append(combo)
    print "=========="
    print "SUMMARY"
    print "There are " + str(combos) + " possible combinations"
    print str(len(goodCombos)) + " of them work fine"
    print "The other " + str(len(badCombos)) + " had a conflict"
    print ""
    print "Good combinations:"
    for x in goodCombos:
        print x

def checkCombination(inputList):
    '''This will go through a combination list and see if it all works'''
    conflicts = 0
    diffDays = 0
    for i in range(len(inputList)-1):
        comp1 = inputList[i]
        if comp1[7] == 'L':
            course1 = comp1[0:8]
            section1 = comp1[8:]
        else:
            course1 = comp1[0:7]
            section1 = comp1[7:]
        comp2 = inputList[i+1]
        if comp2[7] == 'L':
            course2 = comp2[0:8]
            section2 = comp2[8:]
        else:
            course2 = comp2[0:7]
            section2 = comp2[7:]
        print "Comparing " + course1 + ' ' + section1 + " to " + course2 + ' ' + section2
        check1 = coursesNestedBetter[course1][section1]
        check2 = coursesNestedBetter[course2][section2]
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
    print "There were " + str(conflicts) + " conflicts"
    if conflicts == 0:
        return True

findAllCombinations()

'''
"BT  353A",M,0100PM,0150PM
"BT  353A",W,1100AM,1240PM
"BT  353B",M,0300PM,0440PM
"BT  353B",W,0900AM,0950AM
"BT  353C",T,0300PM,0440PM
"BT  353C",R,1100AM,1150AM
"BT  353D",T,0300PM,0440PM
"BT  353D",R,1100AM,1150AM
"BT  353E",M,0615PM,0845PM
"CS  115A",MWF,1200PM,1250PM
"CS  115B",MRF,0100PM,0150PM
"CS  115LA",R,0900AM,1040AM
"CS  115LB",R,1100AM,1240PM
"CS  115LC",R,0300PM,0440PM
"CS  115LD",R,0300PM,0440PM
"CS  115LE",F,1000AM,1140AM
"CS  115LF",F,0400PM,0540PM
"CS  135A",MWF,1000AM,1050AM
"CS  135LA",F,1100AM,1240PM
"CS  135LB",F,0100PM,0240PM
"CS  146A",TWF,0900AM,0950AM
"CS  146B",MTR,0200PM,0250PM
"CS  284A",MWF,1200PM,1250PM
"CS  284RA",M,0300PM,0350PM
"CS  284RB",M,0300PM,0350PM
"D   110A",T,0500PM,0605PM
"HHS 468EV",M,0615PM,0845PM
'''