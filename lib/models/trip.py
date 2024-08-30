# lib/models/trip.py

from models.__init__ import CURSOR, CONN
from datetime import datetime

class Trip:
    
    all = {}

    def __init__(self, name, location, start_date, end_date, id=None):
        self.id = id
        self.name = name
        self.location = location
        self.start_date = start_date
        self.end_date = end_date

    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, name):
        if isinstance(name, str) and len(name):
            self._name = name
        else:
            raise ValueError("Name must be an non-empty string.")
    
    @property
    def location(self):
        return self._location
    @location.setter
    def location(self, location):
        if isinstance(location, str) and len(location):
            self._location = location
        else:
            raise ValueError("Location must be a non-empty string.")
    
    @property
    def start_date(self):
        return self._start_date
    @start_date.setter
    def start_date(self, start_date):
        if isinstance(start_date, str) and datetime.strptime(start_date, "%m/%d/%Y"):
            self._start_date = start_date
        else:
            raise ValueError("Start Date must be a non-empty string in the format mm/dd/yyyy.")
        
    @property
    def end_date(self):
        return self._end_date
    @end_date.setter
    def end_date(self, end_date):
        if isinstance(end_date, str) and datetime.strptime(end_date, "%m/%d/%Y"):
            self._end_date = end_date
        else:
            raise ValueError("End Date must be a non-empty string in the format mm/dd/yyyy.")
    

    @classmethod
    def create_table(cls):
        """Create a new table to persist the attributes of Trip instances"""
        sql = """
            CREATE TABLE IF NOT EXISTS trips (
            id INTEGER PRIMARY KEY,
            name TEXT,
            location TEXT,
            start_date TEXT,
            end_date TEXT);
        """
        CURSOR.execute(sql)
        CONN.commit()
    
    @classmethod
    def drop_table(cls):
        """Drop the table that persists trip instances"""
        sql = """
            DROP TABLE IF EXISTS trips;
            """
        CURSOR.execute(sql)
        CONN.commit()
    
    def save(self):
        """Insert a new row with the name, location, start, and end date values of the current trip instance.
        Update object id attribute using the primary key value of new row.
        Save the object in local dictionary using table row's primary key as dictionary key."""
        sql = """
            INSERT INTO trips (name, location, start_date, end_date)
            VALUES (?, ?, ?, ?)
        """

        CURSOR.execute(sql, (self.name, self.location, self.start_date, self.end_date))
        CONN.commit()
        self.id = CURSOR.lastrowid
        type(self).all[self.id] = self
    
    @classmethod
    def create(cls, name, location, start_date, end_date):
        """Init a new trip instance and save the object to the database."""
        trip = cls(name, location, start_date, end_date)
        trip.save()
        return trip
    
    def update(self):
        """Update the table row corresponding to the current trip instance."""
        sql = """
            UPDATE trips
            SET name = ?, location = ?, start_date = ?, end_date = ?
            WHERE id = ?
        """

        CURSOR.execute(sql, (self.name, self.location, self.start_date, self.end_date, self.id))
        CONN.commit()
    
    def delete(self):
        """delete the table row corresponding to the current trip instance,
        delete the dictionary entry, and reassign id attribute"""
        sql = """
            DELETE FROM trips
            where id = ?
        """
        CURSOR.execute(sql, (self.id,))
        CONN.commit()

        if self.id in type(self).all:
            del type(self).all[self.id]
        self.id = None
    
    @classmethod
    def instance_from_db(cls, row):
        """return a trip object having the attribute values from the table row."""

        trip = cls.all.get(row[0])
        if trip:
            trip.name = row[1]
            trip.location = row[2]
            trip.start_date = row[3]
            trip.end_date = row[4]
        else:
            trip = cls(row[1], row[2], row[3], row[4])
            trip.id = row[0]
            cls.all[trip.id] = trip
        return trip
    
    @classmethod
    def get_all(cls):
        """return a list containing a trip object per row in the table"""
        sql = """
            SELECT *
            FROM trips
        """
        rows = CURSOR.execute(sql).fetchall()
        return [cls.instance_from_db(row) for row in rows]
    
    @classmethod
    def find_by_id(cls, id):
        """return a trip object corresponding to the table row matching the specified primary key"""
        sql = """
            SELECT *
            FROM trips
            WHERE id = ?
        """
        row = CURSOR.execute(sql, (id,)).fetchone()
        return cls.instance_from_db(row) if row else None
    
    @classmethod
    def find_by_name(cls, name):
        """return a trip object corresponding to first table row matching specified name"""
        sql = """
            SELECT *
            FROM trips
         WHERE name = ?
        """
        row = CURSOR.execute(sql, (name,)).fetchone()
        return cls.instance_from_db(row) if row else None
    
    @classmethod
    def find_by_location(cls, location):
        """return a list of trip objects corresponding to table rows matching specified location"""
        sql = """
            SELECT *
            FROM trips
            WHERE location = ?
        """
        rows = CURSOR.execute(sql, (location,)).fetchall()
        return [cls.instance_from_db(row) for row in rows]
    
    def activities(self):
        """return a list of activities associated with current trip"""
        from models.activity import Activity
        sql = """
            SELECT * FROM activities
            WHERE trip_id = ?
        """
        CURSOR.execute(sql, (self.id,),)
        rows = CURSOR.fetchall()
        return [Activity.instance_from_db(row) for row in rows]