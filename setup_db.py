import mysql.connector
from mysql.connector import Error

def create_database():
    try:
        # Connect to MySQL server (no database selected yet)
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Gauri@2006"
        )
        if conn.is_connected():
            cursor = conn.cursor()
            
            # Create database
            cursor.execute("CREATE DATABASE IF NOT EXISTS attendance_db")
            print("Database 'attendance_db' checked/created.")
            
            # Connect to the specific database
            conn.database = "attendance_db"
            
            # Create students table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS students (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255) NOT NULL
                )
            """)
            print("Table 'students' checked/created.")
            
            # Create attendance table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS attendance (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    student_id INT,
                    date DATE,
                    status VARCHAR(50),
                    UNIQUE(student_id, date),
                    FOREIGN KEY (student_id) REFERENCES students(id)
                )
            """)
            print("Table 'attendance' checked/created.")
            
            # Check if students exist, if not add dummy data
            cursor.execute("SELECT COUNT(*) FROM students")
            count = cursor.fetchone()[0]
            
            if count == 0:
                students = [("Alice",), ("Bob",), ("Charlie",), ("Diana",)]
                cursor.executemany("INSERT INTO students (name) VALUES (%s)", students)
                conn.commit()
                print(f"Added {len(students)} dummy students.")
            else:
                print(f"Students table already has {count} records.")
                
    except Error as e:
        print(f"Error: {e}")
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()
            print("MySQL connection closed.")

if __name__ == "__main__":
    create_database()
