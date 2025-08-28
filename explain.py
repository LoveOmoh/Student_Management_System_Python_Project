
import sqlite3, hashlib   # Importing the sqlite3 module (for database operations) 
                          # and hashlib (for password hashing).

def hash_password(password):                  # Define a function to hash the password before saving it
    return hashlib.sha256(password.encode()).hexdigest()  
    # hashlib.sha256() creates a secure hash using SHA-256.
    # password.encode() converts the password string into bytes (required for hashing).
    # hexdigest() converts the hash object into a readable hexadecimal string.

def signup(username, password, role):         # Define a signup function with username, password, and role as inputs.
    conn = sqlite3.connect("school.db")       # Connect to the SQLite database "school.db" (creates it if it doesn’t exist).
    cur = conn.cursor()                       # Create a cursor object to execute SQL commands.

    try:                                      # Try block to handle errors like duplicate usernames.
        cur.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",  
                    (username, hash_password(password), role))  
        # Run an SQL INSERT query to add a new user into the "users" table.
        # '?' placeholders are used to prevent SQL injection attacks.
        # The values inserted are: username, the hashed version of the password, and role.

        conn.commit()                         # Save (commit) the changes to the database.
        print("Signup successful!")           # Inform the user that signup worked.
    except sqlite3.IntegrityError:            # This error happens if the username already exists (unique constraint).
        print("Username already exists.")     # Tell the user the signup failed because the username is taken.
    conn.close()                              # Close the database connection to free resources.


import sqlite3, hashlib   # Importing the sqlite3 module for database interaction 
                          # and hashlib for securely hashing passwords.

def hash_password(password):  
    return hashlib.sha256(password.encode()).hexdigest()  
    # This function converts the plain password into a SHA-256 hash
    # so that the actual password is never stored in the database directly.

def login(username, password):  
    conn = sqlite3.connect("school.db")  
    # Connect to the SQLite database file named 'school.db'.  
    # If the file does not exist, it will be created automatically.  

    cur = conn.cursor()  
    # Create a cursor object to execute SQL queries on the database.  

    cur.execute("SELECT password, role FROM users WHERE username = ?", (username,))  
    # SQL query: Selects the password and role for the user with the given username.  
    # The `?` placeholder prevents SQL injection attacks.  
    # (username,) ensures it is passed as a tuple.  

    result = cur.fetchone()  
    # Fetch the first row returned from the query.  
    # It will return `None` if no user with that username exists.  

    if result and result[0] == hash_password(password):  
        # Check if a user was found (`result` is not None)  
        # AND if the stored hashed password matches the hashed input password.  

        print(f"Login successful! Welcome, {username}. Role: {result[1]}")  
        # If the password matches, print a success message along with the user's role.  

    else:  
        print("Invalid username or password.")  
        # If no user is found or the password doesn’t match, print an error message.  

    conn.close()  
    # Close the database connection to free up resources.  
