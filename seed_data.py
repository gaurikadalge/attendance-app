import sqlite3
import random

def seed_data():
    conn = sqlite3.connect('attendance.db')
    cursor = conn.cursor()
    
    # Names lists
    first_names = ["Aarav", "Vivaan", "Aditya", "Vihaan", "Arjun", "Sai", "Reyansh", "Ayaan", "Krishna", "Ishaan", "Diya", "Saanvi", "Ananya", "Aadhya", "Pari", "Anika", "Navya", "Angel", "Myra", "Riya"]
    last_names = ["Sharma", "Verma", "Gupta", "Malhotra", "Bhatia", "Saxena", "Mehta", "Chopra", "Singh", "Patel", "Reddy", "Nair", "Iyer", "Rao", "Kumar"]
    
    def generate_name():
        return f"{random.choice(first_names)} {random.choice(last_names)}"
    
    def add_member(role, count, prefix):
        for i in range(1, count + 1):
            name = generate_name()
            roll_no = f"{prefix}{random.randint(1000, 9999)}"
            email = f"{name.lower().replace(' ', '.')}@example.com"
            
            try:
                cursor.execute(
                    "INSERT INTO students (name, roll_no, email, role) VALUES (?, ?, ?, ?)",
                    (name, roll_no, email, role)
                )
                print(f"Added {role}: {name} ({roll_no})")
            except sqlite3.IntegrityError:
                print(f"Skipped duplicate: {name}")

    print("--- Seeding Data ---")
    add_member("Student", 10, "S")
    add_member("Teacher", 5, "T")
    add_member("Worker", 3, "W")
    
    conn.commit()
    conn.close()
    print("--- Seeding Complete ---")

if __name__ == "__main__":
    seed_data()
