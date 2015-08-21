from flask import render_template
from app import app
import scheduler  # file with all the functions
import course_dict  # dictionary of all courses
import forms  # login form ish


@app.route('/')
@app.route('/index')
def index():
    user = {'nickname': 'Josh'}
    return render_template("index.html", title='Home', user=user,)


@app.route('/donate')
def donate():
    return render_template("donate.html", title='Donate')


@app.route('/courses')
def courses():
    these_courses = course_dict.getMeCourses()
    sorted_courses = sorted(these_courses)
    return render_template('courses.html', title='Courses', courses=these_courses, sorted_c=sorted_courses)


@app.route('/scheduler')
def scheduler():
    pass


@app.route('/sched/<someList>')
def scheduleMe(someList):
    # format the list into a python list based on the commas
    courseList = someList.split(',')
    deezCombos = scheduler.schedule(courseList)
    # render it all with the template
    return render_template("sched.html", title="Scheduler", combos=deezCombos)
