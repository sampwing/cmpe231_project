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
import os
import re
from collections import defaultdict

import webapp2
from google.appengine.ext.webapp import template

class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Hello World')

class Login(webapp2.RequestHandler):
    def get(self):
        path = os.path.join(os.path.dirname(__file__), 'templates/login.html')
        self.response.write(template.render(path, {}))

class Dashboard(webapp2.RequestHandler):
    def get(self):
        path = os.path.join(os.path.dirname(__file__), 'templates/dashboard.html')
        self.response.write(template.render(path, {}))

class Homepage(webapp2.RequestHandler):
    def get(self):
        path = os.path.join(os.path.dirname(__file__), 'templates/home.html')
        self.response.write(template.render(path, {}))

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



app = webapp2.WSGIApplication([
    ('/', Homepage),
    ('/dashboard', Dashboard),
    ('/courses', ListCourses),
    ('/login', Login),
], debug=True)
