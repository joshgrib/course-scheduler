from bottle import route, run, template

@route('/')
def index():
	return template

@route('/hello/<name>')
def index(name):
    return template('<b>Hello {{name}}</b>!', name=name)

@route('/square/<number>')
def square(number):
	number = int(number)
	number2 = number**2
	return template('<b>{{number2}}</b>!', number2=str(number2))

run(host='localhost', port=8080)
