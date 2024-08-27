# lib/cli.py
from models.trip import Trip
from models.activity import Activity
from colorama import Fore, Style, init as init_colorama

from helpers import (
    exit_program,
    list_trips,
    get_trips_by_name,
    create_trip,
    update_trip,
    delete_trip,
    list_activities,
    find_activity_by_name,
    find_activity_by_category,
    find_activity_by_currency,
    create_activity,
    update_activity,
    delete_activity,
    list_trip_activities,
    quick_overview
    )
init_colorama(autoreset=True)


def display_menu(options, prompt="Select from the following options:", is_main_menu=False):
    while True:
        print(prompt)
        for i, (desc, action) in enumerate(options, 1):
            print(f'{Fore.CYAN}{i}. {desc}')
        print(f'or type {Fore.GREEN}(e)xit{Fore.RESET} at any time to quit.')
        choice = input("> ").strip().lower()
        if choice in ["exit", "e"]:
            exit_program()
        try:
            choice = int(choice)
            if 1<=choice<=len(options):
                if not is_main_menu and choice == len(options):
                    break
                action = options[choice -1][1]
                if action:
                    action()
            else:
                print(f'{Fore.RED} Invalid Choice, please select a valid option.')
        except ValueError:
            print(f'{Fore.RED} Invalid Input, please enter a number.')



def main():
    trip_count = len(Trip.get_all())
    activity_count = len(Activity.get_all())

    options = [
        ("Trips", trip_menu), 
        ("Activities", activity_menu),
        ("Quick overview", quick_overview)]

    print("----------------------------------")
    print(f"Welcome to {Style.BRIGHT}your{Style.RESET_ALL} Travel Database!")
    print("==================================")
    print(f"you currently have {Fore.YELLOW}{trip_count}{Fore.RESET} trips and {Fore.YELLOW}{activity_count}{Fore.RESET} activities logged.")
    print("==================================")
    display_menu(options, is_main_menu = True)

'''
    while True:
        menu()
        choice = input("> ")
        if choice == "0" or choice.lower() == 'exit' or choice.lower() == "e":
            exit_program()
        elif choice == "1":
            trip_menu()
        elif choice == "2":
            activity_menu()
        else:
            print(Fore.RED + "Invalid choice")
'''

'''
def menu():
        print("----------------------------------")
        print(f"Welcome to {Style.BRIGHT}your{Style.RESET_ALL} Travel Database!")
        print("==================================")
        print(f"you currently have {Fore.YELLOW}{len(Trip.get_all())}{Fore.RESET} trips and {Fore.YELLOW}{len(Activity.get_all())}{Fore.RESET} activities logged.")
        print("==================================")
        print("Please select an option:")
        print(Fore.CYAN + "1. Trips")
        print(Fore.CYAN + "2. Activities")
        print(f"or type {Fore.GREEN}(e)xit{Fore.RESET} at any time to exit")
'''


def trip_menu():
    options = [
        ("List all trips", list_trips),
        ("Create a trip", create_trip),
        ("Update a previously created trip", update_trip),
        ("Delete a trip", delete_trip),
        ("Find a trip by name", get_trips_by_name),
        ("Return to the previous menu", None)]
    display_menu(options, "Select from the following trip options:")

""" 
    while True:
        print('Select from the following trip options:')
        for i, (desc, _) in enumerate(options, 1):
            print(f'{Fore.CYAN}{i}. {desc}')
        print(f'or type {Fore.GREEN}(e)xit{Fore.RESET} at any time to exit')

        choice = input("> ").lower()
        if choice in ["e", "exit"]:
            exit_program()
        try:
            choice = int(choice)
            if 1<=choice<=len(options):
                if choice == len(options):
                    break
                action = options[choice -1][1]
                if action:
                    action()
            else:
                print(Fore.RED + "Invalid choice, please select a valid option")
        except ValueError:
            print(Fore.RED + "Invalid input, please enter a number")
            """



def activity_menu():
    options = [
        ("List all activities", list_activities),
        ("List activities by trip", list_trip_activities),
        ("Create an activity", create_activity),
        ("Update an existing activity", update_activity),
        ("Delete an activity", delete_activity),
        ("Find an activity by name", find_activity_by_name),
        ("Find an activity by category", find_activity_by_category),
        ("Return to previous menu", None)]
    display_menu(options, "Select from the following activity options:")
'''    
    while True:
        print('Select from the following activity options: ')
        for i, (desc, _) in enumerate(options, 1):
            print(f'{Fore.CYAN}{i}. {desc}')
        print(f'or type {Fore.GREEN}(e)xit{Fore.RESET} at any time to exit')

        choice = input("> ").lower()
        if choice in ["e", "exit"]:
            exit_program()
        try:
            choice = int(choice)
            if 1<=choice<=len(options):
                if choice == len(options):
                    break
                action = options[choice - 1][1]
                if action:
                    action()
            else:
                print(Fore.RED + "Invalid choice. Please select a valid option\n")
        except ValueError:
            print(Fore.RED + "Invalid input. Please enter a number.\n")
'''


if __name__ == "__main__":
    main()
