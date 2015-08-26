from flask import Flask

app = Flask(__name__)

from flask import render_template, request, make_response, redirect

from settings import DEBUG


@app.route('/')
@app.route('/index')
def index():
    visited = request.cookies.get('visited')
    if visited == 'True':
        resp = make_response(
            render_template("index.html", title='Home', visted='True'))
    else:
        resp = make_response(
            render_template("index.html", title='Home', visited='False'))
        resp.set_cookie('visited', 'True', max_age=2592000, path='/')
    return resp


@app.route('/donate')
def donate():
    return render_template("donate.html", title='Donate')

import json
import os

@app.route('/courses')
def courses():
    my_dir = os.path.dirname(__file__)
    json_file_path = os.path.join(my_dir, 'courses.json')
    with open(json_file_path, 'r') as f:
        these_courses = json.load(f)
    # so I can list the courses in order
    sorted_courses = sorted(these_courses)
    course_letters = []
    for course in sorted_courses:
        if not course[0] in course_letters:
            course_letters.append(course[0])
    visited = request.cookies.get('visited')
    if visited == 'True':
        resp = make_response(render_template('courses.html',
                                             title='Courses',
                                             courses=these_courses,
                                             sorted_c=sorted_courses,
                                             letter_links=course_letters,
                                             visited='True'))
    else:
        resp = make_response(render_template('courses.html',
                                             title='Courses',
                                             courses=these_courses,
                                             sorted_c=sorted_courses,
                                             letter_links=course_letters,
                                             visited='False'))
        resp.set_cookie('visited', 'True', max_age=2592000, path='/')
    return resp


import scheduler


@app.route('/how_many')
def how_many():
    visited = request.cookies.get('visited')
    if visited == 'True':
        resp = make_response(
            render_template("how_many.html", title='Scheduler', visited='True'))
    else:
        resp = make_response(
            render_template("how_many.html", title='Scheduler', visited='False'))
        resp.set_cookie('visited', 'True', max_age=2592000, path='/')
    return resp


@app.route('/how_many', methods=['GET', 'POST'])
def how_many_post():
    course_amount = request.form['course_amount']
    amount_of_courses = int(course_amount)
    # for messing with CSS - remove once fixed
    test_courses = [
        'BT 353', 'CS 135', 'HH 0468', 'BT 181', 'CS 146', 'CS 284']
    resp = make_response(render_template(
        "schedule_entry.html", quantity=amount_of_courses, title='Scheduler', test_vals=test_courses))
    resp.set_cookie('course_amount', str(amount_of_courses), max_age=None)
    return resp


@app.route('/schedules', methods=['GET', 'POST'])
def my_form_post():
    text_list = []
    amount_of_courses = int(request.cookies.get('course_amount'))
    for i in range(1, amount_of_courses + 1):
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
    printout = printout.upper()
    my_url = '/sched/' + printout

    return redirect(my_url)


@app.route('/sched/<someList>')
def scheduleMe(someList):
    # format the list into a python list based on the commas
    courseList = someList.split(',')
    deezCombos = scheduler.schedule(courseList)
    # render it all with the template
    combo_count = str(len(deezCombos))
    return render_template("sched.html", title="Scheduler", combos=deezCombos, combo_amount=combo_count)

import secrets


@app.route('/add_course/<secret_code>')
def enterCourse(secret_code):
    if str(secret_code) == secrets.add_course_users():
        return render_template('add_course_form.html')
    else:
        return 'Sorry you cant use this page.<br><b>' + str(secret_code) + '</b> is not the secret code'


@app.route('/add_course', methods=['GET', 'POST'])
def addCourse():
    c_name = str(request.form['course_name'])
    l_info_maybe = str(request.form['lecture_info'])
    r_info_maybe = str(request.form['recitation_info'])
    h_info_maybe = str(request.form['homework_info'])
    e_info_maybe = str(request.form['exams_info'])
    f_info_maybe = str(request.form['final_info'])

    addition_info = {}
    if not l_info_maybe == "None":
        addition_info['Lecture'] = l_info_maybe
    if not r_info_maybe == "None":
        addition_info['Recitation'] = r_info_maybe
    if not h_info_maybe == "None":
        addition_info['Homework'] = h_info_maybe
    if not e_info_maybe == "None":
        addition_info['Exams'] = e_info_maybe
    if not f_info_maybe == "None":
        addition_info['Final'] = f_info_maybe

    my_dir = os.path.dirname(__file__)
    json_file_path = os.path.join(my_dir, 'courses.json')
    with open(json_file_path, 'r') as f:
        courses = json.load(f)
    courses[c_name] = {'info': addition_info}
    with open(json_file_path, 'w') as f:
        json.dump(courses, f)

    return render_template("index.html", title='Home', visted='True')

if DEBUG:
    app.run(debug = True)


def courses():
    my_dir = os.path.dirname(__file__)
    json_file_path = os.path.join(my_dir, 'courses.json')
    with open(json_file_path, 'r') as f:
        these_courses = json.load(f)
    return str(these_courses)
