import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QLabel, QTableWidget, QTableWidgetItem, QMessageBox, QInputDialog
from PyQt5.QtCore import Qt, pyqtSignal
import mysql.connector

db = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="12345",
    database="ssis2",
)


class Student:
    def __init__(self, student_id, name, gender, year_level, course_code):
        self.student_id = student_id
        self.name = name
        self.gender = gender
        self.year_level = year_level
        self.course_code = course_code


class Course:
    def __init__(self, course_code, name):
        self.course_code = course_code
        self.name = name


class StudentInformationSystem:
    def __init__(self):
        self.students = []
        self.courses = []

    def check_student_id(self, student_id):
        cursor = db.cursor()
        query = "SELECT student_id FROM student WHERE student_id = %s"
        cursor.execute(query, (student_id,))
        result = cursor.fetchone()
        if result:
            return True
        else:
            return False

    def add_student(self, student_id, name, gender, year_level, course_code):
        cursor = db.cursor()
        query = "INSERT INTO student (student_id, name, gender, year_level, course_code) VALUES (%s, %s, %s, %s, %s)"
        values = (student_id, name, gender, year_level, course_code)
        cursor.execute(query, values)
        db.commit()
        print("Student added successfully.")

    def delete_student(self, student_id):
        cursor = db.cursor()
        query = "DELETE FROM student WHERE student_id = %s"
        cursor.execute(query, (student_id,))
        db.commit()

        if cursor.rowcount > 0:
            print("Student deleted successfully.")
        else:
            print("Student not found.")

    def edit_student(self, student_id, name=None, gender=None, year_level=None, course_code=None):
        cursor = db.cursor()
        query = "SELECT * FROM student"
        cursor.execute(query)
        data = cursor.fetchall()
        for row in data:
            if row[0] == student_id:
                # Update the student's attributes
                if name:
                    query = "UPDATE student SET name = %s WHERE student_id = %s"
                    cursor.execute(query, (name, student_id))
                if gender:
                    query = "UPDATE student SET gender = %s WHERE student_id = %s"
                    cursor.execute(query, (gender, student_id))
                if year_level:
                    query = "UPDATE student SET year_level = %s WHERE student_id = %s"
                    cursor.execute(query, (year_level, student_id))
                if course_code:
                    query = "UPDATE student SET course_code = %s WHERE student_id = %s"
                    cursor.execute(query, (course_code, student_id))
                db.commit()
                print(f"Student with ID {student_id} has been edited.")
                return
        print(f"Student with ID {student_id} was not found.")

    def search_student(self, search_key):
        cursor = db.cursor()
        query = "SELECT * FROM student WHERE student_id LIKE %s OR name LIKE %s OR gender LIKE %s OR year_level LIKE %s OR course_code LIKE %s"
        values = (f"%{search_key}%", f"%{search_key}%", f"%{search_key}%", f"%{search_key}%", f"%{search_key}%")
        cursor.execute(query, values)
        data = cursor.fetchall()
        self.students = []
        for row in data:
            student = Student(row[0], row[1], row[2], row[3], row[4])
            self.students.append(student)

    def load_courses(self):
        cursor = db.cursor()
        query = "SELECT * FROM course"
        cursor.execute(query)
        data = cursor.fetchall()
        self.courses = []
        for row in data:
            course = Course(row[0], row[1])
            self.courses.append(course)

    def add_course(self, course_code, course_name):
        cursor = db.cursor()
        query = "INSERT INTO course (course_code, course_name) VALUES (%s, %s)"
        values = (course_code, course_name)
        cursor.execute(query, values)
        db.commit()
        print("Course added successfully.")

    def delete_course(self, course_code):
        cursor = db.cursor()
        query = "DELETE FROM course WHERE course_code = %s"
        cursor.execute(query, (course_code,))
        db.commit()

        if cursor.rowcount > 0:
            print("Course deleted successfully.")
        else:
            print("Course not found.")

    def edit_course(self, course_code, name=None):
        cursor = db.cursor()
        query = "SELECT * FROM course"
        cursor.execute(query)
        data = cursor.fetchall()
        for row in data:
            if row[0] == course_code:
                # Update the course's attributes
                if name:
                    query = "UPDATE course SET course_name = %s WHERE course_code = %s"
                    cursor.execute(query, (name, course_code))
                db.commit()
                print(f"Course with code {course_code} has been edited.")
                return
        print(f"Course with code {course_code} was not found.")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Information System")
        self.setGeometry(100, 100, 800, 600)
        self.setup_ui()
        self.show()

    def setup_ui(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        # Student UI
        self.student_layout = QHBoxLayout()

        self.student_id_label = QLabel("Student ID:")
        self.student_id_edit = QLineEdit()
        self.student_layout.addWidget(self.student_id_label)
        self.student_layout.addWidget(self.student_id_edit)

        self.name_label = QLabel("Name:")
        self.name_edit = QLineEdit()
        self.student_layout.addWidget(self.name_label)
        self.student_layout.addWidget(self.name_edit)

        self.gender_label = QLabel("Gender:")
        self.gender_edit = QLineEdit()
        self.student_layout.addWidget(self.gender_label)
        self.student_layout.addWidget(self.gender_edit)

        self.year_level_label = QLabel("Year Level:")
        self.year_level_edit = QLineEdit()
        self.student_layout.addWidget(self.year_level_label)
        self.student_layout.addWidget(self.year_level_edit)

        self.course_code_label = QLabel("Course Code:")
        self.course_code_edit = QLineEdit()
        self.student_layout.addWidget(self.course_code_label)
        self.student_layout.addWidget(self.course_code_edit)

        self.add_student_button = QPushButton("Add Student")
        self.add_student_button.clicked.connect(self.add_student)
        self.student_layout.addWidget(self.add_student_button)

        self.edit_student_button = QPushButton("Edit Student")
        self.edit_student_button.clicked.connect(self.edit_student)
        self.student_layout.addWidget(self.edit_student_button)

        self.delete_student_button = QPushButton("Delete Student")
        self.delete_student_button.clicked.connect(self.delete_student)
        self.student_layout.addWidget(self.delete_student_button)

        self.layout.addLayout(self.student_layout)

        self.search_layout = QHBoxLayout()

        self.search_label = QLabel("Search:")
        self.search_edit = QLineEdit()
        self.search_layout.addWidget(self.search_label)
        self.search_layout.addWidget(self.search_edit)

        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.search_students)
        self.search_layout.addWidget(self.search_button)

        self.layout.addLayout(self.search_layout)

        # Student Table
        self.student_table = QTableWidget()
        self.student_table.setColumnCount(5)
        self.student_table.setHorizontalHeaderLabels(["ID", "Name", "Gender", "Year Level", "Course Code"])
        self.layout.addWidget(self.student_table)

        # Course UI
        self.course_layout = QHBoxLayout()

        self.course_code_label = QLabel("Course Code:")
        self.course_code_edit = QLineEdit()
        self.course_layout.addWidget(self.course_code_label)
        self.course_layout.addWidget(self.course_code_edit)

        self.course_name_label = QLabel("Course Name:")
        self.course_name_edit = QLineEdit()
        self.course_layout.addWidget(self.course_name_label)
        self.course_layout.addWidget(self.course_name_edit)

        self.add_course_button = QPushButton("Add Course")
        self.add_course_button.clicked.connect(self.add_course)
        self.course_layout.addWidget(self.add_course_button)

        self.edit_course_button = QPushButton("Edit Course")
        self.edit_course_button.clicked.connect(self.edit_course)
        self.course_layout.addWidget(self.edit_course_button)

        self.delete_course_button = QPushButton("Delete Course")
        self.delete_course_button.clicked.connect(self.delete_course)
        self.course_layout.addWidget(self.delete_course_button)

        self.layout.addLayout(self.course_layout)

        # Course Table
        self.course_table = QTableWidget()
        self.course_table.setColumnCount(2)
        self.course_table.setHorizontalHeaderLabels(["Course Code", "Course Name"])
        self.layout.addWidget(self.course_table)

        # Load data
        self.load_data()

    def load_data(self):
        sis = StudentInformationSystem()
        sis.load_courses()
        sis.search_student("")
        students = sis.students
        courses = sis.courses

        # Populate Student Table
        self.student_table.setRowCount(len(students))
        for row, student in enumerate(students):
            self.student_table.setItem(row, 0, QTableWidgetItem(student.student_id))
            self.student_table.setItem(row, 1, QTableWidgetItem(student.name))
            self.student_table.setItem(row, 2, QTableWidgetItem(student.gender))
            year_level_item = QTableWidgetItem(str(student.year_level))
            self.student_table.setItem(row, 3, year_level_item)
            self.student_table.setItem(row, 4, QTableWidgetItem(student.course_code))

        # Populate Course Table
        self.course_table.setRowCount(len(courses))
        for row, course in enumerate(courses):
            self.course_table.setItem(row, 0, QTableWidgetItem(course.course_code))
            self.course_table.setItem(row, 1, QTableWidgetItem(course.name))

    def search_students(self):
        search_key = self.search_edit.text()
        sis = StudentInformationSystem()
        sis.search_student(search_key)
        students = sis.students

        # Clear the student table
        self.student_table.setRowCount(0)

        # Populate the student table with search results
        for row, student in enumerate(students):
            self.student_table.insertRow(row)
            self.student_table.setItem(row, 0, QTableWidgetItem(student.student_id))
            self.student_table.setItem(row, 1, QTableWidgetItem(student.name))
            self.student_table.setItem(row, 2, QTableWidgetItem(student.gender))
            year_level_item = QTableWidgetItem(str(student.year_level))
            self.student_table.setItem(row, 3, year_level_item)
            self.student_table.setItem(row, 4, QTableWidgetItem(student.course_code))

    def add_student(self):
        student_id = self.student_id_edit.text()
        name = self.name_edit.text()
        gender = self.gender_edit.text()
        year_level = self.year_level_edit.text()
        course_code = self.course_code_edit.text()

        sis = StudentInformationSystem()

        if not student_id or not name or not gender or not year_level or not course_code:
            QMessageBox.warning(self, "Error", "Please fill in all fields.")
        elif sis.check_student_id(student_id):
            QMessageBox.warning(self, "Error", "Student ID already exists.")
        else:
            sis.add_student(student_id, name, gender, year_level, course_code)
            self.load_data()
            self.clear_student_fields()

    def edit_student(self):
        student_id = self.student_id_edit.text()
        name = self.name_edit.text()
        gender = self.gender_edit.text()
        year_level = self.year_level_edit.text()
        course_code = self.course_code_edit.text()

        sis = StudentInformationSystem()

        if not student_id or not name or not gender or not year_level or not course_code:
            QMessageBox.warning(self, "Error", "Please fill in all fields.")
        elif not sis.check_student_id(student_id):
            QMessageBox.warning(self, "Error", "Student ID does not exist.")
        else:
            sis.edit_student(student_id, name, gender, year_level, course_code)
            self.load_data()
            self.clear_student_fields()

    def delete_student(self):
        student_id = self.student_id_edit.text()

        sis = StudentInformationSystem()

        if not student_id:
            QMessageBox.warning(self, "Error", "Please enter a student ID.")
        elif not sis.check_student_id(student_id):
            QMessageBox.warning(self, "Error", "Student ID does not exist.")
        else:
            sis.delete_student(student_id)
            self.load_data()
            self.clear_student_fields()

    def add_course(self):
        course_code = self.course_code_edit.text()
        course_name = self.course_name_edit.text()

        sis = StudentInformationSystem()

        if not course_code or not course_name:
            QMessageBox.warning(self, "Error", "Please fill in all fields.")
        else:
            sis.add_course(course_code, course_name)
            self.load_data()
            self.clear_course_fields()

    def edit_course(self):
        course_code = self.course_code_edit.text()
        course_name = self.course_name_edit.text()

        sis = StudentInformationSystem()

        if not course_code or not course_name:
            QMessageBox.warning(self, "Error", "Please fill in all fields.")
        else:
            sis.edit_course(course_code, course_name)
            self.load_data()
            self.clear_course_fields()

    def delete_course(self):
        course_code = self.course_code_edit.text()

        sis = StudentInformationSystem()

        if not course_code:
            QMessageBox.warning(self, "Error", "Please enter a course code.")
        else:
            sis.delete_course(course_code)
            self.load_data()
            self.clear_course_fields()

    def clear_student_fields(self):
        self.student_id_edit.clear()
        self.name_edit.clear()
        self.gender_edit.clear()
        self.year_level_edit.clear()
        self.course_code_edit.clear()

    def clear_course_fields(self):
        self.course_code_edit.clear()
        self.course_name_edit.clear()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
