# lib/helpers.py

from models.trip import Trip
from models.activity import Activity
from colorama import Fore, init as init_colorama

init_colorama(autoreset=True)

def manage_trips():
    trips = Trip.get_all()
    
    if not trips:
        print("No Trips Available.")
        new_trip = input("Create a trip? (Y/N): ").strip().lower()
        if new_trip == "y":
            create_trip() # Exit if no trips exist after trying to create one

    while True:
        trips = Trip.get_all()
        special_trips_updater = [
            (f"{Fore.LIGHTGREEN_EX}Create{Fore.CYAN} a new trip.", create_trip), 
            (f"{Fore.BLUE}Update{Fore.CYAN} a trip.", update_trip), 
            (f"{Fore.RED}Delete{Fore.CYAN} a trip.", delete_trip),
            (f"{Fore.CYAN}Return to menu.", None)
            ]
        print("\nTrips:\n")
        for i, trip in enumerate(trips):
            print(f'{Fore.CYAN}{i + 1}. {Fore.MAGENTA}"{trip.name}"{Fore.CYAN} in {trip.location}: {trip.start_date} - {trip.end_date}')
        for i, (extra, action) in enumerate(special_trips_updater):
            print(f"{Fore.CYAN}{i+len(trips)+1}. {extra}")
        print("")
        print("Select a trip to manage its activities.")
        print(f"You can also {Fore.LIGHTGREEN_EX}create{Fore.RESET}, {Fore.BLUE}update{Fore.RESET}, or {Fore.RED}delete{Fore.RESET} trip(s).")
        choice = input(f"Or type {Fore.GREEN}(e)xit{Fore.RESET} at any time to quit: ").strip().lower()
        if choice in ["e", "exit"]:
            exit_program()
        elif int(choice) == len(trips) + len(special_trips_updater):
            break
        else:
            try:
                choice = int(choice)
                if 1 <= choice <= len(trips):
                # If a trip is selected
                    selected_trip = trips[choice - 1]
                    manage_trip_activities(selected_trip.id)
                elif len(trips) < choice <= len(trips) + len(special_trips_updater) - 1:
                    action = special_trips_updater[choice - len(trips) - 1][1]
                    if action:
                            action()    # Call the function associated with the special option
                    trips = Trip.get_all()
                else:
                    print(f"{Fore.RED}Invalid choice. Please select a valid option.")
            except ValueError:
                print(f"{Fore.RED}Invalid input, please enter a number.")

def manage_trip_activities(trip_id=None):
    while True:
        trip=Trip.find_by_id(trip_id)
        if not trip:
            break
        activity_submenu = [
        (f"Learn more about an {Fore.YELLOW}Activity", list_trip_activities),
        (f"{Fore.GREEN}Add{Fore.CYAN} an activity", create_activity),
        (f"{Fore.BLUE}Update{Fore.CYAN} an existing activity", update_activity),
        (f"{Fore.RED}Delete{Fore.CYAN} an activity", delete_activity),
        (f"{Fore.BLUE}Update{Fore.CYAN} this {Fore.MAGENTA}trip{Fore.CYAN}'s information", update_trip),
        (f"{Fore.RED}Delete{Fore.CYAN} this {Fore.MAGENTA}trip", delete_trip)
        ]
        activities = Activity.find_by_trip_id(trip.id)
        print(f"\nManaging {Fore.BLUE}'{trip.name}'{Fore.RESET} in {trip.location}: {trip.start_date} - {trip.end_date}")
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
        spacer_added = False
        for i, (desc, _) in enumerate(activity_submenu, 1):
            print(f"{Fore.CYAN}{i}. {desc}")
            if "delete" in desc.lower() and not spacer_added:
                print(f"{Fore.CYAN}--------------------------------------")
                spacer_added=True
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

