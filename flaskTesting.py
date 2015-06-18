from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
	#index page
    return "Welcome to my super basic flask app!</br>Add /square/[number] to the url to square that number</br>Add /user/[username] to display that username</br>Add /list/[CSV] where CSV is a list of comma seperated values to print out the list items"

@app.route('/square/<number>')
def square(number):
	#square a number
	number = int(number)
	sqrNumber = number**2
	return str(number) + ' squared is: ' + str(sqrNumber) + '!<br></br><b>Click <a href="/">here</a> to return to home</b>'

@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return 'User %s<br></br><b>Click <a href="/">here</a> to return to home</b>' % username

@app.route('/sum/<num1>/<num2>')
def sumDeezNums(num1,num2):
	#add these numbers
	num1 = int(num1)
	num2 = int(num2)
	numSum=num1+num2
	return 'The sum of %d and %d is: %d</br>/br><b>Click <a href="/">here</a> to return to home</b>' %(num1,num2,numSum)

@app.route('/list/<list>')
def listFormat(list):
	myList = list.split(',')
	html = "Courses:</br>"
	for item in myList:
		html = html + str(item) + '</br>'
	html = html + '</br><b>Click <a href="/">here</a> to return to home</b>'
	return html

@app.route('/schedule/<list>')
def schedule(list):
	courseList = list.split(',')
	

if __name__ == '__main__':
    app.run()