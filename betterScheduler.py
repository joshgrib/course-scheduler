#XML CANNOT HAVE '&'s!!! REPLACE WITH 'and's!!!
import xml.etree.ElementTree as etree #xml parsing stuff
import re #regex stuff
import itertools #for finding combinations
import time
import urllib

#This would work iif there wasn't the error compiling the first time
url = 'https://web.stevens.edu/scheduler/core/2015F/2015F.xml'
urllib.urlretrieve(url, "xmlFile.xml")

xmlFile = "2015f2.xml"
#There needs to be one space between department and number
myCourses=["BT 353","CS 115","CS 115L","CS 135","CS 135L","CS 146","D 110","HHS 468"]

tree = etree.parse(xmlFile)
root = tree.getroot()
#print root
print "There are " + str(len(root)) + " classes here."

def cleanupElements():#working
    '''This goes through the courses in the XML and removes any element that doesnt have info about meeting times'''
    for course in root.findall('Course'):
        for element in course:
            if element.tag == 'Meeting':
                pass
            else:
                course.remove(element) #for some reason this didn't get all of them the first time
    tree.write(xmlFile)
    #time.sleep(5)
    print "=====Uneccesary elements removed====="
def cleanupCourses(courseList):#working
    '''This goes through the XML and removes any course not specified in the courseList from the tree'''
    for course in root.findall('Course'):
        name = course.get('Section')
        while re.match("([A-Za-z-])", name[-1]) or re.match("([A-Za-z-])", name[-2]):
            name = name[:(len(name)-1)]
        if name in courseList:
            pass
        else:
            root.remove(course)
    tree.write(xmlFile)
    print "=====Uneccesary courses removed====="
def fixTime(Time):#working
    '''Fixes the time formatting'''
    Time = Time[:(len(Time)-4)]#remove the seconds and the Z
    if len(Time) == 4:#add the 0 to the front of early times
        Time = '0'+Time
    Time = Time[:2] + Time[3:]
    startHours = int(Time[:2])+4
    startHours = str(startHours)
    if len(startHours) == 1:
        startHours = "0"+startHours
    Time = startHours + Time[2:]
    return Time
bigDict = {} #yeah I got a big dict
callNumbers = {}
def parseXML():#working
    for course in root:
        attribs = course.attrib

        section = attribs['Section']
        #fix the spaces on the course names
        indexCount=0#initialize counter
        newSection = ""
        for letter in section:#fore each letter...
            if letter == " ":#if its the space set the space equal to the right amount of spaces
                #print "Space at index:" + str(indexCount)
                letter = (4-indexCount)*" "
            else:
                letter = letter
            newSection = newSection+letter#create the new name
            indexCount = indexCount+1
        attribs['Section']=newSection

        #fix time formatting
        for meeting in course:
            meetingAttribs = meeting.attrib
            startTime = meetingAttribs['StartTime']
            endTime = meetingAttribs['EndTime']
            startTime = fixTime(startTime)
            endTime = fixTime(endTime)
            meetingAttribs['StartTime'] = startTime
            meetingAttribs['EndTime'] = endTime

    #populate call number dictionary
    for course in root:
        sectionName = course.attrib['Section'] #get the section name
        callNumber = int(course.attrib['CallNumber']) #get the call number as an integer
        callNumbers[sectionName] = callNumber #save section names and call numbers to the dictionary

    '''
    At this point in the function:
    Course names are properly formatted, with the proper number of spaces, one for every section, stored under the 'Section' attribute
    Start and end times are properly formatted, store as the StatTime and EndTime attributes
    The dictionary for call numbers is done
    '''

    prevCourse = ""
    for course in root:
        attribs = course.attrib
        thisCourse = attribs['Section']
        print thisCourse
        if len(thisCourse) == 9: #recitation course
            courseBig = thisCourse[:8]
            courseSection =thisCourse[8:]
            if courseBig == prevCourse[:8]: #same course
                bigDict[courseBig][courseSection] = [] #add the new section with a list
            else: #new course
                bigDict[courseBig] = {} #add the new class
                bigDict[courseBig][courseSection] = [] #add the new section with a list
        else: #normal course(lecture)
            courseBig = thisCourse[:7]
            courseSection =thisCourse[7:]
            if thisCourse[:7] == prevCourse[:7]: #same course
                bigDict[courseBig][courseSection] = [] #add the new section with a list
            else: #new course
                bigDict[courseBig] = {} #add the new class
                bigDict[courseBig][courseSection] = [] #add the new section with a list
        prevCourse = thisCourse

        for meeting in course: #write the meetings to the section lists
            info = meeting.attrib
            day =  info['Day']
            startTime = info['StartTime']
            endTime = info['EndTime']
            if [day,startTime,endTime] in bigDict[courseBig][courseSection]: #if the exact same meeting is already in the list
                break #then dont add another!
            if len(day) == 1: #if this meeting describes one day
                bigDict[courseBig][courseSection].append([day,startTime,endTime]) #add the meeting time
            else: #if multiple days happen at the same time
                for letter in day: #add one list for each meeting
                    bigDict[courseBig][courseSection].append([letter,startTime,endTime])

    print bigDict
    print "\nParsing complete\n"
