import re

class Course(object):
    def __init__(self, name=None, number=None, department=None, description=None, prerequisites=None, offered=None):
        self.name = name #course name
        self.number = number #course number
        self.department = department #department within SOE
        self.description = description #course description
        self.prerequisites = prerequisites #classes that are prerequisites for this
        self.offered = offered #quarters course is typically offered

    def __repr__(self):
        return '{} - {}'.format(self.number, self.name)

def extract(filename):
    regex = re.compile(r'<a href="/courses/(?P<course_number>\w+\d+\w*?)">(?P<course_name>[a-zA-Z0-9 :&#;,+()-/\']+)</a>')
    courses = dict()
    with open(filename) as course_schedule:
        for line in course_schedule.readlines():
            result = regex.search(line)
            if result:
                course_name = result.group('course_name')
                course_number = result.group('course_number')
                new_course = Course(name=course_name, number=course_number)
                courses[course_number] = new_course
    for course_number, course in courses.iteritems():
        print course

if __name__ == '__main__':
    extract(filename='soe_course_links.htm')
