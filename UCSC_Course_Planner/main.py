#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import csv
import cgi
import os
import re
import random
from webapp2 import redirect
from google.appengine.api import users
import datetime
from google.appengine.ext import db

from collections import defaultdict

import webapp2
from google.appengine.ext.webapp import template


class User(db.Model):
    name = db.StringProperty(required=True)
    join_date = db.DateProperty()
    email = db.StringProperty()
    userObject = db.UserProperty()
    major1 = db.StringProperty(required=False) #cmps/ee/cmpe
    major2 = db.StringProperty(required=False) #cmps/ee/cmpe
    major3 = db.StringProperty(required=False) #cmps/ee/cmpe
    minor1 = db.StringProperty(required=False) #cmps/ee/cmpe
    minor2 = db.StringProperty(required=False) #cmps/ee/cmpe
    minor3 = db.StringProperty(required=False) #cmps/ee/cmpe



class Login(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:


            greeting = (" <a href=\"%s\">Log out</a>" %
                        ( users.create_logout_url("/login")))
            logoutURL = users.create_logout_url("/login")
            is_logged_in = True
            name = user.nickname()

            userQuery = User.gql("WHERE name='{}'".format(name)).get()
            # self.response.write(userQuery)
            if (userQuery == None):
                e = User(name=user.nickname(),join_date=datetime.datetime.now().date(), email=users.get_current_user().email(),userObject=users.get_current_user())
                e.put()
                return redirect('/selectmajor')
            else:
                return redirect('/dashboard')
        else:
            greeting = ("<a href=\"%s\">Sign in or register</a>." %
                        users.create_login_url("/login"))
            is_logged_in = False
            logoutURL =  users.create_login_url("/")
            name = "no name"

        output = {
            'name': name,
            'is_logged_in': is_logged_in,
            'greeting': greeting,
            'logoutURL': logoutURL,
            }
        path = os.path.join(os.path.dirname(__file__), 'templates/login.html')
        self.response.write(template.render(path, output))

#         e = User(name="John",
#                  role="manager",
#                  email=users.get_current_user().email())
# e.hire_date = datetime.datetime.now().date()
# e.put()

class Dashboard(webapp2.RequestHandler):
    def get(self):
        from models import MajorRequirements, Progress, Course
        user = users.get_current_user()
        name = "none"
        if user:
            logURL = (users.create_logout_url("/"))
            name = user.nickname()
            is_logged_in = True
        else:

            logURL = ("/login")
            is_logged_in = False
            return redirect ('/login')

        userQuery = User.gql("WHERE name='{}'".format(user.nickname())).get()
        major1 = userQuery.major1
        major2 = userQuery.major2
        major3 = userQuery.major3
        minor1 = userQuery.minor1
        minor2 = userQuery.minor2
        minor3 = userQuery.minor3

        requirements = MajorRequirements.all().filter('major =', 'CMPS').fetch(limit=100)
        requirements = [course.course for course in requirements]
        completed = Progress.all().filter('user =', userQuery).fetch(limit=100)
        completed = [course.course for course in completed]
        available = ['{}-{}'.format(course.number, course.name) for course in requirements if course not in completed]
        output = {
            'major1': major1,
            'major2': major2,
            'major3': major3,
            'minor1': minor1,
            'minor2': minor2,
            'minor3': minor3,
            'logURL': logURL,
            'is_logged_in': is_logged_in,
            'name': name,
            'available': available,
            }
            
        path = os.path.join(os.path.dirname(__file__), 'templates/dashboard.html')
        self.response.write(template.render(path, output))

class Homepage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        name = "none"
        if user:
            logURL = (users.create_logout_url("/"))
            name = user.nickname()
            is_logged_in = True
        else:

            logURL = ("/login")
            is_logged_in = False

        output = {
            'logURL': logURL,
            'is_logged_in': is_logged_in,
            'name': name
            }

        path = os.path.join(os.path.dirname(__file__), 'templates/home.html')
        self.response.write(template.render(path, output))

class SelectMajor(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        name = "none"
        if user:
            logURL = (users.create_logout_url("/"))
            name = user.nickname()
            is_logged_in = True
        else:
            logURL = (users.create_login_url("/"))
            is_logged_in = False
            return redirect('/login')
        output = {
            'logURL': logURL,
            'is_logged_in': is_logged_in,
            'name': name
        }

        path = os.path.join(os.path.dirname(__file__), 'templates/selectmajor.html')
        self.response.write(template.render(path, output))

class MajorProgress(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        name = "none"
        if user:
            logURL = (users.create_logout_url("/"))
            name = user.nickname()
            is_logged_in = True
        else:
            logURL = (users.create_login_url("/"))
            is_logged_in = False
            return redirect('/login')


        userQuery = User.gql("WHERE name='{}'".format(user.nickname())).get()
        major1 = userQuery.major1
        major2 = userQuery.major2
        major3 = userQuery.major3
        minor1 = userQuery.minor1
        minor2 = userQuery.minor2
        minor3 = userQuery.minor3
        from models import MajorRequirements
        courses = MajorRequirements.gql("WHERE major='{}' ORDER by course DESC".format("CMPS")).fetch(limit=200)
        courses = [course.course for course in courses]
        # courses.order("-department")


        output = {
                'courses': courses,
                'major1': major1,
                'major2': major2,
                'major3': major3,
                'minor1': minor1,
                'minor2': minor2,
                'minor3': minor3,
                'logURL': logURL,
                'is_logged_in': is_logged_in,
                'name': name,

            }

        path = os.path.join(os.path.dirname(__file__), 'templates/majorprogress.html')
        self.response.write(template.render(path, output))

    def post(self):
        from models import Course, Progress
        user = users.get_current_user()
        course_numbers = (self.request.get('courses',  allow_multiple=True))
        current_user = User.all().filter('email =', user.email()).get()
        for course_number in course_numbers:
            course = Course.all().filter('number =',course_number).get()
            progress = Progress(user=current_user, course=course, completed=True)
            progress.put()
        return redirect('/dashboard')



class ListCourses(webapp2.RequestHandler):
    def get(self):
        reader = csv.DictReader(open('resources/dump.csv'))
        #departments = defaultdict(list)
        courses = [course for course in reader]
        regex = re.compile(r'Prerequisite\(s\):(.*)\.')
        for course in courses:
            description = course['description']
            result = regex.findall(description)
            if result:
                course['prereq'] = result[0]
        output = {
            'courses': courses,
        }
        path = os.path.join(os.path.dirname(__file__), 'templates/test.html')
        self.response.write(template.render(path, output))

class NotFoundPageHandler(webapp2.RequestHandler):
    def get(self):
        self.error(404)
        dognum = random.randint(0, 4)
        #self.response.out.write('Your 404 error html page')
        output = {
            'dognum': dognum,
            }
        path = os.path.join(os.path.dirname(__file__), 'templates/404.html')
        self.response.write(template.render(path, output))

class Contact(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        name = "none"
        if user:
            logURL = (users.create_logout_url("/"))
            name = user.nickname()
            is_logged_in = True
        else:
            logURL = (users.create_login_url("/"))
            is_logged_in = False
        output = {
            'logURL': logURL,
            'is_logged_in': is_logged_in,
            'name': name
        }

        path = os.path.join(os.path.dirname(__file__), 'templates/contact.html')
        self.response.write(template.render(path, output))
        
class About(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        name = "none"
        if user:
            logURL = (users.create_logout_url("/"))
            name = user.nickname()
            is_logged_in = True
        else:
            logURL = (users.create_login_url("/"))
            is_logged_in = False
        output = {
            'logURL': logURL,
            'is_logged_in': is_logged_in,
            'name': name
        }

        path = os.path.join(os.path.dirname(__file__), 'templates/about.html')
        self.response.write(template.render(path, output))

class Prerequisites(webapp2.RequestHandler):
    def get(self):
        from models import Course, Prerequisites
        courses = Course.all().order('department').fetch(limit=1000)
        print courses
        output = {
            'courses': courses,
        }
        path = os.path.join(os.path.dirname(__file__), 'templates/prereqs.html')
        self.response.write(template.render(path, output))


import cgi
import logging
class RecordPrereq(webapp2.RequestHandler):
    def get(self):
        from models import Prerequisites
        Prereqs = Prerequisites.all().fetch(limit=200)
        self.response.out.write('<br><br>'.join(map(repr, Prereqs)))

    def post(self):
        from models import Prerequisites, Course
        course = Course.gql("WHERE number='{}'".format(self.request.get('course'))).get()
        prereq = Course.gql("WHERE number='{}'".format(self.request.get('prerequisite'))).get()
        p = Prerequisites(course=course, prereq=prereq)
        p.put()


class TestModels(webapp2.RequestHandler):
    def get(self):
        from models import *

        from google.appengine.ext import db
        db.delete(Course.all())
        db.delete(Offerings.all())

        import re
        rx_department = re.compile(r'[A-Z]+')
        import csv
        reader = csv.DictReader(open('resources/dump.csv'))
        try:
            for course in reader:
                name = course['name']
                number = course['number']
                description = course['description'][:500]
                match = rx_department.match(number)
                department = number
                if match:
                    department = match.group(0)
                entry = Course(name=name, number=number, description=description, department=department)
                entry.put()

                for item in ['winter', 'spring', 'fall', 'summer']:
                    if 1 < len(course[item]):
                        offering = Offerings(course=entry, offered=item)
                        offering.put()
        except KeyError, e:
            pass
        courses = Course.all().order('department').fetch(limit=200)
        self.response.write('<br><br>'.join(map(repr, courses)))

class PopulateCourses(webapp2.RequestHandler):
    def get(self):
        from models import MajorRequirements, Course
        filename = 'resources/cmps_major.txt'
        file = open(filename)
        major = 'CMPS'
        db.delete(MajorRequirements.all())
        skip_flag = False
        for line in file.readlines():
            if line[0] == '\n': continue
            if line[0] == '#': continue
            if line[0] == '-': skip_flag = True;
            if skip_flag == True:
                skip_flag = False
                continue
            course = Course.gql("WHERE number='{}'".format(line.strip())).get()
            if course == None: continue
            requirement = MajorRequirements(major=major, course=course)
            requirement.put()
        requirements = MajorRequirements.all().fetch(limit=100)
        self.response.write('<br><br>'.join(map(repr, requirements)))

class MajorSelected(webapp2.RequestHandler):
    def post(self):
        user = users.get_current_user()

        userQuery = User.gql("WHERE name='{}'".format(user.nickname())).get()

        userQuery.major1 = cgi.escape(self.request.get('m1'))
        userQuery.major2 = cgi.escape(self.request.get('m2'))
        userQuery.major3 = cgi.escape(self.request.get('m3'))
        userQuery.minor1 = cgi.escape(self.request.get('mi1'))
        userQuery.minor2 = cgi.escape(self.request.get('mi2'))
        userQuery.minor3 = cgi.escape(self.request.get('mi3'))
        userQuery.put()

        # self.response.out.write("Very nice, Great Success!");


app = webapp2.WSGIApplication([
    ('/test', TestModels),
    ('/', Homepage),
    ('/dashboard', Dashboard),
    ('/courses', ListCourses),
    ('/login', Login),
    ('/selectMajor', SelectMajor),
    ('/selectmajor', SelectMajor),
    ('/majorprogress', MajorProgress),
    ('/progress', MajorProgress),
    ('/MajorSelected', MajorSelected),
    ('/Contact', Contact),
    ('/About', About),
    ('/prereqs', Prerequisites),
    ('/recordprereq', RecordPrereq),
    ('/populate', PopulateCourses),
    ('/.*', NotFoundPageHandler)

], debug=True)
