import mysql.connector
from mysql.connector import Error

def update_database():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Gauri@2006",
            database="attendance_db"
        )
        if conn.is_connected():
            cursor = conn.cursor()
            
            # Create users table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(50) NOT NULL UNIQUE,
                    password VARCHAR(255) NOT NULL,
                    role VARCHAR(20) DEFAULT 'admin'
                )
            """)
            print("Table 'users' checked/created.")
            
            # Check for admin user
            cursor.execute("SELECT * FROM users WHERE username = 'admin'")
            if not cursor.fetchone():
                # In a real app, hash this password!
                cursor.execute("INSERT INTO users (username, password, role) VALUES ('admin', 'admin123', 'admin')")
                conn.commit()
                print("Default admin user created.")
            else:
                print("Admin user already exists.")
                
            # Add email and roll_no to students if not exists
            # This is a bit tricky in MySQL without checking columns first, 
            # but for simplicity I'll assume they might not exist or handle error if I try to add them.
            # A better way is to check information_schema.
            
            cursor.execute("""
                SELECT COUNT(*) 
                FROM information_schema.columns 
                WHERE table_name = 'students' AND column_name = 'roll_no' AND table_schema = 'attendance_db'
            """)
            if cursor.fetchone()[0] == 0:
                cursor.execute("ALTER TABLE students ADD COLUMN roll_no VARCHAR(20) UNIQUE")
                print("Added 'roll_no' column to students.")
            
            cursor.execute("""
                SELECT COUNT(*) 
                FROM information_schema.columns 
                WHERE table_name = 'students' AND column_name = 'email' AND table_schema = 'attendance_db'
            """)
            if cursor.fetchone()[0] == 0:
                cursor.execute("ALTER TABLE students ADD COLUMN email VARCHAR(100)")
                print("Added 'email' column to students.")

    except Error as e:
        print(f"Error: {e}")
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()
            print("MySQL connection closed.")

if __name__ == "__main__":
    update_database()
