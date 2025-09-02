
# Student Management System — Data Flow & Database Design (Python/MySQL)


## Database Tables (as implemented)


* **Authentication**
  * `Id INT AUTO_INCREMENT PRIMARY KEY`
  * `Username VARCHAR(50) UNIQUE`
  * `Password VARCHAR(100)`  -- (stored as plain text)
  * `Role VARCHAR(20)`  -- ('admin', 'student')


* **Classes**
  * `Class_Id INT AUTO_INCREMENT PRIMARY KEY`
  * `Level VARCHAR(10)`        -- 'SS1', 'SS2', 'SS3'
  * `Section VARCHAR(5)`      -- 'A', 'B', ...
  * `Academic_Year VARCHAR(20)`


* **Students**
  * `Id INT AUTO_INCREMENT PRIMARY KEY`
  * `Matric_No VARCHAR(20) UNIQUE`
  * `First_Name VARCHAR(50)`
  * `Middle_Name VARCHAR(50)`
  * `Last_Name VARCHAR(50)`
  * `Gender VARCHAR(10)`
  * `DOB DATE`
  * `Class_Id INT`  -- FK -> Classes(Class_Id)


* **Teachers**
  * `Id INT AUTO_INCREMENT PRIMARY KEY`
  * `First_Name VARCHAR(50)`
  * `Middle_Name VARCHAR(50)`
  * `Last_Name VARCHAR(50)`
  * `UserName VARCHAR(50) UNIQUE`
  * `Password VARCHAR(100)`
  * `Teachers_Id INT UNIQUE`  -- (custom teacher code)


* **Subjects**
  * `Id INT AUTO_INCREMENT PRIMARY KEY`
  * `Subject_Name VARCHAR(50)`
  * `Code VARCHAR(10)`
  * `Teachers_Id INT`  -- FK -> Teachers(Teachers_Id)
  * `Class_Id INT`     -- FK -> Classes(Class_Id)


* **Score**
  * `Id INT AUTO_INCREMENT PRIMARY KEY`
  * `Student_Id INT` -- FK -> Students(Id)
  * `Subject_Id INT` -- FK -> Subjects(Id)
  * `Teachers_Id INT` -- FK -> Teachers(Teachers_Id)
  * `Score INT`
  * `Session VARCHAR(20)`
  * `Timestamp DATETIME`


# Data Flow Overview

1. **Authentication**: User logs in (admin/student). Credentials checked in Authentication table.
2. **Admin Menu**: Admin can add/view students, teachers, classes, subjects, enter scores, and view best students.
3. **Student Menu**: Student can view their results and subjects.
4. **Class Management**: Classes are created with level, section, and academic year.
5. **Student Management**: Students are added with unique matric number and assigned to a class.
6. **Teacher Management**: Teachers are added with unique Teachers_Id and can be assigned to subjects.
7. **Subject Management**: Subjects are created and linked to both a class and a teacher (via Teachers_Id and Class_Id).
8. **Score Entry**: Scores are entered for students per subject, teacher, and session.
9. **Best Student Calculation**: For a selected class level, the system finds the student with the highest score per subject across all sections (A/B) of that level.
10. **Result Viewing**: Students and admins can view results, which show student name, level, subject, score, and session.

> Note: a single normalized `classes` table is preferred over creating separate tables per class (SS1, SS2, SS3). This makes queries and ranking logic easier. If your instructor insists on separate physical tables, we can generate views or separate tables, but normalization is best practice.

---


## Data Flow (Summary)

1. **Start** → **Login** (Authentication)
2. **Admin**: Can manage classes, students, teachers, subjects, enter scores, and view best students.
  - Adding/Viewing classes, students, teachers, and subjects updates the respective tables.
  - Entering scores updates the Score table.
  - Viewing best students queries Score, Students, Subjects, and Classes tables.
3. **Student**: Can view their results and subjects (with teacher info).
4. **All data is linked by foreign keys (Class_Id, Teachers_Id, Subject_Id, Student_Id) to ensure correct relationships and queries.**

---


## Notes on Result & Ranking Logic

* Scores are stored per (student, subject, session).
* All relationships are managed by foreign keys for data integrity.





