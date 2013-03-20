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
from google.appengine.ext.webapp import template, logging


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
        from datetime import date
        import itertools
        import operator

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
        m1prog = "30";
        m2prog = "20";
        m3prog = "10";
        mi1prog = "10";
        mi2prog = "15";
        mi3prog = "50";

        requirements = MajorRequirements.all().filter('major =', 'CMPS').fetch(limit=100)
        requirements = [course.course for course in requirements]
        completed1 = Progress.all().filter('user =', userQuery).order('year').order('quarter').fetch(limit=100)
        completed = [course.course for course in completed1]

        #  any(quarter == chances.quarter for chances in progCheck):
        available = ['{}-{}'.format(course.number, course.name) for course in requirements if course not in completed]
        maxyear = date.today().year + 5
        # years = tuple((str(n-1), str(n)) for n in range(date.today().year, date.today().year + 5))
        years = list((str(n-1) + " - " + str(n)) for n in range(date.today().year, date.today().year + 5))
        # shortyears = list(years)
        shortyears = list(("Fall" + str(n-1)[2:], "Winter" + str(n)[2:], "Spring" + str(n)[2:], "Summer" + str(n)[2:]) for n in range(date.today().year, date.today().year + 5))
        shortyears2 = list((str(n-1)[2:]) for n in range(date.today().year, date.today().year + 5))

        quarterlist = [ "Fall", "Winter", "Spring", "Summer"]
        # prog2 = Progress.all().filter('user =', userQuery).fetch(limit=10)
        allyears = []
        for year in shortyears2:
            allClasse = []
            for quarter in quarterlist:
                prog2 = Progress.all().filter('user =', userQuery)
                prog2 = prog2.filter('quarter =', quarter)
                prog2 = prog2.filter('year =', int(year))
                prog2 = prog2.fetch(limit=10)
                prog2 = [course1.course.number for course1 in prog2]
                classes = [quarter+str(year), prog2]
                allClasse.append(classes)
            # year = "20" + str(year)
            allyears.append([year,allClasse])
        # completed1 = Progress.all().filter('user =', userQuery).fetch(limit=100)

        # for course in completed1:
        #     course.quarter
        # curr = tuple('{}{}-{}'.format(course1.quarter, course1.year, course1.course.number) for course1 in completed1)
        # curr = list((course1.quarter, course1.year, course1.course.number) for course1 in completed1)
        # curr2 = list()
        # for key,group in itertools.groupby(curr,operator.itemgetter(0)):
        #     curr2.append((list(group)))

        # curr =curr2
        # curr3 = []
        # for listy in curr2:
        #     list1 = []
        #     for tup in listy:
        #         list1.append(listy[0])
        #     curr3.append(list1)
        # curr = curr3
        Fall12Classes   = tuple(("AMS20", "CMPS101","CMPE100"))
        Winter13Classes = tuple(("AMS20", "CMPS101","CMPE100"))
        # shortyears = zip(shortyears,curr)
        # shortyears = zip(years,shortyears)
        # year = curr
        logging = str(allyears)
        # maxyear = max(maxyear, maxyear2)
        # logging.debug(maxyear)
        output = {
            'quarterlist': quarterlist,
            'logging': logging,
            'allyears': allyears,
            'major1': major1,
            'major2': major2,
            'major3': major3,
            'minor1': minor1,
            'minor2': minor2,
            'minor3': minor3,
            'm1prog': m1prog,
            'm2prog': m2prog,
            'm3prog': m3prog,
            'mi1prog': mi1prog,
            'mi2prog': mi2prog,
            'mi3prog': mi3prog,
            'years': years,
            'shortyears': shortyears,
            'logURL': logURL,
            'is_logged_in': is_logged_in,
            'name': name,
            'available': available,
            }
            
        path = os.path.join(os.path.dirname(__file__), 'templates/dashboard.html')
        self.response.write(template.render(path, output))

    def post(self):
        from models import Course, Progress
        user = users.get_current_user()
        course_numbers = (self.request.get_all('courses[]'))
        current_user = User.all().filter('email =', user.email()).get()
        myclasses = []
        myclasses2 = []
        for classy in course_numbers:
            test = [x.strip() for x in classy.split(',')]
            myclasses.append(test)
        for classy in myclasses:
            coursename = classy[0].replace(" ", "")
            coursetime = classy[1]
            myclasses2.append((coursename,coursetime))

        # [u'Fall12,PHYS 5A,Fall12,PHYS 5L,Fall12,CMPS 12B,Fall12,CMPS 12L,Fall12,CMPE 16,',
        #  u'Winter13,HCI 131 ,Winter13,CMPS 101 ,Winter13,DANM 250,Winter13,Math 21 ,',
        #  u'Spring13,PHYSC 5C,Spring13,PHYSC 5L,Spring13,AMS 131,',
        #  u'Summer13,CMPS109,Summer13,Math 24,']
        # myclasses = filter(None, myclasses)
        # test = [x.strip() for x in myclasses[0].split(',')]
        progCheck = Progress.all().filter('user =', current_user).fetch(limit=1000)
        db.delete(progCheck)

        for course_number in myclasses:

            coursename = course_number[0].replace(" ", "")
            quarter = course_number[1][:-2]
            year = int(course_number[1][-2:])
            course = Course.all().filter('number =',coursename).get()
            progress = Progress(user=current_user, course=course, completed=True, quarter=quarter, year=year)
            if (course != None):
                progress.put()


            # if (course != None):
            #     quarter = course_number[1][:-2]
            #     year = int(course_number[1][-2:])
            #     # need to figure out how to query for specific course
            #     # so that we can remove it if neccessary
            #     progress = Progress(user=current_user, course=course, completed=True, quarter=quarter, year=year)
            #     progCheck = Progress.all().filter('user =', current_user).filter('course =', course).fetch(limit=20)
            #     # if (progCheck.quarter != quarter):
            #     #     progress.put()
            #     #     #then remove the old class here too....
                log = ""
            #     if not progCheck:
            #         progress.put()
            #         log = "progCheck==None , " + str(course_number)
            #     else:
            #         if not any(quarter == chances.quarter for chances in progCheck):
            #             progress.put()
            #         # for chances in progCheck:
            #         #     if (chances.quarter != quarter):
            #         #         itsHere


                # progress.put()
        self.response.write(log + str(myclasses2));

        # self.response.write("test" + str(course_numbers));
        #return redirect('/dashboard')

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
        import logging
        from models import Course, Progress
        user = users.get_current_user()
        args = self.request.arguments()
        course_numbers = []
        # logging.debug("test")
        idx = 0
        # courses = self.request.get_all(args[0])
        # for course in courses:
        #     for c2 in course:
        #         course_numbers.append(course)
        for arg in args:
            course = self.request.get_all(arg)

            course.insert(0, arg)
            # course = str(course))
            course_numbers.append(course)
            # idx= idx+1
        current_user = User.all().filter('email =', user.email()).get()
        # for course in course_numbers:
        # course_numbers = args
        for coursevals in course_numbers:
            number = coursevals[0]
            quarteryear = coursevals[1]
            quarteryear = [x.strip() for x in quarteryear.split(',')]
            if len(quarteryear) == 2:
                quarter=quarteryear[0]
                year=int(quarteryear[1][-2:])
                course = Course.all().filter('number =',number).get()
                progress = Progress(user=current_user, course=course, quarter=quarter, year=year, completed=True)
                progress.put()

            # self.response.write("<br>")
        # print (str(course_numbers))
        return redirect('/dashboard')
    # self.response.write("yooo")
        # self.response.write(" <br> <br> course numbers: " + str(course_numbers));




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
