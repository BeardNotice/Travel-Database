# lib/helpers.py

from models.trip import Trip
from models.activity import Activity
from colorama import Fore, init as init_colorama

init_colorama(autoreset=True)

def manage_trips():
    trips = Trip.get_all()
    activity_submenu = [
        ("Learn more about an Activity", list_trip_activities),
        ("Add an activity", create_activity),
        ("Update an existing activity", update_activity),
        ("Delete an activity", delete_activity)
    ]
    
    if not trips:
        print("No Trips Available.")
        new_trip = input("Create a trip? (Y/N): ").strip().lower()
        if new_trip == "y":
            create_trip()
        return  # Exit if no trips exist after trying to create one

    while True:
        print("\nTrips:\n")
        for i, trip in enumerate(trips):
            print(f'{Fore.CYAN}{i + 1}. {Fore.MAGENTA}"{trip.name}"{Fore.CYAN} in {trip.location}: {trip.start_date} - {trip.end_date}')
        print(f"{Fore.CYAN}{len(trips) + 1}. {Fore.LIGHTGREEN_EX}Create{Fore.CYAN} a new trip.", end = "    ")
        print(f"{Fore.CYAN}{len(trips) + 2}. {Fore.BLUE}Update{Fore.CYAN} a trip.", end = "    ")
        print(f"{Fore.CYAN}{len(trips) + 3}. {Fore.RED}Delete{Fore.CYAN} a trip.")
        print(f"{Fore.CYAN}{len(trips) + 4}. Return to menu.")
        print("")
        print("Select a trip to manage its activities.")
        print(f"You can also {Fore.LIGHTGREEN_EX}create{Fore.RESET}, {Fore.BLUE}update{Fore.RESET}, or {Fore.RED}delete{Fore.RESET} trip(s).")
        choice = input(f"Or type {Fore.GREEN}(e)xit{Fore.RESET} at any time to quit: ").strip().lower()
        if choice in ["e", "exit"]:
            exit_program()
        elif choice == str(len(trips) + 1):
            create_trip()
            trips = Trip.get_all()
            continue
        elif choice == str(len(trips) + 2):
            update_trip()
            trips = Trip.get_all()
            continue
        elif choice == str(len(trips) + 3):
            delete_trip()
            trips = Trip.get_all()
            continue
        elif choice == str(len(trips) + 4):
            break
        else:
            try:
                choice = int(choice)
                if 1 <= choice <= len(trips):
                    selected_trip = trips[choice - 1]
                    manage_trip_activities(selected_trip, activity_submenu)
                else:
                    print("Invalid choice. Please select a valid option.")
            except ValueError:
                print("Invalid input, please enter a number.")

def manage_trip_activities(trip, activity_submenu):
    while True:
        activities = Activity.find_by_trip_id(trip.id)
        print(f"\nManaging activities for {Fore.BLUE}'{trip.name}'{Fore.RESET} in {trip.location}: {trip.start_date} - {trip.end_date}")
        print()
        print("Logged Activities:")
        print()
        if activities == []:
            print(f"{Fore.RED}No logged activities.")
        for i, activity in enumerate(activities):
            print(f'{Fore.YELLOW}  "{activity.name}"', end='    ')
            if (i+1)%4 == 0:
                print()
        if len(activities)%4 != 0:
            print()
        print()
        for i, (desc, _) in enumerate(activity_submenu, 1):
            print(f"{Fore.CYAN}{i}. {desc}")
        print(f"{Fore.CYAN}{len(activity_submenu) + 1}. Return to previous menu")
        print()

        activity_choice = input(f"Select from the following options or type {Fore.GREEN}(e)xit{Fore.RESET} to quit: ").strip().lower()
        if activity_choice in ["e", "exit"]:
            exit_program()
        elif activity_choice == str(len(activity_submenu) + 1):
            break
        else:
            try:
                activity_choice = int(activity_choice)
                if 1 <= activity_choice <= len(activity_submenu):
                    action = activity_submenu[activity_choice - 1][1]
                    if action:
                        action(trip.id)
                else:
                    print("Invalid choice. Please select a valid option.")
            except ValueError:
                print("Invalid input, please enter a number.")


