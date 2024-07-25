# lib/cli.py
from models.trip import Trip
from models.activity import Activity

from helpers import (
    exit_program,
    list_trips,
    update_trip,
    delete_trip,
    list_activities,
    update_activity,
    delete_activity

)

def main():
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
            print("Invalid choice")


def menu():
        print("----------------------------------")
        print("Welcome to your Travel Database!")
        print("==================================")
        print(f"you currently have {len(Trip.get_all())} trips and {len(Activity.get_all())} activities logged.")
        print("==================================")
        print("Please select an option:")
        print("1. Trips")
        print("2. Activities")
        print("or type (e)xit at any time to exit")


def trip_menu():
    while True:
        print('Select from the following trip options:')
        print('1. List all trips')
        print('2. Find a trip by name')
        print('3. Find trips by location')
        print('4. Create a trip')
        print('5. Update a previously created trip.')
        print('6. Delete a trip')
        print('7. Return to the previous menu')
        print('or type (e)xit at any time to exit the program')

        choice = input(">")
        if choice == "1":
            list_trips()
        elif choice == "7":
            break
        elif choice.lower() == "e" or choice.lower() == "exit":
            exit_program()



def activity_menu():
    while True:
        print('Select from the following activity options: ')
        print("1. List all activities")
        print("2. Return to previous menu")
        print('or type (e)xit at any time to exit the program')

        choice = input('>')
        if choice.lower() == "e" or choice.lower() == "exit":
            exit_program()
        elif choice == "1":
            list_activities()
        elif choice == "2":
            break



if __name__ == "__main__":
    main()
