# UCI Class Notifier
import user_interface

user_courses = []

def main():
    user_input = input()
    while user_input != "Q":
        user_interface.main_menu()
        user_input = input()

if __name__ == "__main__":
    main()