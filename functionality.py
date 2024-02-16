from bs4 import BeautifulSoup
import requests
import json

class Course:
    def __init__(self, teacher, course_name, course_code, class_enrolled, class_status, class_time):
        self.teacher = teacher
        self.name = course_name
        self.code = course_code
        self.enrolled = class_enrolled
        self.status = class_status
        self.time = class_time

def extract_data(course_term = "2024-03", course_code = "62150"):  #Extracts course data from ZotCourse
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
    data_dict = json.loads(data)
# Extract Course Information from Json
    # Declare Dictionaries
    courses_dict = data_dict['data'][0]['courses'][0]
    sections_dict = courses_dict["sections"][0]
    meeting_dict = sections_dict["mtng"][0]
    # Declare Variables
    teacher = courses_dict["sections"][0]["instr"][0]["name"]
    course_name = f"{data_dict['data'][0]['dept']} {courses_dict['num']}"
    course_code = sections_dict["code"]
    class_enrolled = f"{sections_dict['enrll']}/{sections_dict['m_enrll']}"
    class_status = sections_dict["stat"]
    class_time = meeting_dict["f_time"]
    print(teacher, course_name, course_code, class_enrolled, class_status, class_time)


def add_course():
    course_code = input("Type in Course Code: ")
    print("Added Course:", course_code)


def delete_course():
    course_code = input("Type in Course Code: ")
    print("Deleted Course:", course_code)


def view_course(user_courses):
    for course in user_courses:
        print(course)

extract_data()