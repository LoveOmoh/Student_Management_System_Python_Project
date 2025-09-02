import mysql.connector as db
import time   # for adding small delays in messages


def log_to_file(message):
    with open("log.txt", "a") as f:
        f.write(message + "\n")


# ----------------- CLASS MANAGEMENT -----------------
def add_class(level, section, academic_year):
    """Add a new class"""
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO Classes (Level, Section, Academic_Year) VALUES (%s, %s, %s)", 
                (level, section, academic_year))
    conn.commit()
    print("Class added successfully!")
    conn.close()


# ----------------- DATABASE CONNECTION -----------------

def connect_db():
    """Helper function to connect to MySQL Database"""
    return db.connect(
        host="localhost",
        user="root",
        password="Gboyega2*",
        database="Student_Management_System",
        auth_plugin="mysql_native_password"
    )


# ----------------- AUTHENTICATION -----------------

def signup(username, password, role):
    """Register a new user (admin or student)"""
    conn = connect_db()
    cur = conn.cursor()

    try:
        # Store plain password 
        if len(password) > 8:
            print("Password is too long! Must be 8 characters or fewer")
            conn.close()
        else:
            cur.execute("INSERT INTO Authentication (Username, Password, Role) VALUES (%s, %s, %s)",
                        (username, password, role))
            conn.commit()
            print("Signup successful!")
    except db.Error as e:
        print("Error during signup:", e)

    conn.close()


def login(username, password):
    """Login function for both admin and student"""
    conn = connect_db()
    cur = conn.cursor()

    cur.execute("SELECT Password, Role FROM Authentication WHERE Username = %s", (username,))
    result = cur.fetchone()

    if result and result[0] == password:   # compare directly
        print(f"\nLogin successful! Welcome, {username}. Role: {result[1]}")
        role = result[1]
    else:
        print("Invalid username or password.")
        role = None

    conn.close()
    return role


# ----------------- STUDENT MANAGEMENT -----------------

