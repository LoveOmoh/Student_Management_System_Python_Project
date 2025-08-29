# ----------------- CLASS MANAGEMENT -----------------
def add_class(level, section, academic_year):
    """Add a new class"""
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO Classes (Level, Section, Academic_Year) VALUES (%s, %s, %s)", (level, section, academic_year))
    conn.commit()
    print("Class added successfully!")
    conn.close()
import mysql.connector as db
import hashlib
import time   # for adding small delays in messages


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


# ----------------- UTILITY -----------------

def hash_password(password):
    """Convert plain password into SHA256 hash"""
    return hashlib.sha256(password.encode()).hexdigest()


# ----------------- AUTHENTICATION -----------------

def signup(username, password, role):
    """Register a new user (admin or student)"""
    conn = connect_db()
    cur = conn.cursor()

    try:
        cur.execute("INSERT INTO Authentication (Username, Password, Role) VALUES (%s, %s, %s)",
                    (username, hash_password(password), role))
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

    if result and result[0] == hash_password(password):
        print(f"\nLogin successful! Welcome, {username}. Role: {result[1]}")
        role = result[1]
    else:
        print("Invalid username or password.")
        role = None

    conn.close()
    return role


# ----------------- STUDENT MANAGEMENT -----------------

def add_student(matric_no, fname, lname, gender, dob, class_id):
    """Add a new student record"""

    conn = connect_db()
    cur = conn.cursor()

    # Check if Class_Id exists
    while True:
        cur.execute("SELECT Class_Id FROM Classes WHERE Class_Id = %s", (class_id,))
        result = cur.fetchone()
        if result:
            break
        else:
            print(f"Class ID {class_id} does not exist. Please enter a valid Class ID.")
            class_id = input("Class ID: ")

    cur.execute("""INSERT INTO Students (Matric_No, First_Name, Last_Name, Gender, DOB, Class_Id)
                   VALUES (%s, %s, %s, %s, %s, %s)""",
                   (matric_no, fname, lname, gender, dob, class_id))
    conn.commit()
    print("Student added successfully!")

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

def add_teacher(fname, lname, username, password):
    """Add new teacher"""
    conn = connect_db()
    cur = conn.cursor()

    cur.execute("""INSERT INTO Teachers (First_Name, Last_Name, UserName, Password)
                   VALUES (%s, %s, %s, %s)""",
                   (fname, lname, username, password))
    conn.commit()
    print("Teacher added successfully!")

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

def add_subject(name, code):
    """Add a new subject"""
    conn = connect_db()
    cur = conn.cursor()

    cur.execute("INSERT INTO Subjects (Subject_Name, Code) VALUES (%s, %s)", (name, code))
    conn.commit()
    print("Subject added successfully!")

    conn.close()


def view_subjects():
    """View all subjects"""
    conn = connect_db()
    cur = conn.cursor()

    cur.execute("SELECT * FROM Subjects")
    subjects = cur.fetchall()

    print("\n--- Subjects ---")
    for sub in subjects:
        print(sub)

    conn.close()


# ----------------- SCORES / RESULTS -----------------

def add_score(student_id, subject_id, teacher_id, score, term, session):
    """Teacher enters student score"""
    conn = connect_db()
    cur = conn.cursor()

    cur.execute("""INSERT INTO Score (Student_Id, Subject_Id, Teacher_Id, Score, Term, Session)
                   VALUES (%s, %s, %s, %s, %s, %s)""",
                   (student_id, subject_id, teacher_id, score, term, session))
    conn.commit()
    print("Score added successfully!")

    conn.close()


def view_results(student_id):
    """View results of a student"""
    conn = connect_db()
    cur = conn.cursor()

    cur.execute("""SELECT Subjects.Subject_Name, Score.Score, Score.Term, Score.Session
                   FROM Score
                   JOIN Subjects ON Score.Subject_Id = Subjects.Id
                   WHERE Score.Student_Id = %s""", (student_id,))
    results = cur.fetchall()

    print("\n--- Results ---")
    for r in results:
        print(r)

    conn.close()


def best_student():
    """Find overall best student based on average score"""
    conn = connect_db()
    cur = conn.cursor()

    cur.execute("""SELECT Students.First_Name, Students.Last_Name, AVG(Score.Score) as AvgScore
                   FROM Score
                   JOIN Students ON Score.Student_Id = Students.Id
                   GROUP BY Students.Id
                   ORDER BY AvgScore DESC
                   LIMIT 1""")
    best = cur.fetchone()

    if best:
        print(f"\nBest Student: {best[0]} {best[1]} with Average Score {best[2]:.2f}")
    else:
        print("No scores available yet.")

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
        print("7. Add Class (You must add class before you can add students and teachers to that class)")
        print("8. Add Score")
        print("9. Best Student")
        print("10. Logout")

        choice = input("Enter choice: ")

        if choice == "1":
            matric = input("Matric No: ")
            fname = input("First Name: ")
            lname = input("Last Name: ")
            gender = input("Gender (Male/Female): ")
            dob = input("Date of Birth (YYYY-MM-DD): ")
            class_id = input("Class ID: ")
            add_student(matric, fname, lname, gender, dob, class_id)

        elif choice == "2":
            view_students()

        elif choice == "3":
            fname = input("First Name: ")
            lname = input("Last Name: ")
            username = input("Username: ")
            password = input("Password: ")
            add_teacher(fname, lname, username, password)

        elif choice == "4":
            view_teachers()

        elif choice == "5":
            name = input("Subject Name: ")
            code = input("Subject Code: ")
            add_subject(name, code)

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
            teacher_id = input("Teacher ID: ")
            score = input("Score: ")
            session = input("Session: ")
            add_score(student_id, subject_id, teacher_id, score, session)

        elif choice == "9":
            best_student()

        elif choice == "10":
            print("Logging out...")
            break

        else:
            print("Invalid choice, try again.")
            add_class(level, section, academic_year)

def student_menu(username):
    """Student menu (limited access)"""
    while True:
        print("\n===== STUDENT MENU =====")
        print("1. View Results")
        print("2. Logout")

        choice = input("Enter choice: ")

        if choice == "1":
            student_id = input("Enter your Student ID: ")
            view_results(student_id)

        elif choice == "2":
            print("Logging out...")
            break

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