def isAllowed(classList1, classList2):
    if (classList2[2] < classList1[1]) or (classList1[2] < classList2[1]):
        return True
    else:
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
        bigList.append(courseList)
    combos=0 #initialize the counter
    allCombos = list(itertools.product(*bigList))#find all combinations of one section of each class
    for combo in allCombos:
        combos=combos+1
        checkCombination(courseDict,combo)#see if the combo works and add to apppropriate list
        if checkCombination(courseDict,combo) == True:
            goodCombos.append(combo)
        else:
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
            urlPart.append(callNumbers[str(course)])
        #format url
        url = 'https://web.stevens.edu/scheduler/#2015F='
        for callNumber in urlPart:
            url = url + str(callNumber) + ","
        url = url[:-1]
        print url
def checkCombination(courseDict,inputList):
    '''This will go through a combination list and see if it all works. If it does it will return a true value'''
    conflicts = 0 #initialize counters
    diffDays = 0
    for i in range(len(inputList)-1): #compare each item in the list to each other, I dont remember what I did here rn, should have commented earlier
        comp1 = inputList[i] #comparison one in the item in the list we are on now
        if len(comp1) == 9: #seperate the section and the course, different if its a lecture
            course1 = comp1[0:8]
            section1 = comp1[8:]
        else:
            course1 = comp1[0:7]
            section1 = comp1[7:]

        comp2 = inputList[i+1] #comparison two is the next item in the list
        if len(comp2) == 9: #seperate the section and the course, different if its a letter
            course2 = comp2[0:8]
            section2 = comp2[8:]
        else:
            course2 = comp2[0:7]
            section2 = comp2[7:]
        check1 = courseDict[course1][section1] #check one is the list of meetings for course1 section1
        check2 = courseDict[course2][section2] #check two is the list of meetings for course2 section2
        for meeting1 in check1:
            for meeting2 in check2:
                if meeting1[0] == meeting2[0]: #if the meetins are on the same day...
                    if (isAllowed(meeting1,meeting2) == True): #if there is no conflicts do nothing
                        pass
                    else: #if there is a conflict, add to the conflict counter
                        conflicts = conflicts + 1
    if conflicts == 0: #if there were no conflicts, return true
        return True

def main(): #main function to do everything
    '''Given the XML and a list of courses, this will output all the possible schedules as a list of course ID(dept. ### section) and call numbers'''
    #ask for a courselist, maybe read from a file?
    cleanupCourses(myCourses)
    cleanupElements()
    parseXML()
    findAllCombinations(bigDict)#from the other file

main()

'''
TODO
main should probably take in the xml file and the courselist, and output the possible schedules to a file
Add a step to remove the extra D110's
'''
