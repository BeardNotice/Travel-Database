# Trip and Activity Logger CLI

This is a Python command-line interface (CLI) application that allows users to log and manage trips and associated activities. The program uses two models, `Trip` and `Activity`, to store information about trips and their corresponding activities and displays this information to the user.

## Features

- **Create and Manage Trips:** Users can create trips by specifying details such as the trip name, location, start date, and end date. Users can also update or delete existing trips.
- **Log Activities for Trips:** Users can log various activities for each trip, including the name, cost, category, description, and associated trip.
- **View Trips and Activities:** Users can view a list of all trips or activities, as well as search for trips and activities based on different criteria.

## Important Files

### `lib/cli.py`

The `cli.py` file is the core of the application, handling all user interactions. This file contains the command-line interface logic, parsing user inputs and invoking the appropriate functions to perform the requested operations.

- **Main CLI Loop:** The script runs a loop that listens for user commands, processes them, and calls the relevant functions from other modules to handle tasks like creating, updating, or listing trips and activities.
- **Command Handling:** Each user command is mapped to a specific function, making it easy to extend or modify the CLI's behavior. Commands include creating a trip, listing trips, creating an activity, and listing activities, among others.

### `lib/helpers.py`

The `helpers.py` file provides utility functions that support the main CLI operations. These functions handle common tasks, such as exiting the program, listing trips and activities, and formatting text output.

- **exit_program:** Safely exits the program, ensuring any necessary cleanup is performed.
- **list_trips:** Retrieves and displays all trips stored in the database.
- **get_trips_by_name:** Fetches trips that match a given name, providing a way to filter trips by their title.
- **create_trip:** Invokes the trip creation process, gathering user input and interacting with the database.
- **update_trip:** Allows users to update existing trip details.
- **delete_trip:** Handles the deletion of trips from the database.
- **list_activities:** Retrieves and displays all activities associated with a specific trip.
- **find_activity_by_name:** Searches for activities by name, allowing users to locate specific activities.

### `lib/trip.py` & `lib/activity.py`

The `trip.py` and `activity.py` files define the `Trip` and `Activity` models, respectively. These models encapsulate the properties and behaviors of trips and activities, including methods for interacting with the database. Many of the functions in these models are similar, as both types of records require similar CRUD (Create, Read, Update, Delete) operations.

- **create_table:** Sets up the database table for storing trips or activities if it doesn't already exist.
- **drop_table:** Removes the trips or activities table from the database, useful for resetting or cleaning up the data.
- **create:** Adds a new trip or activity to the database and returns the corresponding `Trip` or `Activity` object.
- **instance_from_db:** Converts a database row into a `Trip` or `Activity` instance, bridging the gap between raw data and the application's model.
- **update:** Updates the details of an existing trip or activity in the database.
- **delete:** Removes a trip or activity from the database.
- **all:** Retrieves all trips or activities from the database as a list of `Trip` or `Activity` objects.
- **find_by_id:** Finds a trip or activity by its unique ID.
- **find_by_name:** Searches for the first trip or activity matching a specified name.
- **activities (Trip specific):** Returns a list of activities associated with a specific trip, linking the `Trip` and `Activity` models.
- **trip (Activity specific):** Returns the `Trip` object associated with the activity, linking the `Activity` model back to the `Trip` model.

### `lib/__init__.py`

The `__init__.py` file is responsible for setting up the database connection and cursor, which are used throughout the application to interact with the SQLite database.

- **CONN:** The database connection object, allowing the application to execute SQL commands.
- **CURSOR:** The database cursor, used to execute queries and retrieve data from the database.

### `lib/seed.py`

The `seed.py` file is a utility script that populates the database with initial data. This is useful for testing or demonstrating the application's functionality.

- **seed_database:** Drops existing tables and recreates them, then inserts sample trips and activities into the database.

## Usage

1. **Setting Up the Environment:**
   - Make sure you have Python 3.x installed.
   - Install the necessary dependency by running:
     ```
     pip install colorama ipdb
     ```

2. **Running the CLI:**
   - To start the CLI, run the following command:
     ```
     python lib/cli.py
     ```

3. **Seeding the Database:**
   - To seed the database with sample data, run:
     ```
     python lib/seed.py
     ```
   - This will create initial trips and activities for you to explore.

## Contributing

Feel free to fork this repository and make changes as you see fit. Contributions are always welcome!

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
