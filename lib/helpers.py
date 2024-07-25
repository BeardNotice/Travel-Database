# lib/helpers.py

from models.trip import Trip
from models.activity import Activity

def list_trips():
    trips = Trip.get_all()
    print("\n")
    for trip in trips:    
        print(f'"{trip.name}" in {trip.location}: {trip.start_date} - {trip.end_date}')
    print("\n")

def get_trips_by_name():
    name = input("Enter Trip's name: ")
    trip = Trip.find_by_name(name)
    print(trip) if trip else print(f'{trip} was not found.')

def create_trip():
    name = input("Enter a name for the trip: ")
    location = input("Add a location for the trip: ")
    start_date = input("Add the start date: ")
    end_date = input("Add the end date: ")
    try:
        trip = Trip.create(name, location, start_date, end_date)
        print(f'Sucessfully created {name}, details: {trip}')
    except Exception as exc:
        print("Error: ", exc)

def update_trip():
    name_ = input("Enter the name of the trip to update: ")
    if trip := Trip.find_by_name(name_):
        try:
            new_name = input(f"Enter a new name for {name_}")
            trip.name=new_name
            new_location = input('Enter a new location: ')
            trip.location = new_location
            new_start_date = input("Enter a new start date: ")
            trip.start_date = new_start_date
            new_end_date = input("Enter new end date: ")
            trip.end_date = new_end_date

            trip.update()
        except Exception as exc:
            print(f'Error updating: {exc}')
    else:
        print(f'{name_} was not found.')




def delete_trip():
    name = input("Enter the name of the trip to be deleted: ")
    trip = Trip.find_by_name(name)
    if trip:
        try:
            trip.delete()
            print(f'Sucessfully deleted {name}.')
        except Exception as exc:
            print(f'Error deleting {name}: {exc}')
    else:
        print(f'{name} was not found.')

def list_activities():
    activities = Activity.get_all()
    print("\n")
    for activity in activities:
        print(f'--"{activity.name}" ({activity.category})\n--Cost: {activity.cost} {activity.currency}\n--{activity.description}\n\n')

def find_activity_by_name():
    name = input("Enter the activity by the activity's name: ")
    activity = Activity.find_by_name(name)
    if activity:
        print(f'--"{activity.name}" ({activity.category})\n--Cost: {activity.cost} {activity.currency}\n--{activity.description}\n')
    else:
        print(f'{name} was not found.')

def find_activity_by_category():
    pass

def find_activity_by_currency():
    pass

def create_activity():
    pass

def update_activity():
    pass

def delete_activity():
    pass

def list_trip_activities():
    pass


def exit_program():
    print("Goodbye!")
    exit()
