#TODO: comment everything

#http://www.diveintopython3.net/xml.html
#XML CANNOT HAVE '&'s!!! REPLACE WITH 'and's!!!
import xml.etree.ElementTree as etree #xml parsing stuff
import re #regex stuff

tree = etree.parse('2015F.xml')
root = tree.getroot()
#print root
print "There are " + str(len(root)) + " classes here."

def trialParsing():#useless
    '''This goes through and prints some stuff. It's more for me to learn have to parse the XML'''
    for course in root:
        attribs = course.attrib
        print attribs['Section']
        #print course[0].attrib
        meeting = course[0] #TODO: This only checks the first meeting rn
        info = meeting.attrib
        tbaCheck = info['Day']
        try:
            print info['Day']
            print info['StartTime']
            print info['EndTime']
        except KeyError:
            pass#print "Sorry key not there. Either the meeting time is TBA or this is CH 780A."
        print ""

def cleanupElements():#working
    '''This goes through the courses in the XML and removes any element that doesnt have info about meeting times'''
    for course in root.findall('Course'):
        #print course.get('Section')
        #current = course
        for element in course:
            #print element.tag, element.attrib
            if element.tag == 'Meeting':
                #print "Its a meeting!"
                pass
            else:
                #print "I dont need this!!!"
                course.remove(element) #for some reason this didn't get all of them the first time
                #print "Removed " + str(element) + " from " + str(course)
    tree.write('2015F.xml')
    print "\nUneccesary elements removed\n"
def cleanupCourses(courseList):#working
    '''This goes through the XML and removes any course not specified in the courseList from the tree'''
    for course in root.findall('Course'):
        name = course.get('Section')
        #print name
        while re.match("([A-Za-z-])", name[-1]) or re.match("([A-Za-z-])", name[-2]):
            name = name[:(len(name)-1)]
            #print "Deleted stuff"
            #print name
        #print name
        if name in courseList:
            #print "This belongs"
            pass
        else:
            #print "This does not belong"
            root.remove(course)
    tree.write('2015F.xml')
    print "\nUneccesary courses removed\n"

def fixTime(Time):
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


def parseXML():
    '''
    Psuedo-code
    Go through the courses
        Store course name and call number as variables
        Add both to the dictionary of call numbers
        Create a dictionary for the course
            For each section, create the list of meeting times store under the letter of the section within the course dictionary
                For each meeting time, get the letter, start time, end time
    Save it all to an external file with the dicionary of courses, and the dictionary of call numbers
    '''
    for course in root:
        bigDict = {} #yeah I got a big dict
        callNumbers = {}
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
        #print sectionName
        callNumber = int(course.attrib['CallNumber']) #get the call number as an integer
        #print callNumber
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
#AT THIS POINT - all classes and sections are added to the bigDict

        for meeting in course:
            info = meeting.attrib
            day =  info['Day']
            startTime = info['StartTime']
            endTime = info['EndTime']
            print day
            print startTime
            print endTime
            if len(day) == 1:
                bigDict[courseBig][courseSection].append([day,startTime,endTime])
            else:
                for letter in day:
                    bigDict[courseBig][courseSection].append([letter,startTime,endTime])

    print bigDict
    print "\nParsing complete\n"
parseXML()


def main(): #main function to do everything
    '''Given the XML and a list of courses, this will output all the possible schedules as a list of course ID(dept. ### section) and call numbers'''
    #ask for a courselist, maybe read from a file?
    cleanupCourses(courseList)
    cleanupElements()
    parseXML()
    findAllCombinations()#from the other file

#There needs to be one space between department and number
myCourses=["BT 353","CS 115","CS 115L","CS 135","CS 135L","CS 146","D 110","HHS 468"]

#cleanupCourses(myCourses)

#Schema references
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
    }
courseCodes = {\
    'BT  353A':10085,\
    'BT  353B':12010,\
    'BT  353C':12011,\
    'BT  353D':12012,\
    'BT  353E':12009,\
    'CS  115A':10472,\
    'CS  115B':10473,\
    'CS  115LA':10474,\
    'CS  115LB':10475,\
    'CS  115LC':10476,\
    'CS  115LD':10477,\
    'CS  115LE':10478,\
    'CS  115LF':11839,\
    'CS  135A':10479,\
    'CS  135LA':10480,\
    'CS  135LB':11840,\
    'CS  146A':10481,\
    'CS  146B':10482,\
    'D   110A':10583,\
    'HHS 468EV':11995\
    }
