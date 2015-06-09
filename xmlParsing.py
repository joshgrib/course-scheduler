#http://www.diveintopython3.net/xml.html
#XML CANNOT HAVE '&'s!!! REPLACE WITH 'and's!!!
import xml.etree.ElementTree as etree

tree = etree.parse('2015F.xml')
root = tree.getroot()

print root
print "There are " + str(len(root)) + " classes here."

def trialParsing():
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

trialParsing()

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
