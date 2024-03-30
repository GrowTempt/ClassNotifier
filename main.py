# UCI Class Notifier
# Programmed by Vincent Hoang

from user_interface import main_menu
import functionality

checking_mode = False

def commands(user_input):
    global checking_mode
    if user_input == "1":  # Add Course
        functionality.add_course()
    elif user_input == "2":  # Delete Course
        functionality.delete_course()
    elif user_input == "3":  # View Coures
        functionality.view_course()
    elif user_input == "4":  # Checking Mode, mode that sends updates if there's a change
        checking_mode = True
        functionality.checking_mode()
    elif user_input == "Q":
        exit()
    else:
        print("Not a valid option. Please try again.")


def main():
    global checking_mode
    checking_mode = False

    user_input = ""
    while user_input != "Q" and checking_mode is False:
        main_menu()
        user_input = input()
        print()
        commands(user_input)

if __name__ == "__main__":
    functionality.load_classes()
    main()
