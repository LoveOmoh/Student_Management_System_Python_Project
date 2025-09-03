# Student Management System (Python/MySQL)

## Project Overview
This Student Management System is built with Python and MySQL. It allows administrators and students to manage and view academic records, including classes, students, teachers, subjects, and scores. All data is stored in a normalized MySQL database for easy querying and integrity.

### Database Design
The system uses the following tables:
- **Authentication**: Stores user credentials and roles (admin/student).
- **Classes**: Contains class details (level, section, academic year).
- **Students**: Student records linked to classes.
- **Teachers**: Teacher records with unique IDs.
- **Subjects**: Subjects linked to classes and teachers.
- **Score**: Stores student scores per subject, teacher, and session.

### Data Flow
1. **Authentication**: Users log in as admin or student.
2. **Admin Menu**: Add/view students, teachers, classes, subjects, enter scores, view best students.
3. **Student Menu**: View results and subjects.
4. **Relationships**: All tables are linked by foreign keys for data integrity.

## Setup Instructions
1. **Clone the repository**
2. **Install dependencies**:
	```
	pip install -r requirements.txt
	```
3. **Configure MySQL**: Ensure you have a MySQL server running and update the connection details in `student_management.py` if needed.
4. **Create the database and tables**: Run the setup code in `database.py` (uncomment and execute the table creation code if not already done).
5. **Run the application**:
	```
	python student_management.py
	```

## Usage
- Admins can add/view classes, students, teachers, subjects, enter scores, and view best students.
- Students can log in to view their results and subjects.

## Notes
- All relationships are managed by foreign keys for data integrity.
- For best results, use a single normalized `Classes` table as described in the design.

---
For more details, see `design.md`.