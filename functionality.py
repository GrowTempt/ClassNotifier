from bs4 import BeautifulSoup
import requests
from user_interface import ui_course_view, ui_add_course, ui_waiting_mode
from main import main
import time

user_courses = []  # User courses stored as objects
file_name = "course_codes.txt"

class Course:
    def __init__(self, teacher, course_name, course_code, course_enrolled, course_status, course_time):
        self.teacher = teacher
        self.name = course_name
        self.code = course_code
        self.enrolled = course_enrolled
        self.status = course_status
        self.time = course_time

def extract_data(course_code: str, course_term = "2024-03"): # Extracts course data from ZotCourse and defaults term to 2024 Winter Quarter
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
    course_status = ""
    course_time = ""
    for clean_line in clean_data:
        if "[{name: " in clean_line:
            teacher = clean_line[clean_line.find("[{name: ") + len("[{name: "):]
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
            course_status = clean_line[clean_line.find("stat: ") + len("stat: "):]
        elif "f_time: " in clean_line:
            course_time = clean_line[clean_line.find("f_time: ") + len("f_time: "):]
    course_name = f"{c_type} {dept} {num}"
    course_enrolled = f"{enrll} / {m_enrll}"
    course_data = [teacher, course_name, course_code, course_enrolled, course_status, course_time, data] #data at end used for validity code checker
    return course_data

def valid_course_code_checker(code):
    course_data = extract_data(code)
    raw_data = course_data[6]
    if raw_data == '{"data": []}':
        print("Invalid")
        return False  # Invalid Code
    else:
        print("Valid")
        return True  # Valid Code
    

def add_course():
    course_code_input = input("Add Course Code: ")
    if len(course_code_input) == 5 and valid_course_code_checker(course_code_input) is True:
        with open(file_name, "a") as file:
            file.write(f"{course_code_input}\n")
        course_data = extract_data(course_code_input)
        teacher = course_data[0]
        course_name = course_data[1]
        course_code = course_data[2]
        course_enrolled = course_data[3]
        course_status = course_data[4]
        course_time = course_data[5]
        course = Course(teacher, course_name, course_code, course_enrolled, course_status, course_time) 
        user_courses.append(course)
        ui_add_course(teacher, course_name, course_code, course_enrolled, course_status, course_time)
        print("Added Course:", course_code_input)
    else:
        print("Failed to add course.")
        main()


def delete_course():
    course_code_input = input("Delete Course Code: ")
    if len(course_code_input) == 5:
        delete = False
        for course in user_courses:
            if course.code == course_code_input:
                user_courses.remove(course)
                delete = True
        if delete is True:
            with open(file_name, "r") as file:
                lines = file.readlines()
            with open(file_name, "w") as file:
                for line in lines:
                    if line.strip("\n") != course_code_input:
                        file.write(line)
            print("Deleted Course:", course_code_input)
        else:
            print("Failed to delete course.")
            main()
    else:
        print("Failed to delete course.")
        main()


def view_course():
    if len(user_courses) != 0:
        ui_course_view(user_courses)
    else:
        print("You don't have any courses added right now.")


def waiting_mode():
    ui_waiting_mode()
    while True:
        for course in user_courses:
            if course.status == "OPEN":
                print(f"!!!\t{course.name} IS OPEN ({course.enrolled})\t!!! ")
        time.sleep(60)  # Checks user courses every minute


def load_classes():
    print("Loading Data . . .")
    course_codes = []  # Course Codes stored as course numbers
    with open(file_name, "r") as file:
        for line in file.readlines():
            try:
                course_codes.append(int(line))
            except ValueError:
                continue
    if len(course_codes) != 0:
        for code in course_codes:
            course_data = extract_data(code)
            teacher = course_data[0]
            course_name = course_data[1]
            course_code = course_data[2]
            course_enrolled = course_data[3]
            course_status = course_data[4]
            course_time = course_data[5]
            course = Course(teacher, course_name, course_code, course_enrolled, course_status, course_time) 
            user_courses.append(course)
    print("Successfully loaded!")
