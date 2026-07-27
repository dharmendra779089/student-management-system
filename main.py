# Import the custom data_handler module we created to handle file saving/loading
import data_handler
# Import the Student class from our custom student.py module
from student import Student

# --- Helper Functions for Validation ---

import re

# Define a function to ensure the user enters a valid text-only name (no numbers allowed)
def get_valid_name(prompt):
    while True:
        name = input(prompt).strip()
        if not name:
            print("Error: Name cannot be empty.")
            continue
        if any(char.isdigit() for char in name):
            print("Error: Name cannot contain numbers. Please enter text only.")
            continue
        if not re.match(r"^[A-Za-z\s.'-]+$", name):
            print("Error: Name must contain letters and text characters only.")
            continue
        return name

# Define a function to ensure the user enters a valid whole number between 0 and 100 for Age
def get_valid_age():
    while True:
        try:
            val_str = input("Enter Age (0-100): ").strip()
            age_float = float(val_str)
            if not age_float.is_integer():
                print("Error: Age must be a whole number (no decimals allowed).")
                continue
            age = int(age_float)
            if 0 <= age <= 100:
                return age
            print("Error: Age must be a whole number between 0 and 100.")
        except ValueError:
            print("Invalid input. Please enter a whole number between 0 and 100.")

# Define a function to ensure the user enters a valid percentage between 0 and 100 for Marks
def get_valid_marks():
    while True:
        try:
            marks = float(input("Enter percentage of marks (0-100%): "))
            if 0 <= marks <= 100:
                return marks
            print("Error: Percentage of marks must be between 0 and 100.")
        except ValueError:
            print("Invalid input. Please enter a valid number for percentage.")

# Define a simple function to calculate a letter grade based on numeric marks
def get_grade(marks):
    # If marks are 90 or above, return 'A'
    if marks >= 90: return 'A'
    # Otherwise, if 80 or above, return 'B'
    elif marks >= 80: return 'B'
    # Otherwise, if 70 or above, return 'C'
    elif marks >= 70: return 'C'
    # Otherwise, if 60 or above, return 'D'
    elif marks >= 60: return 'D'
    # If all previous checks fail (marks are below 60), return 'F'
    else: return 'F'

# Define a function to retrieve a validated gender, mapping single letters ('m' or 'f') to full words
def get_valid_gender():
    while True:
        # Prompt for gender, strip spaces, and convert to lowercase
        gender_input = input("Enter Gender (Male/Female/Other or M/F/O): ").strip().lower()
        if gender_input in ["m", "male"]:
            return "Male"
        elif gender_input in ["f", "female"]:
            return "Female"
        elif gender_input in ["o", "other"]:
            return "Other"
        else:
            print("Error: Invalid Gender. Please enter Male (M), Female (F), or Other (O).")

def get_next_available_id(student_list):
    used_ids = {int(s["student_id"]) for s in student_list if str(s.get("student_id", "")).isdigit()}
    for candidate in range(100, 1000):
        if candidate not in used_ids:
            return str(candidate)
    return "100"

# --- Main Program Logic ---