def update_trip(trip_id=None):
    while True:
        if trip_id:
            updated_trip = Trip.find_by_id(trip_id)
            try:
                new_name = input(f"Add a new {Fore.MAGENTA}name{Fore.RESET} for {Fore.MAGENTA}{updated_trip.name}{Fore.RESET} or press {Fore.LIGHTGREEN_EX}Enter{Fore.RESET} to skip: ")
                if new_name:
                    updated_trip.name=new_name
                new_location = input(f'Add a new {Fore.CYAN}location{Fore.RESET} or press {Fore.LIGHTGREEN_EX}Enter{Fore.RESET} to skip: ')
                if new_location:
                    updated_trip.location = new_location
                new_start_date = input(f"Add a new {Fore.GREEN}start date{Fore.RESET} or press {Fore.LIGHTGREEN_EX}Enter{Fore.RESET} to skip: ")
                if new_start_date:
                    updated_trip.start_date = new_start_date
                new_end_date = input(f"Add new {Fore.LIGHTRED_EX}end date{Fore.RESET} or press {Fore.LIGHTGREEN_EX}Enter{Fore.RESET} to skip: ")
                if new_end_date:
                    updated_trip.end_date = new_end_date
                updated_trip.update()
                print(f'{Fore.GREEN}Trip "{updated_trip.name}" updated sucessfully.')
                break
            except ValueError as exc:
                print(f'{Fore.RED}Error updating: {exc}\n')
                break
 
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
                new_name = input(f"Add a new {Fore.MAGENTA}name{Fore.RESET} for {Fore.MAGENTA}{name_}{Fore.RESET} or press {Fore.LIGHTGREEN_EX}Enter{Fore.RESET} to skip: ")
                if new_name:
                    trip.name=new_name
                new_location = input(f'Add a new {Fore.CYAN}location{Fore.RESET} or press {Fore.LIGHTGREEN_EX}Enter{Fore.RESET} to skip: ')
                if new_location:
                    trip.location = new_location
                new_start_date = input(f"Add a new {Fore.GREEN}start date{Fore.RESET} or press {Fore.LIGHTGREEN_EX}Enter{Fore.RESET} to skip: ")
                if new_start_date:
                    trip.start_date = new_start_date
                new_end_date = input(f"Add new {Fore.RED}end date{Fore.RESET} or press {Fore.LIGHTGREEN_EX}Enter{Fore.RESET} to skip: ")
                if new_end_date:
                    trip.end_date = new_end_date

                trip.update()
                print(f'{Fore.GREEN}Trip "{trip.name}" updated sucessfully.')
                break
            except ValueError as exc:
                print(f'{Fore.RED}Error updating: {exc}\n')
                break
        else:
            print(f'{Fore.RED}{name_} was not found.\n')
            continue

def delete_trip(trip_id = None):
    while True:
        if trip_id:
            trip_from_id = Trip.find_by_id(trip_id)
            confirm = input(f"Are you sure you want to delete {trip_from_id.name}? (Y/N)").strip().lower()
            if confirm in ("e", "exit"):
                exit_program()
            if confirm == "y":
                try:
                    activities = Activity.find_by_trip_id(trip_id)
                    for activity in activities:
                        activity.delete()
                    trip_from_id.delete()
                    print()
                    print(f"'{trip_from_id.name}' Sucessfully deleted.")
                    break
                except Exception as exc:
                    print(f"Error: {exc}")
                    break
            else:
                print()
                print("Deletion Cancelled.")
                break
        trips = Trip.get_all()
        print()
        for i, trip in enumerate(trips):
            print (f"{i+1}. {Fore.MAGENTA}{trip.name}")
        print()
        name = input(f"TYPE the name of the trip to be deleted or {Fore.BLUE}(re)eturn{Fore.RESET} to go back: ")
        if name in ("e", "exit"):
            exit_program()
        if name in ("re", "return"):
            break
        trip = Trip.find_by_name(name)
        if trip:
            confirmation = input(f'Are you sure you want to delete "{name}"? (Y/N):').strip().lower()
            if confirmation == "y":
                try:
                    removable_activities = Activity.find_by_trip_id(trip.id)
                    for activity in removable_activities:
                        activity.delete()
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
    all_activities = Activity.get_all()
    for i, activity in enumerate(all_activities):
        print(f'{Fore.CYAN}{i+1}. {activity.name}', end='   ')
        if (i+1) == 4:
            print()
    if len(all_activities) != 4:
        print()
    print()
    name = input("Enter the activity by the activity's name: ")
    activity = Activity.find_by_name(name)
    if activity:
        print(f'-"{activity.name}" ({activity.category}):\n     Cost: {activity.cost} {activity.currency}\n     Description: {activity.description}\n')
    else:
        print(f'{name} was not found.')