def get_trip_by_name():
    name = input("Enter Trip's name: ")
    trip = Trip.find_by_name(name)
    print(f'\n-"{trip.name}" in {trip.location}:\n     {trip.start_date} - {trip.end_date}\n') if trip else print(f'{trip} was not found.')

def create_trip():
    
    name = input("Enter a name for the trip: ")
    location = input("Add a location for the trip: ")
    start_date = input("Add the start date: ")
    end_date = input("Add the end date: ")
    try:
        Trip.create(name, location, start_date, end_date)
        print(f'{Fore.GREEN}Sucessfully created {name}')
    except ValueError as exc:
        print(f"{Fore.RED}Error: ", exc)

def update_trip():
    while True:
        trips = Trip.get_all()
        print()
        for i, trip in enumerate(trips):
            print (f"{Fore.CYAN}{i+1}. {trip.name}", end = '    ')
            if (i+1)%4 == 0:
                print()
        if len(trips)%4 !=0:
            print()
        print()
        name_ = input(f"Enter the name of the trip to update or {Fore.BLUE}(re)eturn{Fore.RESET} to go back: ")
        if name_ in ("e", "exit"):
            exit_program()
        if name_ in ("re", "return"):
            break
        if trip := Trip.find_by_name(name_):
            try:
                new_name = input(f"Add a new name for {name_} or press Enter to skip: ")
                if new_name:
                    trip.name=new_name
                new_location = input('Add a new location or press Enter to skip: ')
                if new_location:
                    trip.location = new_location
                new_start_date = input("Add a new start date or press Enter to skip: ")
                if new_start_date:
                    trip.start_date = new_start_date
                new_end_date = input("Add new end date or press Enter to skip: ")
                if new_end_date:
                    trip.end_date = new_end_date

                trip.update()
                print(f'Trip "{trip.name}" updated sucessfully.')
                break
            except ValueError as exc:
                print(f'Error updating: {exc}\n')
                break
        else:
            print(f'{name_} was not found.\n')
            continue

def delete_trip():
    while True:
        trips = Trip.get_all()
        print()
        for i, trip in enumerate(trips):
            print (f"{i+1}. {trip.name}", end = '  ')
            if (i+1)%2 == 0:
                print()
        if len(trips)%2 !=0:
            print()
        print()
        name = input(f"Enter the name of the trip to be deleted or {Fore.BLUE}(re)eturn{Fore.RESET} to go back: ")
        if name in ("e", "exit"):
            exit_program()
        if name in ("re", "return"):
            break
        trip = Trip.find_by_name(name)
        if trip:
            confirmation = input(f'Are you sure you want to delete "{name}"? (Y/N):').strip().lower()
            if confirmation == "y":
                try:
                    trip.delete()
                    print(f'\n{Fore.GREEN}Sucessfully deleted {name}.\n')
                    break
                except ValueError as exc:
                    print(f'\n{Fore.RED}Error deleting {name}: {exc}\n')
            else:
                print("Cancelled Deletion.")
        else:
            print(f'\n{Fore.RED}{name} was not found.\n')

def list_activities():
    activities = Activity.get_all()
    print("==========================\n")
    for activity in activities:
        print(f'-"{activity.name}" ({activity.category}):\n     Cost: {activity.cost} {activity.currency}\n     Description: {activity.description}\n')
    print("==========================")

def find_activity_by_name():
    name = input("Enter the activity by the activity's name: ")
    activity = Activity.find_by_name(name)
    if activity:
        print(f'-"{activity.name}" ({activity.category}):\n     Cost: {activity.cost} {activity.currency}\n     Description: {activity.description}\n')
    else:
        print(f'{name} was not found.')

def find_activity_by_category():
    category = input("Enter the activity's category: ")
    activities = Activity.find_by_category(category)
    if activities:
        for activity in activities:
            print(f'-"{activity.name}" ({activity.category}):\n     Cost: {activity.cost} {activity.currency}\n     Description: {activity.description}\n')
    else:
        print(f'No activities found in category {category}')

