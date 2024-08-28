
# Trip and Activity Logger CLI

This Python command-line interface (CLI) application allows users to log and manage trips and their associated activities. The program includes two primary models, `Trip` and `Activity`, to store and manage details about trips and activities, enabling users to create, update, delete, and view this information through a text-based interface.

## Important Files

### `lib/cli.py`

The `cli.py` file is the main script for interacting with the application via the command line. It handles all user inputs and guides users through various operations, such as creating trips, adding activities, and viewing existing data. The script operates in a loop, continuously listening for user commands until an exit command is issued.

- **Main CLI Loop:** The loop runs indefinitely, prompting the user for input and responding accordingly. Commands like `create_trip`, `create_activity`, `manage_trips`, `list_activities`, and `exit_program` trigger respective functions to handle these actions.
- **Command Handling:** Commands are mapped to specific functions, each of which provides feedback to the user. For example, when a user types "create trip," the script invokes the `create_trip()` function, which collects details from the user and calls the relevant model method to store this information.
- **Error Handling:** The script includes error handling for invalid inputs, prompting users to re-enter commands when necessary.
- **User Guidance:** Displays options and instructions to help users navigate through different functionalities, ensuring a smooth user experience.

#### Detailed Description: `manage_trips()` Function

When users activate the `manage_trips()` function, the following steps occur:

1. **Retrieve Trip Data:** The function queries the database to retrieve all existing trips using the `all()` method from the `Trip` class, which fetches all trip records and returns them as a list of `Trip` objects.

2. **Display Trip List:** The function then formats the retrieved trip data for display in a user-friendly way, presenting a numbered list of trips (including details like trip name, location, start date, and end date) in the console.

3. **Manage Submenu for Trip Selection:**
   - **Submenu Activation:** After displaying the trips, the user is prompted to select a specific trip by entering the corresponding number from the list. Selecting a trip triggers a submenu specifically for managing activities related to that trip.
   - **Submenu Options:**
     - **View Activities:** Displays all activities associated with the selected trip, allowing the user to see detailed information (e.g., name, cost, category, description).
     - **Create Activity:** Allows the user to create a new activity directly linked to the selected trip, prompting for all necessary details (name, cost, category, description).
     - **Update Activity:** Enables the user to update an existing activity for the selected trip, allowing changes to any of the activity's details.
     - **Delete Activity:** Provides the option to delete an activity from the selected trip, removing it from the database.

4. **Interactive User Control:** The user remains within this submenu until they choose to exit back to the main menu. Each option is selected by entering the appropriate command or number, ensuring an interactive and dynamic experience.

5. **Error Handling and Feedback:** Throughout this process, the function handles any potential errors (e.g., invalid trip selection, database access issues) and provides clear feedback to the user, such as prompting for re-selection or displaying error messages.

6. **Return to Main CLI Loop:** Once the user exits the trip-specific submenu, control returns to the main CLI loop, allowing the user to perform additional actions or exit the program.

### `lib/helpers.py`

The `helpers.py` file contains utility functions that support the main operations of the CLI. These functions handle tasks that are used frequently throughout the program, ensuring code modularity and reusability.

- **`exit_program`:** Safely exits the program, ensuring any necessary cleanup is performed before termination.
- **`manage_trips`:** Retrieves and displays all trips stored in the database, formatted for readability.
- **`list_activities`:** Retrieves and displays all activities associated with trips, formatted for readability.
- **`get_trips_by_name`:** Searches and returns trips that match a given name, enhancing the search functionality.
- **`format_output`:** Provides formatting utilities for displaying information.

### `lib/debug.py`

The `debug.py` file provides debugging tools for developers. It includes functions that test and debug the creation of `Trip` and `Activity` objects, allowing developers to inspect and verify the behavior of these objects.

- **`debug_trip_creation(name, location, start_date, end_date)`:** Creates a trip with the specified parameters and uses `ipdb` to pause execution for inspection.
- **`debug_activity_creation(name, cost, category, description, trip_id)`:** Creates an activity associated with a given trip and uses `ipdb` for debugging purposes.

### `lib/seed.py`

The `seed.py` file is a utility script designed to populate the database with initial data. This is useful for testing or demonstrating the application's functionality without manually entering data.

- **`seed_database()`:** Drops existing tables (if any), recreates them, and inserts a predefined set of trips and activities. This function is essential for quickly setting up a working dataset to explore and test the application's features.

### `lib/__init__.py`

The `__init__.py` file initializes the application's database environment. It sets up a connection to the SQLite database and provides a cursor for executing SQL commands.

- **`CONN`:** The database connection object that establishes and maintains a connection with the SQLite database.
- **`CURSOR`:** The cursor object used to execute SQL commands and retrieve results from the database.

### `lib/trip.py`

The `trip.py` file defines the `Trip` class, representing a trip within the application. This model handles all database interactions related to trips, providing methods for creating, retrieving, updating, and deleting trips.

- **`create(name, location, start_date, end_date)`:** Creates a new trip record in the database with the provided details.
- **`update(id, name, location, start_date, end_date)`:** Updates an existing trip record identified by its ID with the new details provided.
- **`delete(id)`:** Deletes a trip record from the database using its ID.
- **`find_by_id(id)`:** Searches for a trip by its unique ID and returns the corresponding object.
- **`find_by_name(name)`:** Searches for the first trip matching a specified name.
- **`all()`:** Retrieves all trip records from the database as a list of `Trip` objects.
- **`activities()`:** Returns a list of activities associated with a specific trip, establishing a link between the `Trip` and `Activity` models.

### `lib/activity.py`

The `activity.py` file defines the `Activity` class, representing an activity that can be associated with a trip. This model handles all database interactions related to activities, providing methods for managing activities' data.

- **`create(name, cost, category, description, trip_id)`:** Creates a new activity record in the database and associates it with a specific trip.
- **`update(id, name, cost, category, description, trip_id)`:** Updates an existing activity record identified by its ID with new details.
- **`delete(id)`:** Deletes an activity record from the database using its ID.
- **`find_by_id(id)`:** Finds an activity by its unique ID and returns the corresponding object.
- **`all()`:** Retrieves all activity records from the database as a list of `Activity` objects.
- **`trip()`:** Returns the `Trip` object associated with the activity, linking back to the `Trip` model.

## Usage

1. **Setting Up the Environment:**
   - Ensure Python 3.x is installed.
   - Install the necessary dependencies by running:
     \`\`\`bash
     pip install colorama ipdb
     \`\`\`

2. **Running the CLI:**
   - To start the CLI, run the following command:
     \`\`\`bash
     python lib/cli.py
     \`\`\`

3. **Seeding the Database:**
   - To seed the database with sample data, run:
     \`\`\`bash
     python lib/seed.py
     \`\`\`
   - This will create initial trips and activities for you to explore.

## Contributing

Feel free to fork this repository and make changes as you see fit. Contributions are always welcome!

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