def find_activity_by_category():
    while True:
        for i, category in enumerate(activity_categories):
            print(f'{Fore.CYAN}{i+1}. {category}')
        category = input(f"Select a Category or {Fore.BLUE}(re)turn{Fore.RESET} to previous menu: ")
        if category in ("re", "return"):
            break
        category = int(category)
        if 1 <= category <= len(activity_categories):
            category = activity_categories[category -1]
        else:
            print(f"{Fore.RED}Please select a valad option.")
            continue
        activities = Activity.find_by_category(category)
        if activities:
            print()
            for activity in activities:
                print(f'{Fore.MAGENTA}-"{activity.name}" ({activity.category}):\n     Cost: {activity.cost} {activity.currency}\n     Description: {activity.description}\n')
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

        try:
            name = input(f"Enter a {Fore.MAGENTA}name{Fore.RESET} for the activity: ")
        except ValueError as exc:
            print(f'{Fore.RED}Error: {exc}')
            break
        try:
            cost = float(input(f"Enter a {Fore.GREEN}cost{Fore.RESET} for the activity: "))
        except ValueError:
            print(f"{Fore.RED}Invalid input. Please enter a valid number for the cost.\n")
            break
        try:
            currency = input(f"Enter a {Fore.GREEN}currency{Fore.RESET} for the activity: ")
        except ValueError as exc:
            print(f'{Fore.RED}Error: {exc}')
            break
        categories = activity_categories
        for idx, category in enumerate(categories):
            print(f'{idx + 1}. {category}')
        category_choice = input(f"Enter the number corresponding to the {Fore.BLUE}category for the activity: ").strip()
        try:
            category_choice = int(category_choice)
            if 1 <= category_choice <= len(categories):
                category = categories[category_choice - 1]
            else:
                print("Invalid choice. Please select a valid category number.\n")
                continue
        except ValueError:
            print("Invalid input. Please enter a number.\n")
            break
        try:
            description = input(f"Enter a {Fore.LIGHTCYAN_EX}description{Fore.RESET} for the activity: ")
        except ValueError:
            continue

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
            trip = Activity.find_by_trip_id(trip_id)
            print()
            for i, activity in enumerate(trip):
                print(f"{i+1}. {Fore.YELLOW}{activity.name}")
            selection = input(f"Select the activity to update or {Fore.BLUE}(re)turn{Fore.RESET} to previous menu:")
            if selection in ("re", "return"):
                break
            try:
                selection = int(selection)
                if 1<=selection<=len(trip):
                    name_ = trip[selection - 1].name
            except ValueError:
                continue
        else:
            name_ = input(f"Enter the name of the activity to update or {Fore.BLUE}(re)eturn{Fore.RESET} to go back: ")
        if name_ in ("e", "exit"):
            exit_program()
        if name_ in ("re", "return"):
            break
        if activity:= Activity.find_by_name(name_):
            try:
                new_name = input(f"Enter a new {Fore.MAGENTA}name{Fore.RESET} or press {Fore.LIGHTGREEN_EX}Enter{Fore.RESET} to keep {Fore.YELLOW}'{activity.name}'{Fore.RESET}: ")
                if new_name:
                    activity.name = new_name
                new_cost = input(f"Enter a new {Fore.GREEN}cost{Fore.RESET} or press {Fore.LIGHTGREEN_EX}Enter{Fore.RESET} to keep {Fore.GREEN}'{activity.cost}'{Fore.RESET}: ")
                if new_cost:
                    activity.cost = int(new_cost)
                new_currency = input(f"Enter a new {Fore.GREEN}currency{Fore.RESET} or press {Fore.LIGHTGREEN_EX}Enter{Fore.RESET} to keep {Fore.GREEN}'{activity.currency}'{Fore.RESET}: ").upper()
                if new_currency:
                    activity.currency = new_currency
                categories = activity_categories
                print()
                for idx, category in enumerate(categories):
                    print(f"{idx + 1}. {Fore.BLUE}{category}")
                print()
                print(f"Current category: {Fore.BLUE}{activity.category}{Fore.RESET}")
                print()
                category_choice = input(f"Choose a new {Fore.BLUE}category{Fore.RESET} or press {Fore.LIGHTGREEN_EX}Enter{Fore.RESET} to keep the current category: ")
                if category_choice:
                    try:
                        category_choice = int(category_choice)
                        if 1<= category_choice <= len(categories):
                            activity.category = categories[category_choice - 1]
                        else:
                            print("Invalid choice. Keeping the current category.")
                    except ValueError:
                        print("Invalid input. Keeping the current category.")
                        continue
                new_description = input(f"Add a new {Fore.LIGHTCYAN_EX}description{Fore.RESET} or press {Fore.LIGHTGREEN_EX}Enter{Fore.RESET} to keep the current description:\n{Fore.LIGHTCYAN_EX}'{activity.description}'{Fore.RESET}\n> ")
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
            activities_from_trip = Activity.find_by_trip_id(trip_id)
            for i, activity in enumerate(activities_from_trip):
                print(f"{i+1}. {Fore.YELLOW}{activity.name}")
            print()
            choice = input("Select the activity to delete: ")
            choice = int(choice)
            if 1<=choice<=len(activities_from_trip):
                activity_to_delete = activities_from_trip[choice - 1]
            id_confirm = input(f"Are you sure you want to delete '{activity_to_delete.name}'? (Y/N)").strip().lower()
            if id_confirm in ("e", "exit"):
                exit_program()
            if id_confirm == "y":
                activity_to_delete.delete()
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
            print("No activities found for the selected trip.")      
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

activity_categories = ["Relaxation", "Photography", "Entertainment", "Cultural", "Culinary", "Adventure", "Sports"]

def exit_program():
    print(f"{Fore.GREEN}Goodbye!")
    exit()
