import smtplib  # for sending the messages
import pickle  # for accessing the saved list/ dictionary files
import time  # for time delays
import random  # for random numbers
import sys  # for quitting the program
import secrets
import hashlib


def sendMsg():
    '''Takes in the name to identify the phone number address, and a message, and sends the message to the number'''
    login = secrets.send_message()
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(login['emailUsername'], login['emailPassword'])
    rand_code = random.randint(0, 999999)
    server.sendmail(
        'Messages',
        login['phone_number'],
        str(rand_code))
    print "Code is: " + str(rand_code)
    h = hashlib.md5()
    h.update(str(rand_code))
    hash_code = h.hexdigest()
    #Save hash code as a cookie
    return hash_code


if __name__ == '__main__':
    hash_code = sendMsg()
    text = raw_input('What is the code?')
    j = hashlib.md5()
    j.update(str(text))
    hash_text = j.hexdigest()
    if hash_code == hash_text:
        print 'Correct'
    else:
        print 'Incorrect'
