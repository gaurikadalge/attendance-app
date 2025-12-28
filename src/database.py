import sqlite3
import streamlit as st

def get_connection():
    """Connects to the SQLite database."""
    try:
        # Connect to a file-based DB. 
        # check_same_thread=False is needed for Streamlit's threading model if we share connections, 
        # but here we open/close per query so it's less critical, but good practice.
        conn = sqlite3.connect('attendance.db', check_same_thread=False)
        conn.row_factory = sqlite3.Row  # Access columns by name
        return conn
    except Exception as e:
        st.error(f"❌ Database Connection Error: {e}")
        return None

def run_query(query, params=None, fetch=False, fetch_one=False):
    """Executes a query and returns results if fetch is True."""
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        try:
            # SQLite uses ? for placeholders, MySQL uses %s.
            # We'll replace %s with ? to minimize code changes in other files,
            # BUT we must be careful about literal %s. 
            # Given our simple app, a replace is likely safe.
            sqlite_query = query.replace('%s', '?')
            
            if params:
                cursor.execute(sqlite_query, params)
            else:
                cursor.execute(sqlite_query)
            
            if fetch:
                result = [dict(row) for row in cursor.fetchall()]
                return result
            if fetch_one:
                row = cursor.fetchone()
                return dict(row) if row else None
            
            conn.commit()
            return True
        except Exception as e:
            st.error(f"❌ Query Error: {e}")
            return None
        finally:
            cursor.close()
            conn.close()
    return None

def init_db():
    """Initializes the SQLite database with tables."""
    # Create users table
    run_query("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            role TEXT DEFAULT 'admin'
        )
    """)
    
    # Create students table
    run_query("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            roll_no TEXT UNIQUE,
            email TEXT
        )
    """)
    
    # Create attendance table
    # Note: SQLite doesn't support ON DUPLICATE KEY UPDATE directly in the same syntax as MySQL.
    # We need a UNIQUE constraint for ON CONFLICT to work.
    run_query("""
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            date TEXT,
            status TEXT,
            UNIQUE(student_id, date),
            FOREIGN KEY (student_id) REFERENCES students(id)
        )
    """)
    
    # Create default admin if not exists
    existing = run_query("SELECT * FROM users WHERE username = ?", ('admin',), fetch_one=True)
    if not existing:
        run_query("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", ('admin', 'admin123', 'admin'))