def find_activity_by_currency():
    currency = input("Enter the activity's currency: ")
    activities = Activity.find_by_currency(currency)
    if activities:
        for activity in activities:
            print(f'-"{activity.name}" ({activity.category}):\n     Cost: {activity.cost} {activity.currency}\n     Description: {activity.description}\n')
    else:
        print(f'No activities found with currency {currency}\n')

def create_activity(trip_id=None):
    while True:
        if trip_id is None:
            trips = Trip.get_all()
            if trips:
                print("Existing trips:")
                for idx, trip in enumerate(trips):
                    print(f'{idx + 1}. {trip.name} in {trip.location}')
                choice = input("Select a trip by number or type 'new' to create a new trip: ").strip().lower()
                if choice == 'new':
                    trip = create_trip()
                    trip_id = trip.id
                else:
                    try:
                        choice = int(choice)
                        if 1 <= choice <= len(trips):
                            trip = trips[choice - 1]
                            trip_id = trip.id
                        else:
                            print("Invalid choice. Please select a valid trip number.\n")
                            continue
                    except ValueError:
                        print("Invalid input. Please enter a number.\n")
                        continue
            else:
                print("No existing trips found. You need to create a new trip.\n")
                trip = create_trip()
                trip_id = trip.id
        else:
            trip = Trip.find_by_id(trip_id)
            if not trip:
                print("Invalid trip ID. No such trip exists.")
                break


        name = input("Enter a name for the activity: ")
        try:
            cost = float(input("Enter a cost for the activity: "))
        except ValueError:
            print("Invalid input. Please enter a valid number for the cost.\n")
            continue
        
        currency = input("Enter a currency for the activity: ")

        categories = ["Relaxation", "Photography", "Entertainment", "Cultural", "Culinary", "Adventure", "Sports"]
        while True:
            for idx, category in enumerate(categories):
                print(f'{idx + 1}. {category}')
            category_choice = input("Enter the number corresponding to the category: ").strip()
            try:
                category_choice = int(category_choice)
                if 1 <= category_choice <= len(categories):
                    category = categories[category_choice - 1]
                    break
                else:
                    print("Invalid choice. Please select a valid category number.\n")
            except ValueError:
                print("Invalid input. Please enter a number.\n")

        description = input("Enter a description for the activity: ")

        try:
            Activity.create(name, cost, currency.upper(), category, description, trip_id)
            print(f'Successfully created {name} for trip {trip.name} in {trip.location}.\n')
            break
        except ValueError as exc:
            print("Error: ", exc)
            continue
    

def update_activity(trip_id=None):
    while True:
        if trip_id:
            trip = Trip.find_by_id(trip_id)
        name_ = input(f"Enter the name of the activity to update or {Fore.BLUE}(re)eturn{Fore.RESET} to go back: ")
        if name_ in ("e", "exit"):
            exit_program()
        if name_ in ("re", "return"):
            break
        if activity:= Activity.find_by_name(name_):
            try:
                new_name = input(f"Enter a new name for '{name_}' or press Enter to keep '{activity.name}': ")
                if new_name:
                    activity.name = new_name
                new_cost = input(f"Enter a new cost or press Enter to keep '{activity.cost}': ")
                if new_cost:
                    activity.cost = new_cost
                new_currency = input(f"Enter a new currency or press Enter to keep '{activity.currency}': ")
                if new_currency:
                    activity.currency = new_currency
                categories = ["Relaxation", "Photography", "Entertainment", "Cultural", "Culinary", "Adventure", "Sports"]
                for idx, category in enumerate(categories):
                    print(f"{idx + 1}. {category}")
                print(f"Current category: {activity.category}")
                category_choice = input("Choose a new category or press Enter to keep the current category: ")
                if category_choice:
                    try:
                        category_choice = int(category_choice)
                        if 1<= category_choice <= len(categories):
                            activity.category = categories[category_choice - 1]
                        else:
                            print("Invalid choice. Keeping the current category.")
                    except ValueError:
                        print("Invalid input. Keeping the current category.")
                new_description = input(f"Add a new description or press Enter to keep the current description:\n'{activity.description}'\n> ")
                if new_description:
                    activity.description = new_description
                activity.update()
                print(f"Sucessfully updated {activity.name}")
                break
            except ValueError as exc:
                print("Error: ", exc)
        else:
            print(f"{name_} was not found.")

