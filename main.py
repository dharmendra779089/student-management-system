# Import the custom data_handler module we created to handle file saving/loading
import data_handler
# Import the Student class from our custom student.py module
from student import Student

# --- Helper Functions for Validation ---

# Define a function to ensure the user types something for text fields
def get_valid_name(prompt):
    # Start an infinite loop that will only break when valid data is returned
    while True:
        # Ask for input using the provided prompt, and use .strip() to remove accidental spaces at the beginning/end
        name = input(prompt).strip()
        # Check if the name variable actually contains characters (is not empty)
        if name:
            # If it is valid, return the name (this automatically breaks the loop)
            return name
        # If the input was empty, print an error and let the loop repeat
        print("Error: Name cannot be empty.")

# Define a function to ensure the user enters a valid, positive whole number for Age
def get_valid_age():
    # Start an infinite loop for validation
    while True:
        # Start a try block to catch errors if the user types letters instead of numbers
        try:
            # Ask for input, attempt to convert it to an integer (int), and store it in 'age'
            age = int(input("Enter Age: "))
            # Check if the entered integer is logically valid (greater than 0)
            if age > 0:
                # If valid, return the age to the main program (breaking the loop)
                return age
            # If the number is 0 or negative, print an error
            print("Error: Age must be greater than 0.")
        # Catch the specific error that happens if int() fails (e.g., user typed "twenty")
        except ValueError:
            # Print a friendly error message and let the loop repeat
            print("Invalid input. Please enter a whole number.")

# Define a function to ensure the user enters a valid number between 0 and 100 for Marks
def get_valid_marks():
    # Start an infinite loop for validation
    while True:
        # Start a try block to catch text-to-number conversion errors
        try:
            # Ask for input, convert to float (allows decimals like 85.5), and store it
            marks = float(input("Enter Marks (0-100): "))
            # Check if the number falls within the logically valid range of 0 to 100
            if 0 <= marks <= 100:
                # If valid, return the marks
                return marks
            # If outside the range, print an error
            print("Error: Marks must be between 0 and 100.")
        # Catch the error if the user types letters instead of numbers
        except ValueError:
            # Print an error and repeat the loop
            print("Invalid input. Please enter a valid number.")

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
                # Ask for the student ID, validating that it is neither empty nor a duplicate
                while True:
                    student_id = input("Enter Student ID: ").strip()
                    if not student_id:
                        print("Error: Student ID cannot be empty.")
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
                    # Loop through every dictionary in the student_list
                    for student in student_list:
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
                        # Overwrite the existing dictionary values using our helper functions
                        # Notice we do NOT update the ID, per the requirements
                        student["name"] = get_valid_name("Enter new Name: ")
                        student["age"] = get_valid_age()
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