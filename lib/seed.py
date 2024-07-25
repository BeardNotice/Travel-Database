#!/usr/bin/env python3
# lib/seed.py

from models.__init__ import CONN, CURSOR
from models.trip import Trip
from models.activity import Activity

def seed_database():
    Activity.drop_table()
    Trip.drop_table()
    Trip.create_table()
    Activity.create_table()

    spring_break = Trip.create("Spring Break", "Bahamas", "4/20/2024", "4/24/2024")
    summer_trip = Trip.create("Family Get Together", "New Mexico", "6/28/2024", "7/05/2024")
    fall_trip = Trip.create("United Kingdom Trip", "United Kingdom", "10/23/2024", "11/06/2024")
    Activity.create("Water Park", 0, "USD", "Relaxation", "Playing at the water park.", spring_break.id)
    Activity.create("Beach", 0, "USD", "Relaxation", "Lounge and tan on the beach.", spring_break.id)
    Activity.create("Family Pictures", 350, "USD", "Photography", "Get picturs of the family professionally taken", spring_break.id)
    Activity.create("Dolphin Petting", 200, "USD", "Entertainment", "Taking our niece to play with the dolphins", spring_break.id)
    Activity.create("Visit Taos", 0, "USD", "Cultural", "Trip to the local town to check out the art.", summer_trip.id)
    Activity.create("Wheeler Hike", 0, "USD", "Adventure", "Hike up the tallest mountain in the state", summer_trip.id)
    Activity.create("Lunch at Orlando's", 100, "USD", "Culinary", "Lunch at a local staple called Orlando's in Taos.", summer_trip.id)
    Activity.create("Tree Clearing", 0, "USD", "Adventure", "Clear trees around the property.", summer_trip.id)
    Activity.create("Tower of London", 35, "GBP", "Cultural", "Tour of the tower of London", fall_trip.id)
    Activity.create("Lunch at Witchery", 100, "GBP", "Culinary", "Lunch at The Witchery in Edinburgh", fall_trip.id)

seed_database()
print("Database seeded.")