def delete_activity(trip_id=None):
    while True:
        if trip_id:
            trip = Trip.find_by_id(trip_id)
            id_confirm = input(f"Are you sure you want to delete '{trip.name}'? (Y/N)").strip().lower()
            if id_confirm in ("e", "exit"):
                exit_program()
            if id_confirm == "y":
                trip.delete()
                break
        name = input(f"TYPE the name of the activity to be deleted or {Fore.BLUE}(re)eturn{Fore.RESET} to go back: ")
        if name in ("e", "exit"):
            exit_program()
        if name in ("re", "return"):
            break
        activity = Activity.find_by_name(name)
        if activity:
            confirm = input(f"Are you sure you want to Delete '{name}? (Y/N)").strip().lower()
            if confirm in ("e", "exit"):
                exit_program()
            if confirm == "y":
                try:
                    activity.delete()
                    print(f'Succesfully deleted {name}.')
                    break
                except ValueError as exc:
                    print(f'Error deleting {name}: {exc}')
            else:
                print("Deletion cancelled.")
                break
        else:
            print(f'{name} was not found.')

def list_trip_activities(trip_id=None):
    while True:
        # Prompt for trip name if no trip ID is provided
        if not trip_id:
            trip_name = input("Enter the trip name to list its activities: ")
            trip = Trip.find_by_name(trip_name)
        else:
            trip = Trip.find_by_id(trip_id)


        if trip:
            activities = trip.activities()
        else:
            print("No trip found.")
            break


        if activities:
            print(f"Select one of the following activities or type {Fore.BLUE}(re)turn{Fore.RESET} to go back:")
            print()
            for i, activity in enumerate(activities):
                print(f'{Fore.YELLOW}{i + 1}. {activity.name}', end="    ")
                if (i + 1) % 4 == 0:
                    print()

            if len(activities) % 4 != 0:
                print()

            try:
                choice = input("> ")
                if choice in ("re", "return"):
                    break
                if choice in ("e", "exit"):
                    exit_program()
                choice = int(choice)-1
                if 0 <= choice < len(activities):
                    activity_info = activities[choice]
                    print(f'\n-- {Fore.YELLOW}"{activity_info.name}"{Fore.RESET} ({activity_info.category})')
                    print(f'-- Cost: {Fore.GREEN}{activity_info.cost} {activity_info.currency}')
                    print(f'-- {Fore.LIGHTMAGENTA_EX}{activity_info.description}\n')
                    
                else:
                    print("Invalid choice. Please select a valid number.")
            except ValueError:
                print(f"{Fore.RED}Invalid input. Please enter a number.")

        else:
            print("No activities found for the selected criteria.")
            break

def quick_overview():
    trips = Trip.get_all()
    if not trips:
        print(create_boxed_text("No trips found."))
        return
    output = []
    for trip in trips:
        output.append(f'-{trip.name} in {trip.location}\n')
        activities = Activity.find_by_trip_id(trip.id)
        output.append("  Activities:")
        if activities:
            for activity in activities:
                output.append(f'     -{activity.name} ({activity.category})')
        else:
            output.append("     -No activities found.")
        output.append("")
        output.append("-" * 40)
    boxed_output = create_boxed_text('\n'.join(output))
    print(boxed_output)

# Adds a box around output
def create_boxed_text(content):
    lines = content.split('\n')
    max_length = max(len(line) for line in lines)
    border_line = '+'+'-'*(max_length+2)+'+'

    boxed_text = [border_line]
    for line in lines:
        boxed_text.append(f'| {line.ljust(max_length)} |')
    boxed_text.append(border_line)

    return '\n'.join(boxed_text)



def exit_program():
    print(f"{Fore.GREEN}Goodbye!")
    exit()
