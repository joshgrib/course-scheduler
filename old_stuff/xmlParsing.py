#TODO: comment everything

#http://www.diveintopython3.net/xml.html
#XML CANNOT HAVE '&'s!!! REPLACE WITH 'and's!!!
import xml.etree.ElementTree as etree #xml parsing stuff
import re #regex stuff

tree = etree.parse('2015F.xml')
root = tree.getroot()
#print root
print "There are " + str(len(root)) + " classes here."

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
def parseXML():#working
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

        #TODO: stop duplicate writing for D110
        for meeting in course: #write the meetings to the section lists
            info = meeting.attrib
            day =  info['Day']
            startTime = info['StartTime']
            endTime = info['EndTime']
            #print day
            #print startTime
            # endTime
            if [day,startTime,endTime] in bigDict[courseBig][courseSection]: #if the exact same meeting is already in the list
                break #then dont add another!
            if len(day) == 1: #if this meeting describes one day
                bigDict[courseBig][courseSection].append([day,startTime,endTime]) #add the meeting time
            else: #if multiple days happen at the same time
                for letter in day: #add one list for each meeting
                    bigDict[courseBig][courseSection].append([letter,startTime,endTime])

    print bigDict
    print "\nParsing complete\n"

#There needs to be one space between department and number
myCourses=["BT 353","CS 115","CS 115L","CS 135","CS 135L","CS 146","D 110","HHS 468"]

def main(): #main function to do everything
    '''Given the XML and a list of courses, this will output all the possible schedules as a list of course ID(dept. ### section) and call numbers'''
    #ask for a courselist, maybe read from a file?
    cleanupCourses(myCourses)
    cleanupElements()
    parseXML()
    findAllCombinations()#from the other file

main()

'''
main should probably take in the xml file and the courselist, and output the possible schedules to a file
