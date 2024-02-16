import user_interface

def add_course():
    course_code = input("Type in Course Code: ")
    print("Added Course:", course_code)

def delete_course():
    course_code = input("Type in Course Code: ")
    print("Deleted Course:", course_code)

def view_course(user_courses):
    for course in user_courses:
        print(course)
