import sqlite3

def migrate_db():
    conn = sqlite3.connect('attendance.db')
    cursor = conn.cursor()
    
    try:
        # Check if role column exists
        cursor.execute("PRAGMA table_info(students)")
        columns = [info[1] for info in cursor.fetchall()]
        
        if 'role' not in columns:
            print("Adding 'role' column to students table...")
            cursor.execute("ALTER TABLE students ADD COLUMN role TEXT DEFAULT 'Student'")
            conn.commit()
            print("Migration successful.")
        else:
            print("'role' column already exists.")
            
    except Exception as e:
        print(f"Migration failed: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    migrate_db()
