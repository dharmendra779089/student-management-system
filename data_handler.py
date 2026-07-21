# Import the json module from Python's standard library to work with JSON files
import json
# Import the os module to check if a file exists and to resolve file paths
import os

# Build an absolute path to 'students.json' that is always located in the same
# directory as this script, regardless of where Python is invoked from.
# os.path.abspath(__file__) gives the full path to data_handler.py itself.
# os.path.dirname() strips the filename to get just the folder path.
# os.path.join() then appends 'students.json' to that folder path.
FILE_NAME = os.path.join(os.path.dirname(os.path.abspath(__file__)), "students.json")


def load_data():
    """
    Load student records from the JSON file.

    - If the file does not exist, return an empty list (the file will be
      created automatically the first time save_data() is called).
    - If the file exists but contains invalid/corrupted JSON, print a
      warning and return an empty list so the program can still start.

    Returns:
        list: A list of student dictionaries loaded from the file.
    """
    # Check whether the JSON file actually exists on the computer
    if not os.path.exists(FILE_NAME):
        # If the file is missing, return a fresh empty list (no crash)
        return []

    # Use a try block to safely attempt reading the file
    try:
        # Open the file in read mode ("r") using a 'with' block so it closes automatically
        with open(FILE_NAME, "r") as file:
            # Use json.load() to parse the file contents into a Python list of dictionaries
            data = json.load(file)
            # Return the loaded data to the caller
            return data
    # Catch the error that occurs if the file contains broken/invalid JSON
    except json.JSONDecodeError:
        # Inform the user that the file was unreadable
        print("Warning: students.json is corrupted. Starting with empty data.")
        # Return an empty list so the program can continue running
        return []


def save_data(student_list):
    """
    Save the current list of student records to the JSON file.

    The file is created automatically if it does not exist.
    Data is written with indentation for human readability.

    Args:
        student_list (list): The list of student dictionaries to save.
    """
    # Use a try block to safely attempt writing to the file
    try:
        # Open the file in write mode ("w") — this creates the file if it doesn't exist
        with open(FILE_NAME, "w") as file:
            # Use json.dump() to convert the Python list into formatted JSON and write it
            # indent=4 makes the file human-readable with proper spacing
            json.dump(student_list, file, indent=4)
    # Catch any unexpected error during file writing (e.g., disk full, permission denied)
    except IOError:
        # Print a friendly error message instead of crashing
        print("Error: Could not save data to file.")