# Define the main function that drives the entire application
def main():
    # Load the existing data from the JSON file into a variable called 'student_list'
    student_list = data_handler.load_data()
    
    # Wrap the entire main loop in a try block to catch KeyboardInterrupt (Ctrl+C)
    try:
        # Start the infinite loop for the main application menu
        while True:
            # Print the main menu options to the screen
            print("\n=== Student Management System ===")
            print("1. Add Student")
            print("2. View All Students")
            print("3. Search Student")
            print("4. Update Student")
            print("5. Delete Student")
            print("6. Show Statistics")
            print("7. Exit")
            
            # Get the user's choice and store it as a string
            choice = input("Enter your choice (1-7): ")
            
            # --- OPTION 1: Add Student ---
            if choice == "1":
                print("\n--- Add Student ---")
                next_suggested_id = get_next_available_id(student_list)
                # Ask for the student ID, validating numeric range 100-999 and uniqueness (defaults to next available ID)
                while True:
                    student_id_input = input(f"Enter Student ID (100-999) [Press Enter for default '{next_suggested_id}']: ").strip()
                    if not student_id_input:
                        student_id = next_suggested_id
                    else:
                        try:
                            id_num = int(student_id_input)
                            if not (100 <= id_num <= 999):
                                print("Error: Student ID must be a whole number from 100 to 999.")
                                continue
                            student_id = str(id_num)
                        except ValueError:
                            print("Error: Student ID must be a whole number from 100 to 999.")
                            continue

                    if any(student["student_id"] == student_id for student in student_list):
                        print("Error: A student with this ID already exists.")
                        continue
                    break
                
                # Call our helper functions to safely collect the rest of the data
                name = get_valid_name("Enter Name: ")
                age = get_valid_age()
                gender = get_valid_gender()
                course = get_valid_name("Enter Course: ")
                marks = get_valid_marks()
                
                # Create a new Student object using the data we just collected
                new_student = Student(student_id, name, age, gender, course, marks)
                # Convert the object to a dictionary and append it to our main list
                student_list.append(new_student.to_dict())
                # Save the newly updated list to the JSON file
                data_handler.save_data(student_list)
                # Confirm success to the user
                print("Student added successfully!")

            # --- OPTION 2: View All Students ---
            elif choice == "2":
                print("\n--- All Students ---")
                # Check if the list is completely empty
                if len(student_list) == 0:
                    print("No students found.")
                else:
                    # Print the table headers, using format specifiers (e.g., :<10) to align columns to the left
                    print(f"{'ID':<10} {'Name':<15} {'Course':<15} {'Marks':<10} {'Grade'}")
                    # Print a dashed line to separate the header from the data
                    print("-" * 60)
                    # Sort students by ID from least to max (ascending)
                    sorted_students = sorted(student_list, key=lambda s: int(''.join(filter(str.isdigit, str(s["student_id"]))) or 0))
                    # Loop through every dictionary in the sorted_students list
                    for student in sorted_students:
                        # Calculate the grade for this specific student
                        grade = get_grade(student["marks"])
                        # Print the student's data using the exact same column widths as the header
                        print(f"{student['student_id']:<10} {student['name']:<15} {student['course']:<15} {student['marks']:<10} {grade}")

            # --- OPTION 3: Search Student ---
            elif choice == "3":
                print("\n--- Search Student ---")
                # Prevent searching if the system is empty
                if len(student_list) == 0:
                    print("System is empty.")
                    continue
                    
                # Ask the user for the ID they want to find
                search_id = input("Enter Student ID to search: ")
                # Create a flag variable to track if we find a match, initially set to False
                found = False
                
                # Loop through the list
                for student in student_list:
                    # Check if the current dictionary's ID matches the searched ID
                    if search_id == student["student_id"]:
                        # If a match is found, print all their details
                        print("\nStudent Details:")
                        print(f"ID: {student['student_id']}")
                        print(f"Name: {student['name']}")
                        print(f"Age: {student['age']}")
                        print(f"Gender: {student['gender']}")
                        print(f"Course: {student['course']}")
                        # Print marks and call get_grade() inside the f-string
                        print(f"Marks: {student['marks']} (Grade {get_grade(student['marks'])})")
                        # Set the flag to True so we know we found them
                        found = True
                        # Stop looping since we found the exact student
                        break
                
                # After the loop, if the flag is still False, it means no match was found
                if not found:
                    print("Student not found.")

            # --- OPTION 4: Update Student ---
            elif choice == "4":
                print("\n--- Update Student ---")
                if len(student_list) == 0:
                    print("System is empty.")
                    continue
                    
                # Get the ID to update
                search_id = input("Enter Student ID to update: ")
                found = False
                
                for student in student_list:
                    # Find the matching student
                    if search_id == student["student_id"]:
                        print("Enter new details below:")
                        # Allow updating Student ID (press Enter to keep current ID)
                        while True:
                            new_id_input = input(f"Enter new Student ID (100-999) [Press Enter to keep '{search_id}']: ").strip()
                            if not new_id_input:
                                new_id = search_id
                                break
                            try:
                                id_num = int(new_id_input)
                                if not (100 <= id_num <= 999):
                                    print("Error: Student ID must be a whole number from 100 to 999.")
                                    continue
                                new_id = str(id_num)
                            except ValueError:
                                print("Error: Student ID must be a whole number from 100 to 999.")
                                continue

                            if new_id != search_id and any(s["student_id"] == new_id for s in student_list):
                                print("Error: A student with this ID already exists.")
                                continue
                            break

                        student["student_id"] = new_id
                        student["name"] = get_valid_name("Enter new Name: ")
                        student["age"] = get_valid_age()
                        student["gender"] = get_valid_gender()
                        student["course"] = get_valid_name("Enter new Course: ")
                        student["marks"] = get_valid_marks()
                        
                        # Save the modified list back to the file
                        data_handler.save_data(student_list)
                        print("Student updated successfully!")
                        found = True
                        break
                        
                if not found:
                    print("Student not found.")

            # --- OPTION 5: Delete Student ---
            elif choice == "5":
                print("\n--- Delete Student ---")
                if len(student_list) == 0:
                    print("System is empty.")
                    continue
                    
                search_id = input("Enter Student ID to delete: ")
                found = False
                
                for student in student_list:
                    if search_id == student["student_id"]:
                        # Ask for a Y/N confirmation and convert their answer to uppercase
                        confirm = input(f"Are you sure you want to delete {student['name']}? (Y/N): ").upper()
                        # If they type 'Y'
                        if confirm == 'Y':
                            # Remove this specific dictionary from the list
                            student_list.remove(student)
                            # Save the updated list to the file
                            data_handler.save_data(student_list)
                            print("Student deleted successfully!")
                        # If they type anything other than 'Y'
                        else:
                            print("Deletion cancelled.")
                        
                        found = True
                        break
                        
                if not found:
                    print("Student not found.")

            # --- OPTION 6: Show Statistics ---
            elif choice == "6":
                print("\n--- Statistics ---")
                # Ensure there is data to analyze to prevent dividing by zero errors later
                if len(student_list) == 0:
                    print("No data to analyze.")
                else:
                    # Find the total amount of students by checking the length of the list
                    total_students = len(student_list)
                    # Create a variable to hold the running sum of all marks
                    total_marks = 0
                    # Assume the first student in the list has both the highest and lowest marks to start
                    highest_student = student_list[0]
                    lowest_student = student_list[0]
                    
                    # Loop through everyone to update our math variables
                    for student in student_list:
                        # Add the current student's marks to the running total
                        total_marks += student["marks"]
                        # If the current student's marks are higher than our stored highest, replace it
                        if student["marks"] > highest_student["marks"]:
                            highest_student = student
                        # If the current student's marks are lower than our stored lowest, replace it
                        if student["marks"] < lowest_student["marks"]:
                            lowest_student = student
                            
                    # Calculate the average by dividing the sum by the count
                    average = total_marks / total_students
                    
                    # Print the final statistics
                    print(f"Total number of students: {total_students}")
                    # Print the average formatted to 2 decimal places using :.2f
                    print(f"Average marks: {average:.2f}")
                    # Print the highest/lowest marks and look up the name of the student who achieved it
                    print(f"Highest marks: {highest_student['marks']} ({highest_student['name']})")
                    print(f"Lowest marks: {lowest_student['marks']} ({lowest_student['name']})")

            # --- OPTION 7: Exit ---
            elif choice == "7":
                # Do one final save just to be safe
                data_handler.save_data(student_list)
                print("\nData saved. Exiting Student Management System. Goodbye!")
                # Break the main while True loop, ending the program
                break

            # --- Error Handling for Menu ---
            else:
                # If they typed anything other than 1-7, print an error and the loop will restart
                print("Invalid choice. Please enter a number between 1 and 7.")
                
    # If the user presses Ctrl+C at any point while the program is running, catch the interruption
    except KeyboardInterrupt:
        # Save the data to prevent corruption
        data_handler.save_data(student_list)
        # Print a clean exit message instead of a messy Python error trace
        print("\n\nProgram interrupted by user. Data saved. Exiting safely...")

# This special Python condition checks if this specific file was run directly (e.g., 'python main.py')
if __name__ == "__main__":
    # If it was run directly, trigger the main() function to start the app
    main()