def add_student(matric_no, fname, mname, lname, gender, dob, class_id):
    """Add a new student record"""

    conn = connect_db()
    cur = conn.cursor()

    # Ensure Matric No is unique
    cur.execute("SELECT Matric_No FROM Students WHERE Matric_No = %s", (matric_no,))
    if cur.fetchone():
        print("Matric number already exists!")
        conn.close()
        return

    # Check if Class_Id exists
    while True:
        cur.execute("SELECT Class_Id FROM Classes WHERE Class_Id = %s", (class_id,))
        result = cur.fetchone()
        if result:
            break
        else:
            print(f"Class ID {class_id} does not exist. Please enter a valid Class ID.")
            class_id = input("Class ID: ")

    cur.execute("""INSERT INTO Students (Matric_No, First_Name, Middle_Name, Last_Name, Gender, DOB, Class_Id)
                   VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                   (matric_no, fname, mname, lname, gender, dob, class_id))
    conn.commit()

    print("Student added successfully!")
    log_to_file(f"Added student: {matric_no}, {fname} {mname} {lname}, Gender: {gender}, DOB: {dob}, Class ID: {class_id}")

    conn.close()


def view_students():
    """Display all students"""
    conn = connect_db()
    cur = conn.cursor()

    cur.execute("SELECT * FROM Students")
    students = cur.fetchall()

    print("\n--- All Students ---")
    for s in students:
        print(s)

    conn.close()


# ----------------- TEACHER MANAGEMENT -----------------

def add_teacher(fname, mname, lname, username, password, teachers_id):
    """Add new teacher"""
    conn = connect_db()
    cur = conn.cursor()

    cur.execute("""INSERT INTO Teachers (First_Name, Middle_Name, Last_Name, UserName, Password, Teachers_Id)
                   VALUES (%s, %s, %s, %s, %s, %s)""",
                   (fname, mname, lname, username, password, teachers_id))
    conn.commit()

    print("Teacher added successfully!")
    log_to_file(f"Added teacher: {teachers_id}, {fname} {mname} {lname}, Username: {username}")

    conn.close()


def view_teachers():
    """Show all teachers"""
    conn = connect_db()
    cur = conn.cursor()

    cur.execute("SELECT * FROM Teachers")
    teachers = cur.fetchall()

    print("\n--- All Teachers ---")
    for t in teachers:
        print(t)

    conn.close()


# ----------------- SUBJECT MANAGEMENT -----------------

def add_subject(name, code, teachers_id, class_id):
    """Add a new subject"""
    conn = connect_db()
    cur = conn.cursor()

    cur.execute("""INSERT INTO Subjects (Subject_Name, Code, Teachers_Id, Class_Id) 
                   VALUES (%s, %s, %s, %s)""", (name, code, teachers_id, class_id))
    conn.commit()

    print("Subject added successfully!")
    log_to_file(f"Added subject: {name}, Code: {code}, Teacher ID: {teachers_id}, Class ID: {class_id}")

    conn.close()


def view_subjects():
    """View all subjects"""
    conn = connect_db()
    cur = conn.cursor()

    cur.execute("""SELECT Subjects.Id, Subjects.Subject_Name, Subjects.Code, 
                          Teachers.Id, Teachers.First_Name, Teachers.Last_Name, 
                          Classes.Level, Classes.Section
                   FROM Subjects
                   LEFT JOIN Teachers ON Subjects.Teachers_Id = Teachers_code
                   LEFT JOIN Classes ON Subjects.Class_Id = Classes.Class_Id""")
    subjects = cur.fetchall()

    print("\n--- Subjects ---")
    for sub in subjects:
        (subj_id, subj_name, code, teacher_id, teacher_fname, teacher_lname, class_level, class_section) = sub
        teacher_info = f"{teacher_fname} {teacher_lname}" if teacher_id is not None else "No teacher assigned"
        class_info = f"{class_level} {class_section}" if class_level is not None and class_section is not None else "No class assigned"
        print(f"ID: {subj_id}, Name: {subj_name}, Code: {code}, Teacher: {teacher_info}, Class: {class_info}")

    conn.close()


# ----------------- SCORES / RESULTS -----------------

def add_score(student_id, subject_id, teachers_id, score, session):
    """Teacher enters student score"""
    conn = connect_db()
    cur = conn.cursor()

    cur.execute("""INSERT INTO Score (Student_Id, Subject_Id, Teachers_Id, Score, Session)
                   VALUES (%s, %s, %s, %s, %s)""",
                   (student_id, subject_id, teachers_id, score, session))
    conn.commit()

    print("Score added successfully!")
    log_to_file(f"Added score: Student ID {student_id}, Subject ID {subject_id}, Teacher ID {teachers_id}, Score {score}, Session {session}")

    conn.close()


def view_results(student_id):
    """View results of a student"""
    conn = connect_db()
    cur = conn.cursor()

    cur.execute("""SELECT Students.First_Name, Students.Middle_Name, Students.Last_Name, Classes.Level,
                          Subjects.Subject_Name, Score.Score, Score.Session
                   FROM Score
                   JOIN Students ON Score.Student_Id = Students.Id
                   JOIN Classes ON Students.Class_Id = Classes.Class_Id
                   JOIN Subjects ON Score.Subject_Id = Subjects.Id
                   WHERE Score.Student_Id = %s""", (student_id,))
    results = cur.fetchall()

    if results:
        print(f"\nResults for {results[0][0]} {results[0][1]} {results[0][2]} | Level: {results[0][3]}")
        for r in results:
            print(f"Subject: {r[4]}, Score: {r[5]}, Session: {r[6]}")
    else:
        print("No results found.")

    conn.close()


def best_student():
    """Find overall best student based on average score"""
    class_level = input("Enter class level (SS1/SS2/SS3): ").strip().upper()
    conn = connect_db()
    cur = conn.cursor()

    # Get all subjects for the selected class
    cur.execute("""
        SELECT DISTINCT Subjects.Id, Subjects.Subject_Name
        FROM Subjects
        JOIN Classes ON Subjects.Class_Id = Classes.Class_Id
        WHERE Classes.Level = %s
    """, (class_level,))
    subjects = cur.fetchall()

    if not subjects:
        print(f"No subjects found for class {class_level}.")
        conn.close()
        return

    for subject_id, subject_name in subjects:
        cur.execute("""
            SELECT Students.First_Name, Students.Last_Name, MAX(Score.Score) as MaxScore
            FROM Score
            JOIN Students ON Score.Student_Id = Students.Id
            WHERE Score.Subject_Id = %s AND Students.Class_Id IN (
                SELECT Class_Id FROM Classes WHERE Level = %s
            )
            GROUP BY Students.Id, Score.Subject_Id
            ORDER BY MaxScore DESC
        """, (subject_id, class_level))
        all_students = cur.fetchall()
        if all_students:
            best = all_students[0]
            print(f"Best Student for {subject_name} in {class_level}: {best[0]} {best[1]} with Highest Score {best[2]:.2f}")
        else:
            print(f"No scores available for {subject_name} in {class_level}.")

    conn.close()


# ----------------- MENUS -----------------

def admin_menu():
    """Admin menu for managing system"""
    while True:
        print("\n===== ADMIN MENU =====")
        print("1. Add Student")
        print("2. View Students")
        print("3. Add Teacher")
        print("4. View Teachers")
        print("5. Add Subject")
        print("6. View Subjects")
        print("7. Add Class(Adding class is mandatory before you can add students and teachers to that class)")
        print("8. Add Score")
        print("9. Best Student")
        print("10. Logout")

        choice = input("Enter choice: ")

        if choice == "1":
            matric = input("Matric No: ")
            fname = input("First Name: ")
            mname = input("Middle Name: ")
            lname = input("Last Name: ")
            gender = input("Gender (Male/Female): ")
            dob = input("Date of Birth (YYYY-MM-DD): ")
            class_id = input("Class ID: ")
            add_student(matric, fname, mname, lname, gender, dob, class_id)

        elif choice == "2":
            view_students()

        elif choice == "3":
            fname = input("First Name: ")
            mname = input("Middle Name: ")
            lname = input("Last Name: ")
            username = input("Username: ")
            password = input("Password: ")
            teachers_id = input("Teacher ID: ")
            add_teacher(fname, mname, lname, username, password, teachers_id)

        elif choice == "4":
            view_teachers()

        elif choice == "5":
            name = input("Subject Name: ")
            code = input("Subject Code: ")
            teachers_id = input("Teacher ID: ")
            class_id = input("Class ID: ")
            add_subject(name, code, teachers_id, class_id)

        elif choice == "6":
            view_subjects()

        elif choice == "7":
            level = input("Class Level (SS1/SS2/SS3): ")
            section = input("Section: ")
            academic_year = input("Academic Year: ")
            add_class(level, section, academic_year)

        elif choice == "8":
            student_id = input("Student ID: ")
            subject_id = input("Subject ID: ")
            teachers_id = input("Teacher ID: ")
            score = input("Score: ")
            session = input("Session: ")
            add_score(student_id, subject_id, teachers_id, score, session)

        elif choice == "9":
            best_student()

        elif choice == "10":
            print("Logging out....")
            return  # go back to main menu

        else:
            print("Invalid choice, try again.")


def student_menu(username):
    """Student menu (limited access)"""
    while True:
        print("\n===== STUDENT MENU =====")
        print("1. View Results")
        print("2. View Subjects")
        print("3. Logout")

        choice = input("Enter choice: ")

        if choice == "1":
            student_id = input("Enter your Student ID: ")
            view_results(student_id)

        elif choice == "2":
            view_subjects()
            

        elif choice == "3":
            print("Logging out....")
            return

        else:
            print("Invalid choice, try again.")


def main():
    """Main entry point"""
    while True:
        print("\n===== STUDENT MANAGEMENT SYSTEM =====")
        print("1. Signup")
        print("2. Login")
        print("3. Exit")
        choice = input("Enter choice: ")

        if choice == "1":
            username = input("Enter username: ")
            password = input("Enter password: ")
            role = input("Enter role (admin/student): ")
            signup(username, password, role)

        elif choice == "2":
            username = input("Enter username: ")
            password = input("Enter password: ")
            role = login(username, password)

            if role == "admin":
                admin_menu()
            elif role == "student":
                student_menu(username)

        elif choice == "3":
            print("Exiting system...")
            break

        else:
            print("Invalid choice. Try again.")


# ----------------- RUN SYSTEM -----------------
if __name__ == "__main__":
    main()