__author__ = 'samwing'
from google.appengine.ext import db

from main import User

#Course information

class Course(db.Model):
    department = db.StringProperty(required=True)
    name = db.StringProperty(required=True)
    number = db.StringProperty(required=True)
    description = db.StringProperty(multiline=True, required=True)

    def __repr__(self):
        return '{} {} {}'.format(self.department, self.name, self.number)

class Offerings(db.Model):
    offered = db.StringProperty(required=True) #Fall/Winter/Spring/Summer
    course = db.ReferenceProperty(Course, required=True)

    def __repr__(self):
        return '{} {}'.format(self.course, self.offered)

class Prerequisites(db.Model):
    course = db.ReferenceProperty(Course, required=True, collection_name='prerequisites_course')
    prereq = db.ReferenceProperty(Course, required=True, collection_name='prerequisites_prereq')

class MajorRequirements(db.Model):
    major = db.StringProperty(required=True)
    course = db.ReferenceProperty(Course, required=True)

#User Information
class Progress(db.Model):
    user = db.ReferenceProperty(User, required=True)
    #major = db.StringProperty(required=True) #cmps/ee/cmpe
    course = db.ReferenceProperty(Course, required=True)
    year = int()
    quarter = db.StringProperty()
    completed = bool()