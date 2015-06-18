from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
	#index page
    return "Welcome to my super basic flask app!</br>Add /square/[number] to the url to square that number</br>Add /user/[username] to display that username"

@app.route('/square/<number>')
def square(number):
	#square a number
	number = int(number)
	number = number**2
	return '<b>'+str(number)+'</b>!<br>Click <a href="/">here</a> to return to home'
	
@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return 'User %s<br>Click <a href="/">here</a> to return to home' % username

@app.route('/sum/<num1>/<num2>')
def sumDeezNums(num1,num2):
	#add these numbers
	num1 = int(num1)
	num2 = int(num2)
	numSum=num1+num2
	return 'The sum of %d and %d is: %d' %(num1,num2,numSum)

if __name__ == '__main__':
    app.run()