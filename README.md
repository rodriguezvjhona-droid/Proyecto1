📚 Student Management System (Python)

📌 Description

This project is a Student Management System developed in Python.
It allows administrative users to manage student information through a simple console-based interface.

The system supports basic CRUD operations (Create, Read, Update, Delete) and uses Python data structures to store and manage the data efficiently.

🚀 Features
Register new students
View all students
Search students by ID or name
Update student information
Delete students
Store data using:
Lists
Dictionaries
Tuples
Console-based interactive menu
Modular design using functions
Basic error handling

⭐ Optional (Bonus)
Data persistence using .json, .csv, or .txt files
Load data when the program starts
Save data between executions

🛠️ Requirements

Python 3.x installed
▶️ How to Run the Program
Download or clone the repository
Open a terminal or command prompt
Navigate to the project folder
Run the program with:
python main.py

📋 Menu Example

When you run the program, you will see a menu like this:

===== STUDENT MANAGEMENT SYSTEM =====
1. Add Student
2. View Students
3. Search Student
4. Update Student
5. Delete Student
6. Exit
   
🧩 Data Structure Example

Each student is stored as a dictionary:

student = {
    "id": 101,
    "name": "John Doe",
    "age": 20,
    "course": "Software Development",
    "status": True
}

All students are stored in a list:

students = []
💡 Usage Examples
➤ Add a student
Enter ID: 101
Enter name: John Doe
Enter age: 20
Enter course: Software Development
Enter status (True/False): True
➤ Search a student
Enter student ID: 101
Student found: John Doe
➤ Update a student
Enter student ID to update: 101
Update name: John Smith
➤ Delete a student
Enter student ID to delete: 101
Student deleted successfully
⚠️ Error Handling

The system handles common errors such as:

Invalid input types
Student not found
Duplicate IDs

Using try-except blocks to prevent program crashes.

🧱 Project Structure
project/
│── main.py
│── functions.py
│── data.json (optional)
│── README.md
🧠 Concepts Used

Variables and data types (int, str, bool)
Conditional statements (if, elif, else)
Loops (for)
Functions with parameters and return values
Data structures:
Lists
Dictionaries
Tuples
Exception handling (try-except)

✅ Acceptance Criteria

The system runs correctly from the console
All CRUD operations work without errors
The program handles errors properly
Code is clean and well documented
The menu is clear and user-friendly

📎 Notes
Avoid using unnecessary while True loops
Keep code modular and organized
Use clear and meaningful comments
