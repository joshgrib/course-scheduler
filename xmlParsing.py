#http://www.diveintopython3.net/xml.html
#XML CANNOT HAVE '&'s!!! REPLACE WITH 'and's!!!
import xml.etree.ElementTree as etree
import re

tree = etree.parse('2015F.xml')
root = tree.getroot()

print root
print "There are " + str(len(root)) + " classes here."

def trialParsing():#working
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
        print course.get('Section')
        #current = course
        for element in course:
            print element.tag, element.attrib
            if element.tag == 'Meeting':
                print "Its a meeting!"
            else:
                print "I dont need this!!!"
                course.remove(element) #for some reason this didn't get all of them the first time
                print "Removed " + str(element) + " from " + str(course)
    tree.write('2015F.xml')

def cleanupCourses(courseList):#working
    '''This goes through the XML and removes any course not specified in the courseList from the tree'''
    for course in root.findall('Course'):
        name = course.get('Section')
        #print name
        while re.match("([A-Za-z-])", name[-1]) or re.match("([A-Za-z-])", name[-2]):
            name = name[:(len(name)-1)]
            #print "Deleted stuff"
            #print name
        print name
        if name in courseList:
            #print "This belongs"
        else:
            #print "This does not belong"
            root.remove(course)
    tree.write('2015F.xml')


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
    print "Time to parse"

#There needs to be one space between department and number
myCourses=["BT 353","CS 115","CS 115L","CS 135","CS 135L","CS 146","D 110","HHS 468"]

cleanupCourses(myCourses)

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
