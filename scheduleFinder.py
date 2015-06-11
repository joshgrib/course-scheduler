#TODO: GO through, comment more, and remove all the debugging print statements

#import copy
import itertools
'''
http://web.stevens.edu/scheduler/core/2015F/sched_plus_crsemtg.txt
Got there by going back to the "core" part of the url then going to that text file (plus course meeting?)
'''

coursesNesterBetter = {\
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

newCourseList = {'CS  115': {'A': [['M', '1200', '1250'], ['W', '1200', '1250'], ['F', '1200', '1250']], 'B': [['M', '1300', '1350'], ['R', '1300', '1350'], ['F', '1300', '1350']]}, 'CS  115L': {'A': [['R', '0900', '1040']], 'C': [['R', '1500', '1640']], 'B': [['R', '1100', '1240']], 'E': [['F', '1000', '1140']], 'D': [['R', '1500', '1640']], 'F': [['F', '1600', '1740']]}, 'CS  135': {'A': [['M', '1000', '1050'], ['W', '1000', '1050'], ['F', '1000', '1050']]}, 'CS  135L': {'A': [['F', '1100', '1240']], 'B': [['F', '1300', '1440']]}, 'BT  353': {'A': [['M', '1300', '1350'], ['W', '1100', '1240']], 'C': [['T', '1500', '1640'], ['R', '1100', '1150']], 'B': [['M', '1500', '1640'], ['W', '0900', '0950']], 'E': [['M', '1815', '2045']], 'D': [['T', '1500', '1640'], ['R', '1100', '1150']]}, 'HHS 468': {'EV': [['M', '1815', '2045']]}, 'CS  146': {'A': [['T', '0900', '0950'], ['W', '0900', '0950'], ['F', '0900', '0950']], 'B': [['M', '1400', '1450'], ['T', '1400', '1450'], ['R', '1400', '1450']]}, 'D   110': {'A': [['T', '1700', '1805']]}}

courseCodes = {'BT  353A':10085,'BT  353B':12010,'BT  353C':12011,'BT  353D':12012,'BT  353E':12009,'CS  115A':10472,'CS  115B':10473,'CS  115LA':10474,'CS  115LB':10475,'CS  115LC':10476,'CS  115LD':10477,'CS  115LE':10478,'CS  115LF':11839,'CS  135A':10479,'CS  135LA':10480,'CS  135LB':11840,'CS  146A':10481,'CS  146B':10482,'D   110A':10583,'HHS 468EV':11995}

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

def findAllCombinations(courseDict):
    '''This function goes through the nested courses, stores lists of all possible combinations of courses, and prints them'''
    bigList=[] #list of lists of courses and sections
    goodCombos=[] #store all the good combinations
    badCombos=[] #store the bad combinations
    for course in courseDict: #make a list of lists with the small lists being lists of possible sections for one course
        courseList=[]
        for section in courseDict[course]:
            courseList.append(str(course+section))
            #print courseList
        bigList.append(courseList)
    #print "The big list of lists: " + str(bigList)
    combos=0 #initialize the counter
    allCombos = list(itertools.product(*bigList))#find all combinations of one section of each class
    for combo in allCombos:
        #print combo
        combos=combos+1
        checkCombination(courseDict,combo)#see if the combo works and add to apppropriate list
        if checkCombination(courseDict,combo) == True:
            #print "NO CONFLICT HERE!!!"
            goodCombos.append(combo)
        else:
            #print "WOAH FOUND A CONFLICT!!!"
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
        urlPart = []
        for course in x:
            urlPart.append(courseCodes[str(course)])
        print urlPart

def checkCombination(courseDict,inputList):
    '''This will go through a combination list and see if it all works. If it does it will return a true value'''
    conflicts = 0 #initialize counters
    diffDays = 0
    for i in range(len(inputList)-1): #compare each item in the list to each other, I dont remember what I did here rn, should have commented earlier
        comp1 = inputList[i] #comparison one in the item in the list we are on now
        if comp1[7] == 'L': #seperate the section and the course, different if its a lecture
            course1 = comp1[0:8]
            section1 = comp1[8:]
        else:
            course1 = comp1[0:7]
            section1 = comp1[7:]

        comp2 = inputList[i+1] #comparison two is the next item in the list
        if comp2[7] == 'L': #seperate the section and the course, different if its a letter
            course2 = comp2[0:8]
            section2 = comp2[8:]
        else:
            course2 = comp2[0:7]
            section2 = comp2[7:]
        #print "Comparing " + course1 + ' ' + section1 + " to " + course2 + ' ' + section2
        check1 = courseDict[course1][section1] #check one is the list of meetings for course1 section1
        check2 = courseDict[course2][section2] #check two is the list of meetings for course2 section2
        for meeting1 in check1:
            for meeting2 in check2:
                if meeting1[0] == meeting2[0]: #if the meetins are on the same day...
                    #print "* Meeting 1: " + str(meeting1)
                    #print "* Meeting 2: " + str(meeting2)
                    if (isAllowed(meeting1,meeting2) == True): #if there is no conflicts do nothing
                        #print "  * No conflict"
                        pass
                    else: #if there is a conflict, add to the conflict counter
                        #print "  * Conflict"
                        conflicts = conflicts + 1
    #print "There were " + str(conflicts) + " conflicts"
    if conflicts == 0: #if there were no conflicts, return true
        return True

findAllCombinations(newCourseList)

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

'''
http://web.stevens.edu/scheduler/#2015F=#####,#####,#####,#####
'''

#Python xml parsing: https://docs.python.org/2/library/xml.etree.elementtree.html
