#!/usr/bin/env python3
# lib/debug.py

from models.__init__ import CONN, CURSOR
from models.trip import Trip
from models.activity import Activity
import ipdb

def debug_trip_creation(name, location, start_date, end_date):
    print(f"Debugging Trip Creation: Name={name}, Location={location}, Start Date={start_date}, End Date={end_date}")
    trip = Trip.create(name, location, start_date, end_date)
    print(f"Created Trip: {trip}")
    ipdb.set_trace()  # Pause after creation to inspect the trip object

def debug_activity_creation(name, cost, category, description, trip_id):
    print(f"Debugging Activity Creation: Name={name}, Cost={cost}, Category={category}, Description={description}, Trip ID={trip_id}")
    activity = Activity.create(name, cost, category, description, trip_id)
    print(f"Created Activity: {activity}")
    ipdb.set_trace()  # Pause after creation to inspect the activity object

debug_trip_creation("Debug Trip", "Debug Location", "2024-01-01", "2024-01-05")
debug_activity_creation("Debug Activity", 100, "Debug Category", "Debug Description", 1)
