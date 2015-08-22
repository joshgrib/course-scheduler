from flask import render_template, request, redirect, make_response
from app import app

import scheduler  # file with all the functions
import course_dict  # dictionary of all courses



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

@app.route('/how_many')
def how_many():
    return render_template("how_many.html")

@app.route('/how_many', methods=['GET','POST'])
def how_many_post():
    course_amount = request.form['course_amount']
    amount_of_courses = int(course_amount)
    resp = make_response(render_template("schedule_entry.html", quantity = amount_of_courses))
    resp.set_cookie('course_amount', str(amount_of_courses))
    return resp

@app.route('/schedules', methods=['GET','POST'])
def my_form_post():
    text_list = []
    amount_of_courses = int(request.cookies.get('course_amount'))
    for i in range(1, amount_of_courses+1):
        form_num = 'text' + str(i)
        text_list.append(request.form[form_num])
    final_list = []
    for text in text_list:
        if not text == "":
            final_list.append(text)
    printout = ""
    for course in final_list[:-1]:
        printout += (str(course) + ',')
    printout += str(final_list[-1])
    my_url = '/sched/' + printout
    return redirect(my_url)


@app.route('/sched/<someList>')
def scheduleMe(someList):
    # format the list into a python list based on the commas
    courseList = someList.split(',')
    deezCombos = scheduler.schedule(courseList)
    # render it all with the template
    return render_template("sched.html", title="Scheduler", combos=deezCombos)
