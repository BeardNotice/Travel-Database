# lib/helpers.py

from models.trip import Trip
from models.activity import Activity

def list_trips():
    trips = Trip.get_all()
    print("\nTrips:\n")
    for i, trip in enumerate(trips):    
        print(f'{i + 1}. "{trip.name}" in {trip.location}: {trip.start_date} - {trip.end_date}')
    print("")

def get_trips_by_name():
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
        print(f'Sucessfully created {name}')
    except Exception as exc:
        print("Error: ", exc)

def update_trip():
    name_ = input("Enter the name of the trip to update: ")
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
        except Exception as exc:
            print(f'Error updating: {exc}\n')
    else:
        print(f'{name_} was not found.\n')

def delete_trip():
    name = input("Enter the name of the trip to be deleted: ")
    trip = Trip.find_by_name(name)
    if trip:
        confirmation = input(f'Are you sure you want to delete "{name}"? (Y/N)').strip().lower()
        if confirmation == "y":
            try:
                trip.delete()
                print(f'\nSucessfully deleted {name}.\n')
            except Exception as exc:
                print(f'\nError deleting {name}: {exc}\n')
        else:
            print("Cancelled Deletion.")
    else:
        print(f'\n{name} was not found.\n')

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

def create_activity():
    trips = Trip.get_all()
    if trips:
        print("Existing trips:")
        for idx, trip in enumerate(trips):
            print(f'{idx + 1}. {trip.name} in {trip.location}')
        choice = input("Select a trip by number or type 'new' to create a new trip: ")
        if choice.lower() == 'new':
            trip = create_trip()
        else:
            try:
                choice = int(choice)
                if 1<= choice <= len(trips):
                    trip = trips[choice - 1]
                else:
                    print("Invalid choice. Please select a valid trip number.\n")
                    return
            except ValueError:
                print("Invalid input. Please enter a number or 'new'.\n")
                return
    else:
        print("No existing trips found. You need to create a new trip.\n")
        trip = create_trip()

    name = input("Enter a name for the activity: ")
    cost = float(input("Enter a cost for the activity: "))
    currency = input("Enter a currency for the activity: ")

    categories = ["Relaxation", "Photography", "Entertainment", "Cultural", "Culinary", "Adventure", "Sports"]
    #category = input("Enter a category for the activity: ")
    for idx, category in enumerate(categories):
        print(f'{idx + 1}. {category}')
    category_choice = input("Enter the number corresponding to the category: ")
    try:
        category_choice = int(category_choice)
        if 1<= category_choice <= len(categories):
            category = categories[category_choice - 1]
        else:
            print("Invalid choice, Please select a valid category number.\n")
            return
    except ValueError:
        print("Invalid input. Please enter a number.\n")
    
    description = input("Enter a description for the activity: ")
    trip_id = trip.id

    try:
        Activity.create(name, cost, currency.upper(), category, description, trip_id)
        print(f'Successfully created {name}\n')
    except Exception as exc:
        print("Error: ", exc)
    

def update_activity():
    name_ = input("Enter the name of the activity to update: ")
    if activity:= Activity.find_by_name(name_):
        try:
            new_name = input(f"Enter a new name for {name_} or press Enter to keep '{activity.name}': ")
            if new_name:
                activity.name = new_name
            new_cost = input(f"Enter a new cost or press Enter to keep '{activity.cost}': ")
            if new_cost:
                activity.cost = new_cost
            new_currency = input(f"Enter a new currency or press Enter to keep '{activity.currency}': ")
            if new_currency:
                activity.currency = new_currency
            categories = ["Relaxation", "Photography", "Entertainment", "Cultural", "Culinary", "Adventure", "Sports"]
            print("Choose a new category for the activity or press Enter to keep the current category: ")
            for idx, category in enumerate(categories):
                print(f"{idx + 1}. {category}")
                print(f"Current category: {activity.category}")

            category_choice = input("Enter the number corresponding to the new category: ")
            if category_choice:
                try:
                    category_choice = int(category_choice)
                    if 1<= category_choice <= len(categories):
                        activity.category = categories[category_choice - 1]
                    else:
                        print("Invalid choice. Keeping the current category.")
                except ValueError:
                    print("Invalid input. Keeping the current category.")
            new_description = input(f"Add a new description or press Enter to keep the current description:\n'{activity.description}")
            if new_description:
                activity.description = new_description
            activity.update()
            print(f"Sucessfully updated {activity.name}")
        except Exception as exc:
            print("Error: ", exc)
    else:
        print(f"{name_} was not found.")


def delete_activity():
    name = input("Enter the name of the activity to be deleted: ")
    activity = Activity.find_by_name(name)
    if activity:
        confirm = input(f"Are you sure you want to Delete '{name}? (Y/N)").strip().lower()
        if confirm == "y":
            try:
                activity.delete()
                print(f'Succesfully deleted {name}.')
            except Exception as exc:
                print(f'Error deleting {name}: {exc}')
        else:
            print("Deletion cancelled.")
    else:
        print(f'{name} was not found.')

def list_trip_activities():
    trip_name = input("Enter the trip name to list its activities: ")
    trip = Trip.find_by_name(trip_name)
    if trip:
        activities = Activity.find_by_trip_id(trip.id)
    else:
        print(f'No trip found with the name {trip_name}')
        return
    if activities:
        for activity in activities:
            print(f'--"{activity.name}" ({activity.category})\n--Cost: {activity.cost} {activity.currency}\n--{activity.description}\n')
    else:
        print("No activities found for the selected criteria.")

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
    print("Goodbye!")
    exit()
