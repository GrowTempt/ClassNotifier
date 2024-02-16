def main_menu():
    print("\nWelcome to UCI Class Notifier!\n")
    print("\t1 - Add Course")
    print("\t2 - Delete Course")
    print("\t3 - View Added Courses")
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