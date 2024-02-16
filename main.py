# UCI Class Notifier

from user_interface import main_menu
import functionality


def commands(user_input):
    if user_input == "1":  # Add Course
        functionality.add_course()
    elif user_input == "2":  # Delete Course
        functionality.delete_course()
    elif user_input == "3":  # View Coures
        functionality.view_course()
    elif user_input == "Q":
        exit()
    else:
        print("Not a valid option. Please try again.")


def main():
    functionality.load_classes()

    user_input = ""
    while user_input != "Q":
        main_menu()
        user_input = input()
        print()
        commands(user_input)

if __name__ == "__main__":
    #61250, 44397
    main()
