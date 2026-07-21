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
    # Add grades for each student dynamically
    for s in students:
        s['grade'] = calculate_grade(s['marks'])
    return jsonify(students)

@app.route('/api/students', methods=['POST'])
def add_student():
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400

    student_id = data.get("student_id", "").strip()
    name = data.get("name", "").strip()
    age = data.get("age")
    gender = data.get("gender", "").strip()
    course = data.get("course", "").strip()
    marks = data.get("marks")

    # Validate inputs
    if not student_id or not name or not gender or not course:
        return jsonify({"error": "All fields are required"}), 400

    try:
        age = int(age)
        if age <= 0:
            return jsonify({"error": "Age must be greater than 0"}), 400
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid age. Must be a whole number"}), 400

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

    name = data.get("name", "").strip()
    age = data.get("age")
    course = data.get("course", "").strip()
    marks = data.get("marks")

    # Validate inputs
    if not name or not course:
        return jsonify({"error": "Name and Course are required"}), 400

    try:
        age = int(age)
        if age <= 0:
            return jsonify({"error": "Age must be greater than 0"}), 400
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid age"}), 400

    try:
        marks = float(marks)
        if not (0 <= marks <= 100):
            return jsonify({"error": "Marks must be between 0 and 100"}), 400
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid marks"}), 400

    student_list = data_handler.load_data()
    found = False
    for s in student_list:
        if s["student_id"] == student_id:
            s["name"] = name
            s["age"] = age
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
