def main_menu():
    print("\nWelcome to UCI Class Notifier!\n")
    print("\t1 - Add Course")
    print("\t2 - Delete Course")
    print("\t3 - View Added Courses")
    print("\t4 - Enter checking mode")
    print("\tQ - Quit Program\n")
    print("Please type the desired option: ", end="")

def ui_course_view(user_courses):
    for course in user_courses:
        print("------------------------------")
        print(course.teacher)
        print(course.name)
        print(course.code)
        print(course.enrolled)
        print(course.status)
        print(course.time)
        print("------------------------------")

def ui_add_course(teacher, course_name, course_code, course_enrolled, course_status, course_time):
    print("------------------------------")
    print(teacher)
    print(course_name)
    print(course_code)
    print(course_enrolled)
    print(course_status)
    print(course_time)
    print("------------------------------")

def ui_checking_mode():
    print("You are now in checking mode. Exit / kill the terminal if you wish to stop the program.")
    print("You will be notified BELOW if a class becomes open.")
