from flask import Flask, jsonify, request, render_template
import os
import data_handler
from student import Student

app = Flask(__name__)

# Ensure paths match standard Flask structures
# By default, Flask uses templates/ and static/ directories next to the app.py file

def calculate_grade(marks):
    if marks >= 90: return 'A'
    elif marks >= 80: return 'B'
    elif marks >= 70: return 'C'
    elif marks >= 60: return 'D'
    else: return 'F'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/students', methods=['GET'])
def get_students():
    students = data_handler.load_data()
    # Sort students by student_id from least to max (ascending)
    def get_id_key(s):
        try:
            return int(s.get("student_id", 0))
        except (ValueError, TypeError):
            return 999999
    students.sort(key=get_id_key)
    # Add grades for each student dynamically
    for s in students:
        s['grade'] = calculate_grade(s['marks'])
    return jsonify(students)

def get_next_available_id(student_list):
    used_ids = {int(s["student_id"]) for s in student_list if str(s.get("student_id", "")).isdigit()}
    for candidate in range(100, 1000):
        if candidate not in used_ids:
            return str(candidate)
    return "100"

@app.route('/api/students', methods=['POST'])
def add_student():
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400

    student_list = data_handler.load_data()
    student_id = data.get("student_id", "").strip()
    if not student_id:
        student_id = get_next_available_id(student_list)

    name = data.get("name", "").strip()
    age = data.get("age")
    gender = data.get("gender", "").strip()
    course = data.get("course", "").strip()
    marks = data.get("marks")

    # Validate inputs
    if not name or not gender or not course:
        return jsonify({"error": "Name, Gender, and Course are required"}), 400

    try:
        id_num = int(student_id)
        if not (100 <= id_num <= 999):
            return jsonify({"error": "Student ID must be a whole number from 100 to 999"}), 400
        student_id = str(id_num)
    except (ValueError, TypeError):
        return jsonify({"error": "Student ID must be a whole number from 100 to 999"}), 400

    try:
        age_float = float(age)
        if not age_float.is_integer():
            return jsonify({"error": "Invalid age. Must be a whole number"}), 400
        age = int(age_float)
        if not (0 <= age <= 100):
            return jsonify({"error": "Age must be a whole number between 0 and 100"}), 400
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid age. Must be a whole number between 0 and 100"}), 400

    try:
        marks = float(marks)
        if not (0 <= marks <= 100):
            return jsonify({"error": "Marks must be between 0 and 100"}), 400
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid marks. Must be a number between 0 and 100"}), 400

    # Gender standardisation
    gender_lower = gender.lower()
    if gender_lower in ["m", "male"]:
        gender = "Male"
    elif gender_lower in ["f", "female"]:
        gender = "Female"
    elif gender_lower in ["o", "other"]:
        gender = "Other"
    else:
        return jsonify({"error": "Invalid Gender. Choose Male, Female, or Other"}), 400

    # Check uniqueness of ID
    student_list = data_handler.load_data()
    for s in student_list:
        if s["student_id"] == student_id:
            return jsonify({"error": f"Student with ID '{student_id}' already exists"}), 409

    # Create new student and save
    new_student = Student(student_id, name, age, gender, course, marks)
    student_list.append(new_student.to_dict())
    data_handler.save_data(student_list)

    result = new_student.to_dict()
    result['grade'] = calculate_grade(marks)
    return jsonify(result), 201

@app.route('/api/students/<student_id>', methods=['PUT'])
def update_student(student_id):
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400

    new_student_id = data.get("student_id", student_id).strip()
    name = data.get("name", "").strip()
    age = data.get("age")
    gender = data.get("gender", "").strip()
    course = data.get("course", "").strip()
    marks = data.get("marks")

    # Validate inputs
    if not new_student_id or not name or not course:
        return jsonify({"error": "Student ID, Name, and Course are required"}), 400

    # Validate new student ID if changed or provided
    try:
        id_num = int(new_student_id)
        if not (100 <= id_num <= 999):
            return jsonify({"error": "Student ID must be a whole number from 100 to 999"}), 400
        new_student_id = str(id_num)
    except (ValueError, TypeError):
        return jsonify({"error": "Student ID must be a whole number from 100 to 999"}), 400

    try:
        age_float = float(age)
        if not age_float.is_integer():
            return jsonify({"error": "Invalid age. Must be a whole number"}), 400
        age = int(age_float)
        if not (0 <= age <= 100):
            return jsonify({"error": "Age must be a whole number between 0 and 100"}), 400
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid age. Must be a whole number between 0 and 100"}), 400

    try:
        marks = float(marks)
        if not (0 <= marks <= 100):
            return jsonify({"error": "Marks must be between 0 and 100"}), 400
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid marks"}), 400

    # Gender standardisation if provided
    if gender:
        gender_lower = gender.lower()
        if gender_lower in ["m", "male"]:
            gender = "Male"
        elif gender_lower in ["f", "female"]:
            gender = "Female"
        elif gender_lower in ["o", "other"]:
            gender = "Other"
        else:
            return jsonify({"error": "Invalid Gender. Choose Male, Female, or Other"}), 400

    student_list = data_handler.load_data()

    # Check ID collision if changing ID to another student's ID
    if new_student_id != student_id:
        for s in student_list:
            if s["student_id"] == new_student_id:
                return jsonify({"error": f"Student with ID '{new_student_id}' already exists"}), 409

    found = False
    for s in student_list:
        if s["student_id"] == student_id:
            s["student_id"] = new_student_id
            s["name"] = name
            s["age"] = age
            if gender:
                s["gender"] = gender
            s["course"] = course
            s["marks"] = marks
            found = True
            break

    if not found:
        return jsonify({"error": "Student not found"}), 404

    data_handler.save_data(student_list)
    return jsonify({"success": True})

@app.route('/api/students/<student_id>', methods=['DELETE'])
def delete_student(student_id):
    student_list = data_handler.load_data()
    initial_length = len(student_list)
    student_list = [s for s in student_list if s["student_id"] != student_id]

    if len(student_list) == initial_length:
        return jsonify({"error": "Student not found"}), 404

    data_handler.save_data(student_list)
    return jsonify({"success": True})

@app.route('/api/stats', methods=['GET'])
def get_stats():
    students = data_handler.load_data()
    if not students:
        return jsonify({
            "total_students": 0,
            "average_marks": 0.0,
            "highest_student": None,
            "lowest_student": None
        })

    total_students = len(students)
    marks_list = [s["marks"] for s in students]
    average_marks = round(sum(marks_list) / total_students, 2)

    # Find highest and lowest achievers
    highest_student = max(students, key=lambda s: s["marks"])
    lowest_student = min(students, key=lambda s: s["marks"])

    return jsonify({
        "total_students": total_students,
        "average_marks": average_marks,
        "highest_student": highest_student,
        "lowest_student": lowest_student
    })

if __name__ == '__main__':
    # Run server locally on port 5000
    app.run(debug=True, port=5000)
