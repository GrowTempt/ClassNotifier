# UCI Class Notifier

from user_interface import main_menu
import functionality

waiting_mode = False

def commands(user_input):
    global waiting_mode
    if user_input == "1":  # Add Course
        functionality.add_course()
    elif user_input == "2":  # Delete Course
        functionality.delete_course()
    elif user_input == "3":  # View Coures
        functionality.view_course()
    elif user_input == "4":  # Waiting Mode, mode that sends updates if there's a change
        waiting_mode = True
        functionality.waiting_mode()
    elif user_input == "Q":
        exit()
    else:
        print("Not a valid option. Please try again.")


def main():
    global waiting_mode
    waiting_mode = False

    user_input = ""
    while user_input != "Q" and waiting_mode is False:
        main_menu()
        user_input = input()
        print()
        commands(user_input)

if __name__ == "__main__":
    functionality.load_classes()
    main()
