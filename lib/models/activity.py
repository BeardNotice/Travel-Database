# lib/models/activity.py

from models.__init__ import CURSOR, CONN
from models.trip import Trip

class Activity:
    
    all = {}

    def __init__(self, name, cost, currency, category, description, trip_id, id=None):
        self.id = id
        self.name = name
        self.cost = cost
        self.currency = currency
        self.category = category
        self.description = description
        self.trip_id = trip_id
    
    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, name):
        if isinstance(name, str) and len(name):
            self._name = name
        else:
            raise ValueError("Name must be a non-empty string.")
    
    @property
    def cost(self):
        return self._cost
    @cost.setter
    def cost(self, cost):
        if isinstance(cost, int):
            self._cost = cost
        else:
            raise ValueError("Cost must be an integer.")
    
    @property
    def currency(self):
        return self._currency
    @currency.setter
    def currency(self, currency):
        if isinstance(currency, str) and len(currency) == 3 and currency.isupper():
            self._currency = currency
        else:
            raise ValueError("Currency must be a 3-letter uppercase code.")

    @property
    def category(self):
        return self._category
    @category.setter
    def category(self, category):
        if isinstance(category, str) and len(category):
            self._category = category
        else:
            raise ValueError("Category must be a non-empty string.")


    @property
    def description(self):
        return self._description
    @description.setter
    def description(self, description):
        if isinstance(description, str):
            self._description = description
        else:
            raise ValueError("Description must be a string.")
    
    @property
    def trip_id(self):
        return self._trip_id
    @trip_id.setter
    def trip_id(self, trip_id):
        if type(trip_id) is int and Trip.find_by_id(trip_id):
            self._trip_id = trip_id
        else:
            raise ValueError("trip_id must reference a trip in the database")
    
    @classmethod
    def create_table(cls):
        """create a new table to persist the attributes of activity instances"""
        sql = """
            CREATE TABLE IF NOT EXISTS activities (
            id INTEGER PRIMARY KEY,
            name TEXT,
            cost INTEGER,
            currency TEXT,
            category TEXT,
            description TEXT,
            trip_id INTEGER,
            FOREIGN KEY (trip_id) REFERENCES trips(id));
        """
        CURSOR.execute(sql)
        CONN.commit()
    
    @classmethod
    def drop_table(cls):
        """drop the table that persists activity instances"""
        sql = """
            DROP TABLE IF EXISTS activities
        """
        CURSOR.execute(sql)
        CONN.commit()
    
    def save(self):
        """insert a new row with the name, cost, currency, category, description and trip id values of the current activity object.
        update object id attribute using the primary key value of new row
        save the object in local dictionary using table row's primary key as dictionary key"""
        sql = """
            INSERT INTO activities (name, cost, currency, category, description, trip_id)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        CURSOR.execute(sql, (self.name, self.cost, self.currency, self.category, self.description, self.trip_id))
        CONN.commit()
        self.id = CURSOR.lastrowid
        type(self).all[self.id] = self

    def update(self):
        """update the table row corresponding to the current activity instance"""
        sql = """
            UPDATE activities
            SET name = ?, cost = ?, currency = ?, category = ?, description = ?, trip_id = ?
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.name, self.cost, self.currency, self.category, self.description, self.trip_id, self.id))
        CONN.commit()
    
    def delete(self):
        """delete the table row corresponding to the current activity instance
        delete the dictionary entry, and reassign id attribute"""
        sql = """
            DELETE FROM activities
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.id,))
        CONN.commit()
        del type(self).all[self.id]
        self.id=None
    
    @classmethod
    def create(cls, name, cost, currency, category, description, trip_id):
        """init a new activity instance and save the object to the database"""
        activity = cls(name, cost, currency, category, description, trip_id)
        activity.save()
        return activity
    
    @classmethod
    def instance_from_db(cls, row):
        """return an activity object having the attribute values from the table row"""
        activity = cls.all.get(row[0])
        if activity:
            activity.name = row[1]
            activity.cost = row[2]
            activity.currency = row[3]
            activity.category = row[4]
            activity.description = row[5]
            activity.trip_id = row[6]
        else:
            activity = cls(row[1], row[2], row[3], row[4], row[5], row[6])
            activity.id = row[0]
            cls.all[activity.id] = activity
        return activity
    
    @classmethod
    def get_all(cls):
        """return a list containing one activity object per table row"""
        sql = """
            SELECT *
            FROM activities
        """
        rows = CURSOR.execute(sql).fetchall()
        return [cls.instance_from_db(row) for row in rows]
    
    @classmethod
    def find_by_id(cls, id):
        """return activity object corresponding to the table row matching the specified PK"""
        sql = """
            SELECT *
            FROM activities
            WHERE id = ?
        """
        row = CURSOR.execute(sql, (id,)).fetchone()
        return cls.instance_from_db(row) if row else None
    
    @classmethod
    def find_by_name(cls, name):
        "return activity object corresponding to first table row matching specified name"
        sql = """
            SELECT *
            FROM activities
            WHERE name = ?
        """
        row = CURSOR.execute(sql, (name,)).fetchone()
        return cls.instance_from_db(row) if row else None
    
    @classmethod
    def find_by_currency(cls, currency):
        """return a list of activity objects corresponding to table rows matching the specified currency"""
        sql = """
            SELECT *
            FROM activities
            WHERE currency = ?
        """
        rows = CURSOR.execute(sql, (currency,)).fetchall()
        return [cls.instance_from_db(row) for row in rows]
    
    @classmethod
    def find_by_category(cls, category):
        """return a list of activity objects corresponding to table rows matching the specified category"""
        sql = """
            SELECT *
            FROM activities
            WHERE category = ?
        """
        rows = CURSOR.execute(sql, (category,)).fetchall()
        return [cls.instance_from_db(row) for row in rows]
    
    @classmethod
    def find_by_trip_id(cls, trip_id):
        """return a list of activity objects corresponding to table rows matching the specified trip_id"""
        sql = """
            SELECT *
            FROM activities
            WHERE trip_id = ?
        """
        rows = CURSOR.execute(sql, (trip_id,)).fetchall()
        return [cls.instance_from_db(row) for row in rows]