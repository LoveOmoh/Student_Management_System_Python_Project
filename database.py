# import mysql.connector as db

# # Connecting to MySQL
# sms = db.connect(
#     host="localhost",
#     user="root",       
#     password="Gboyega2*",
#     database="Student_Management_System",
#     auth_plugin="mysql_native_password"
# )

# cursor = sms.cursor()

# Creating Database
# # cursor.execute("CREATE DATABASE Student_Management_System")
# print("Database Created")

# Creating Tables
# # Classes Table
# cursor.execute("""CREATE TABLE  Classes (
#                 Class_Id INT AUTO_INCREMENT PRIMARY KEY,
#                 Level ENUM('SS1', 'SS2', 'SS3'),
#                 Section VARCHAR(5),
#                 Academic_Year VARCHAR(20)
#                 )
#                 """)

# # Students table
# cursor.execute("""CREATE TABLE Students (
#                 Id INT AUTO_INCREMENT PRIMARY KEY,
#                 Matric_No VARCHAR(20) UNIQUE,
#                 First_Name VARCHAR(20),
#                 Last_Name VARCHAR(20),
#                 Middle_Name VARCHAR(20),
#                 Gender ENUM('Male', 'Female'),
#                 DOB DATE,
#                 Class_Id INT,
#                 FOREIGN KEY (Class_Id) REFERENCES Classes(Class_Id) ON DELETE SET NULL
#                 )
#                 """)

# # Teachers table
# cursor.execute("""CREATE TABLE Teachers (
#                 Id INT AUTO_INCREMENT PRIMARY KEY,
#                 First_Name VARCHAR(20),
#                 Last_Name VARCHAR(20),
#                 Middle_Name VARCHAR(20),
#                 UserName VARCHAR(50) UNIQUE,
#                 Password VARCHAR(10)
#                 )
#                 """)

# # Subjects table
# cursor.execute("""CREATE TABLE Subjects (
#                 Id INT AUTO_INCREMENT PRIMARY KEY,
#                 Subject_Name VARCHAR(50),
#                 Code VARCHAR(10)
#                 )
#                 """)


# # Score table
# cursor.execute("""CREATE TABLE  Score (
#                 Id INT AUTO_INCREMENT PRIMARY KEY,
#                 Student_Id INT,
#                 Subject_Id INT,
#                 Teacher_Id INT,
#                 Score INT,
#                 Term ENUM('First', 'Second', 'Third'),
#                 Session VARCHAR(20),
#                 Timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#                 FOREIGN KEY (Student_Id) REFERENCES Students(Id) ON DELETE CASCADE,
#                 FOREIGN KEY (Subject_Id) REFERENCES Subjects(Id) ON DELETE CASCADE,
#                 FOREIGN KEY (Teacher_Id) REFERENCES Teachers(Id) ON DELETE CASCADE
#                 )
#                 """)

# print("Database tables created successfully")

# Closing connection
# cursor.close()
# sms.close()
