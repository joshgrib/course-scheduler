from flask import render_template
from app import app

import xml.etree.ElementTree as etree #xml parsing stuff
import re #regex stuff
import itertools #for finding combinations
import urllib #for getting xml from online
import pickle #to read/write from files hopefully better


#This would work iif there wasn't the error compiling the first time
url = 'https://web.stevens.edu/scheduler/core/2015F/2015F.xml'
urllib.urlretrieve(url, "xmlFile.xml") #import the xml file as 'xmlFile.xml'
xmlFile = "xmlFile.xml"

tree = etree.parse(xmlFile) #parse xml
root = tree.getroot() #get the root of the xml tree
pickle.dump( root, open( "rootSave.p", "wb" ) ) #save xml file
root = pickle.load( open( "rootSave.p", "rb" ) ) #load xml file

def cleanupElements():#working
    '''This goes through the courses in the XML and removes any element that doesnt have info about meeting times'''
    root = pickle.load( open( "rootSave.p", "rb" ) ) #open xml file
    for course in root.findall('Course'): #loop through all courses
        for element in course: #loop through the elements in each course
            if element.tag == 'Meeting': #if the element is a meeting leave it alone
                pass
            else: #if its not a meeting (its a prereq or something) then remove it
                course.remove(element) #for some reason this didn't get all of them the first time
    pickle.dump( root, open( "rootSave.p", "wb" ) ) #save file
def cleanupCourses(courseList):#working
    '''This goes through the XML and removes any course not specified in the courseList from the tree'''
    root = pickle.load( open( "rootSave.p", "rb" ) ) #open xml file
    for course in root.findall('Course'): #loop through all courses in the xml tree
        name = course.get('Section') #find the name of this course section
        while re.match("([A-Za-z-])", name[-1]) or re.match("([A-Za-z-])", name[-2]):
            name = name[:(len(name)-1)]
        if name in courseList: #if the course is in the list of courses to schedule, do nothing
            pass
        else: #if it's not on the list (and it doesn't know anyone here) then get rid of it
            root.remove(course)
    pickle.dump( root, open( "rootSave.p", "wb" ) ) #save xml file
def fixTime(Time):#working
    '''Fixes the time formatting'''
    root = pickle.load( open( "rootSave.p", "rb" ) ) #open the xml file
    Time = Time[:(len(Time)-4)]#remove the seconds and the Z
    if len(Time) == 4:#add the 0 to the front of early times
        Time = '0'+Time
    Time = Time[:2] + Time[3:] #get rid of the colon in the time format
    startHours = int(Time[:2])+4 #correct the 4 hour offset in times
    startHours = str(startHours)
    if len(startHours) == 1: #if its a single digit hour then add the 0 before it
        startHours = "0"+startHours
    Time = startHours + Time[2:]
    return Time
    pickle.dump( root, open( "rootSave.p", "wb" ) ) #save the xml file

#initialize data stores
bigDict = {} #yeah I got a big dict
callNumbers = {} #call numbers for the courses will go in this dictionary

def parseXML():#working
    root = pickle.load( open( "rootSave.p", "rb" ) )
    for course in root: #for all courses in the xml tree, fix the spacing between letters and numbers and fix time time formats
        attribs = course.attrib
        section = attribs['Section']
        #fix the spaces on the course names
        indexCount=0 #initialize counter
        newSection = "" #initialize blank string
        for letter in section: #for each letter...
            if letter == " ": #if its the space set the space equal to the right amount of spaces
                letter = (4-indexCount)*" "
            else: #if its a letter or number do nothing
                letter = letter
            newSection = newSection+letter #create the new name
            indexCount = indexCount+1 #add to counter
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
    for course in root: #add classes and section lists
        attribs = course.attrib
        thisCourse = attribs['Section']
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
    possibilities = ""
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

    possibilities = {}
    possibilities['combos']={}
    #possibilities['totalCombos']=str(combos)
    #possibilities['goodCombos']=str(goodCombos)
    comboCounter=1
    for x in goodCombos:
        urlPart = []
        possibilities['combos'][comboCounter]={}
        for course in x:
            urlPart.append(callNumbers[str(course)])
        #format url
        url = 'https://web.stevens.edu/scheduler/#2015F='
        for callNumber in urlPart:
            url = url + str(callNumber) + ","
        url = url[:-1]

        possibilities['combos'][comboCounter]['url']=str(url)
        possibilities['combos'][comboCounter]['list']=str(x)
        comboCounter = comboCounter + 1
    return possibilities
def checkCombination(courseDict,inputList):
    '''This will go through a combination list and see if it all works. If it does it will return a true value'''
    conflicts = 0 #initialize counters
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

def schedule(courseList): #main function to do everything
    '''Given the XML and a list of courses, this will output all the possible schedules as a list of course ID(dept. ### section) and call numbers'''
    root = pickle.load( open( "rootSave.p", "rb" ) )
    pickle.dump( root, open( "rootSave.p", "wb" ) )
    cleanupCourses(courseList)
    cleanupElements()
    root = pickle.load( open( "rootSave.p", "rb" ) )
    pickle.dump( root, open( "rootSave.p", "wb" ) )
    try:
        parseXML()
        return findAllCombinations(bigDict)#from the other file
    except KeyError:
        #try again - this needs to run twice for whatever reason
        schedule(courseList)

myList = ['BT 353','CS 135','HHS 468','BT 181','CS 146','CS 284']


@app.route('/')
@app.route('/index')
def index():
    user = {'nickname': 'Josh'}
    posts = [
        {
            'author': {'nickname': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'nickname': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        },
        {
            'author': {'nickname': 'Josh'},
            'body': 'Look I made a post'
        }
    ]
    return render_template("index.html",title='Home',user=user,)

@app.route('/sched')
def sched():
    return str(schedule(myList))

@app.route('/sched/<someList>')
def scheduleMe(someList):
    user = {'nickname': 'Josh'}
    courseList = someList.split(',')#format the list into a python list based on the commas
    schedResult = schedule(courseList)#schedule and save the dictionary
    return render_template("sched.html",user=user,combos=schedResult['combos'])#render it all with the template
