from bs4 import BeautifulSoup
import json
import requests
from user_interface import ui_course_view, ui_add_course, ui_checking_mode
from main import main
import time

user_courses = []  # User courses stored as objects
timer = 600 # Time before it checks classes again in seconds
file_name = "course_codes.txt"

class Course:
    def __init__(self, teacher, course_name, course_code, course_enrolled, course_status, course_time):
        self.teacher = teacher
        self.name = course_name
        self.code = course_code
        self.enrolled = course_enrolled
        self.status = course_status
        self.time = course_time

def extract_data(course_code: str, course_term = "2024-14"): # Extracts course data from ZotCourse and defaults term to 2024 Spring Quarter
    try:
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
        data_json = json.loads(data)
        course = data_json["data"][0]["courses"][0]
        sections = course["sections"][0]
        teacher = sections["instr"][0]["name"]
        c_type = sections["c_type"]
        s_num = sections["s_num"]
        dept = data_json["data"][0]["dept"]
        dept = dept.replace("amp;", "")
        num = course["num"]
        course_name = f"{c_type} {s_num} {dept} {num}"
        enrll = sections["enrll"]
        m_enrll = sections["m_enrll"]
        course_enrolled = f"{enrll} / {m_enrll}"
        course_status = sections["stat"]
        course_time = sections["mtng"][0]["f_time"]
        # print(json.dumps(data_json, indent=4), type(data_json))
        course_data = [teacher, course_name, course_code, course_enrolled, course_status, course_time]
        return course_data
    except IndexError:
        print(f"Invalid Course Code: {course_code}. Please Try Again.")
        return False # Invalid course code


def valid_course_code_checker(code):
    course_data = extract_data(code)
    if course_data is False:
        return False # Invalid Course Code
    else:
        return True # Valid Course Code


def detect_duplicate_code(code):
    for course in user_courses:
        if course.code == code:
            return True  # Detected a duplicate
    return False


def add_course():
    course_code_input = input("Add Course Code: ")
    if len(course_code_input) == 5 and valid_course_code_checker(course_code_input) is True and detect_duplicate_code(course_code_input) is False:
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
        if detect_duplicate_code(course_code_input) is True:
            print("Already have the course added!")
        else:
            print("Failed to add course.")
        main()


def delete_course():
    course_list = view_course()
    if course_list is True: # Checks to see if the user first has any courses
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
        return True
    else:
        print("You don't have any courses added right now.")


def checking_mode():
    course_list = view_course()
    if course_list is True: # Checks to see if the user first has any courses
        ui_checking_mode()
        count_check = 0
        while True:
            count_check += 1
            print(f"Checked {count_check}x times for class openings")
            for course in user_courses:
                if course.status == "OPEN":
                    print(f"!!!\t{course.name} IS OPEN ({course.enrolled})\t!!! ")
            time.sleep(timer)  # Checks classes at timer
    else:
        main()


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
            try:
                course_data = extract_data(code)
                teacher = course_data[0]
                course_name = course_data[1]
                course_code = course_data[2]
                course_enrolled = course_data[3]
                course_status = course_data[4]
                course_time = course_data[5]
                course = Course(teacher, course_name, course_code, course_enrolled, course_status, course_time) 
                user_courses.append(course)
            except TypeError:
                print(f"Invalid Course Code detected: {code}. Please Remove from the txt file.")
                continue
    print("Successfully loaded!")
