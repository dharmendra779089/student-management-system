# Define a class named Student to act as a blueprint for creating student objects
class Student:
    # The __init__ method automatically runs when a new Student object is created
    # It takes in the specific details (id, name, age, etc.) as parameters
    def __init__(self, student_id, name, age, gender, course, marks):
        # Assign the passed 'student_id' parameter to the object's own student_id attribute
        self.student_id = student_id
        # Assign the passed 'name' parameter to the object's own name attribute
        self.name = name
        # Assign the passed 'age' parameter to the object's own age attribute
        self.age = age
        # Assign the passed 'gender' parameter to the object's own gender attribute
        self.gender = gender
        # Assign the passed 'course' parameter to the object's own course attribute
        self.course = course
        # Assign the passed 'marks' parameter to the object's own marks attribute
        self.marks = marks

    # Define a method to convert the custom Student object into a standard Python dictionary
    # This is necessary because the JSON module cannot save custom objects directly
    def to_dict(self):
        # Return a dictionary where the keys are strings and the values are the object's attributes
        return {
            "student_id": self.student_id,
            "name": self.name,
            "age": self.age,
            "gender": self.gender,
            "course": self.course,
            "marks": self.marks
        }

    # Define a classmethod to construct a Student object directly from a dictionary
    # 'cls' refers to the Student class itself, allowing this to act as an alternative constructor
    # This is the OOP counterpart to to_dict() and follows the standard Python factory pattern
    @classmethod
    def from_dict(cls, data):
        """
        Create and return a Student instance from a plain dictionary.

        Args:
            data (dict): A dictionary containing all student fields.

        Returns:
            Student: A fully populated Student object.
        """
        # Pass each dictionary value as the matching constructor argument and return the new object
        return cls(
            student_id=data["student_id"],
            name=data["name"],
            age=data["age"],
            gender=data["gender"],
            course=data["course"],
            marks=data["marks"]
        )