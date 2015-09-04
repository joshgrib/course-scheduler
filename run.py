#!/usr/bin/env python

# Standard libraries
import json
import os
import random
import smtplib
import hashlib
# downloaded
from flask import Flask, render_template, request, make_response, redirect, session
# files
from settings import PER_PAGE
import scheduler


app = Flask(__name__)


# Start of actual stuff


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
    default_courses = [
        'BT 353', 'CS 135', 'HHS 468', 'BT 181', 'CS 146', 'CS 284']
    resp = make_response(render_template(
        "schedule_entry.html", quantity=amount_of_courses, title='Scheduler', default_vals=default_courses))
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
    course_list = ""
    for course in final_list[:-1]:
        course_list += (str(course) + ',')
    course_list += str(final_list[-1])
    course_list = course_list.upper()
    #my_url = '/sched'

    real_course_list = course_list.split(',')
    my_combos = scheduler.schedule(real_course_list)
    resp = make_response(redirect('/sched'))
    resp.set_cookie('course_combos', json.dumps(my_combos))
    return resp


def getCombosForPage(page_num, per_page, count_of_combos, combos):
    """Returns the set of combos for the current page"""
    combos_start = (per_page * (page_num - 1)) + 1
    combos_end = combos_start + per_page
    these_combos = {}
    for key in range(combos_start, combos_end):
        try:
            # if new dict is not an int schedules are not sorted on the page
            these_combos[key] = combos[str(key)]
        except KeyError:
            pass
    return these_combos


def isLastPage(page_num, count_of_combos, per_page):
    """Return True if this is the last page in the pagination"""
    if count_of_combos <= (page_num * per_page):
        return True
    return False


@app.route('/sched/', defaults={'page': 1})
@app.route('/sched/page/<int:page>')
def scheduleMe(page):
    deezCombos = json.loads(request.cookies.get('course_combos'))
    count = len(deezCombos)
    if count > PER_PAGE:
        this_page_combos = getCombosForPage(page, PER_PAGE, count, deezCombos)
    else:
        this_page_combos = deezCombos
    last_page = isLastPage(page, count, PER_PAGE)
    if not this_page_combos and page != 1:
        return '404 - Not that many schedules'
    return render_template("sched.html",
                           title="Scheduler",
                           combos=this_page_combos,
                           combo_amount=str(count),
                           page=page,
                           last_page=last_page,
                           per_page=PER_PAGE)


if __name__ == '__main__':
    app.run(debug=True)
    session['hash_code'] = ""
