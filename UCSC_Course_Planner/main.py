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

class ListCourses(webapp2.RequestHandler):
    def get(self):
        reader = csv.DictReader(open('resources/dump.csv'))
        departments = defaultdict(list)
        for course in reader:
            result = re.search(r'(?P<dept>[A-Z]+)(?P<number>[0-9]+\w*?)', course['name'])
            if result:
                departments[result.group('dept')] += course
        for dept in departments:
            departments[dept] = sorted(departments[dept], key=lambda element: element['number'])
        output = {
            'departments': departments,
        }
        path = os.path.join(os.path.dirname(__file__), 'templates/test.html')
        self.response.write(template.render(path, output))


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/courses', ListCourses),
                                  ('/login', Login),
], debug=True)
