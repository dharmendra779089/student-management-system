# Student Management System 🎓

A command-line Python application for managing student records. This project demonstrates core Python concepts including Object-Oriented Programming (OOP), file handling with JSON, loops, and robust error handling.

## Features
* **Add Students:** Register new students with ID, Name, Age, Gender, Course, and Marks.
* **View All:** Display a cleanly formatted tabular list of all registered students alongside their calculated letter grades.
* **Search:** Quickly find a student's complete details using their unique ID.
* **Update & Delete:** Modify a student's profile or remove them from the system (includes safety confirmation).
* **Statistics:** Automatically calculate the total number of students, average marks, highest achiever, and lowest achiever.
* **Data Persistence:** All records are saved securely to a `students.json` file.

## Built-In Protections 🛡️
* Prevents creating multiple students with the exact same ID.
* Validates inputs (Age > 0, Marks 0-100, no empty names).
* Safely catches invalid text entries when numbers are required.
* Handles missing or corrupted JSON files gracefully on startup.
* Prevents crashes on empty data searches or `Ctrl + C` keyboard interrupts.

## File Structure
* `main.py`: The entry point containing the interactive menu and core logic.
* `student.py`: Contains the `Student` class used to structure data.
* `data_handler.py`: Manages saving to and loading from the `.json` file.
* `students.json`: The database file (generated automatically upon adding a student).

## How to Run
1. Ensure you have Python 3.10+ installed on your computer.
2. Download or clone this repository so all files are in the same folder.
3. Open your terminal or command prompt.
4. Navigate to the project folder.
5. Run the application using the command: `python main.py`

## Assumptions Made
* **Student ID representation**: Student ID is treated as a unique string to allow alphanumeric IDs (e.g., "S101"), rather than restricting it solely to integer numbers.
* **Gender Standardisation**: Gender values are validated and automatically formatted to "Male", "Female", or "Other". Single letters such as `m`/`M`, `f`/`F`, or `o`/`O` are automatically resolved to their complete equivalents.
* **Marks Representation**: Marks are stored as floats to accommodate decimal score entries (e.g., 85.5), while still strictly validated between 0 and 100 inclusive.
* **Data Storage Location**: The database is stored in `students.json` in the same directory as the script. If deleted, it initializes as a new empty array `[]` automatically.
* **Updating Gender**: In accordance with typical record updates and standard configurations, Gender is not updated in Option 4 (Update Student), aligning with the specification.
* **Ctrl+C Safety**: Any keyboard interruption automatically writes current memory contents safely to `students.json` before ending the session.