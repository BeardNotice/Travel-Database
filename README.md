
# Travel Database CLI

This Python command-line interface (CLI) application allows users to log and manage trips and their associated activities. The application is centered around two primary models, `Trip` and `Activity`, which are related in a one-to-many relationship. Users can perform CRUD (Create, Read, Update, Delete) operations on both trips and activities, with the `manage_trips()` function serving as the central hub for navigation.

## Central Function: `manage_trips()`

The `manage_trips()` function is the core of this application, acting as the primary interface for users to interact with both trips and their associated activities. This function allows users to manage trips and their activities seamlessly within a one-to-many relationship, enabling CRUD operations for both entities at different levels of interaction.

- **Manage Trips and Activities**: Users can view all trips, create new ones, or select a specific trip to manage its details. Once a trip is selected, users can navigate into a lower-level loop to manage its associated activities.
- **Higher-Level Loop for Trip Management**: From this loop, users can create, update, or delete trips. This loop continuously refreshes to display the most up-to-date list of trips.
- **Lower-Level Loop for Activity Management**: After selecting a trip, users can manage its activities. This nested loop allows for creating, updating, and deleting activities linked to the selected trip, providing a focused context for managing data.
- **Seamless Navigation**: The function provides a smooth experience for moving between trip management and activity management without requiring users to exit and re-enter different modes.

## Key Components

### `lib/cli.py`

The `cli.py` file is the main script that runs the application and handles user input. It interacts with both the `Trip` and `Activity` models through the `manage_trips()` function and various helper functions.

- **Command Handling**: User commands trigger functions like `manage_trips()`, which handles most user interactions for trips and activities.
- **Error Handling and Input Validation**: The CLI is equipped with mechanisms to validate user input and handle errors gracefully, ensuring a smooth user experience.
- **Helper Functions**: Functions such as `create_trip()`, `update_trip()`, `delete_trip()`, `list_activities()`, etc., provide specific functionality within the main loop to manage both trips and activities.

### Models: `Trip` and `Activity`

#### `lib/models/trip.py`

The `Trip` class represents a trip and contains methods for interacting with the database to manage trip records.

- **CRUD Operations**: Includes methods like `create()`, `update()`, `delete()`, `find_by_id()`, and `find_by_name()` to handle all trip-related operations.
- **Relationship Management**: The `activities()` method retrieves all activities associated with a particular trip, maintaining the one-to-many relationship between trips and activities.

#### `lib/models/activity.py`

The `Activity` class represents activities associated with trips and contains methods for managing activity records.

- **CRUD Operations**: Similar to the `Trip` model, it includes `create()`, `update()`, `delete()`, `find_by_id()`, and `all()` methods to manage activities.
- **Relationship Linking**: The `trip()` method links an activity back to its associated trip, reinforcing the relationship between the two models.

### Helper Functions (`lib/helpers.py`)

`helpers.py` contains utility functions that support the `manage_trips()` function and other parts of the application. These functions handle specific tasks like creating, updating, and deleting trips and activities, as well as managing user input and displaying data.

- **Reusable Functions**: Functions like `confirm_action()` for user confirmations, `get_user_input()` for validated input, and CRUD operations ensure consistency and reusability across the application.

### Debugging and Seeding (`lib/debug.py` and `lib/seed.py`)

- **`debug.py`**: Contains functions to debug the creation and manipulation of `Trip` and `Activity` objects using `ipdb`, making it easier to troubleshoot and test the application.
- **`seed.py`**: Seeds the database with initial data for testing or demonstration purposes. It safely drops existing tables (if they exist), recreates them, and populates them with sample trips and activities.

## Setup and Usage

1. **Install Dependencies**:
   ```bash
   pip install colorama ipdb
   ```

2. **Run the CLI**:
   ```bash
   python lib/cli.py
   ```

3. **Seed the Database**:
   ```bash
   python lib/seed.py
   ```

## Contributing

Contributions are welcome. Please fork the repository and create a pull request with your changes.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.
