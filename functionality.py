from bs4 import BeautifulSoup
import requests

user_courses = []  # User courses stored as objects


class Course:
    def __init__(self, teacher, course_name, course_code, class_enrolled, class_status, class_time):
        self.teacher = teacher
        self.name = course_name
        self.code = course_code
        self.enrolled = class_enrolled
        self.status = class_status
        self.time = class_time

def extract_data(course_code = "62150", course_term = "2024-03"):  # Extracts course data from ZotCourse and defaults term to 2024 Winter Quarter
    url = ("https://zotcourse.appspot.com/search?"
           f"YearTerm={course_term}"
           "&Breadth=ANY"
           "&Dept=%20ALL"
           f"&CourseCodes={course_code}"
           "&CourseNum="
           "&CourseTitle="
           "&InstrName="
           "&Division=ANY"
           "&ClassType=ALL"
           "&Units="
           "&Days="
           "&StartTime="
           "&EndTime="
           "&FullCourses=ANY")
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")
    data = str(soup)
    # Data is messy, need to clean it up
    clean_data = []
    for line in data.split("\","):
        if "amp;" in line:
            line = line.replace("amp;", "")
        if "m_enrll" in line:
            line = line.replace("m_enrll", "m_enroll")
        line = line.strip("{[]}").replace("\"", "")
        clean_data.append(line)
        #print(line)
    # After cleanup, declare variables
    teacher = ""
    course_code = ""
    dept = ""
    c_type = ""
    num = ""
    enrll = ""
    m_enrll = ""
    class_status = ""
    class_time = ""
    for clean_line in clean_data:
        if "name: " in clean_line:
            teacher = clean_line[clean_line.find("name: ") + len("name: "):]
        elif "code: " in clean_line:
            course_code = clean_line[clean_line.find("code: ") + len("code: "):]
        elif "dept: " in clean_line:
            dept = clean_line[clean_line.find("dept: ") + len("dept: "):]
        elif "c_type: " in clean_line:
            c_type = clean_line[clean_line.find("c_type: ") + len("c_type: "):]
        elif "{num: " in clean_line:
            num = clean_line[clean_line.find("{num: ") + len("{num: "):]
        elif "enrll: " in clean_line:
            enrll = clean_line[clean_line.find("enrll: ") + len("enrll: "):]
        elif "m_enroll: " in clean_line:
            m_enrll = clean_line[clean_line.find("m_enroll: ") + len("m_enroll: "):]
        elif "stat: " in clean_line:
            class_status = clean_line[clean_line.find("stat: ") + len("stat: "):]
        elif "f_time: " in clean_line:
            class_time = clean_line[clean_line.find("f_time: ") + len("f_time: "):]
    course_name = f"{c_type} {dept} {num}"
    class_enrolled = f"{enrll}/{m_enrll}"
    print (teacher, course_name, course_code, class_enrolled, class_status, class_time)


def add_course():
    course_code = input("Type in Course Code: ")
    print("Added Course:", course_code)


def delete_course():
    course_code = input("Type in Course Code: ")
    print("Deleted Course:", course_code)


def view_course():
    if len(user_courses) != 0:
        for course in user_courses:
            print(course)
    else:
        print("You don't have any courses added right now.")

def load_classes():
    course_codes = []  # Course Codes stored as course numbers
    with open("course_codes.txt", "r") as file:
        for line in file.readlines():
            try:
                course_codes.append(int(line))
            except ValueError:
                continue
    print(course_codes)
    if len(course_codes) != 0:
        for code in course_codes:
            extract_data(code)
            #course = Course(extract_data(code)) TODO: FIX This 
            #user_courses.append(course)

            
load_classes()

"""
for course in user_courses:
    print("------------------------------")
    print(course.teacher)
    print(course.name)
    print(course.code)
    print(course.enrolled)
    print(course.status)
    print(course.time)
    print("------------------------------")
"""

#extract_data("35580")