import streamlit as st
import pandas as pd
from src.database import run_query

def get_all_students():
    return run_query("SELECT * FROM students ORDER BY name ASC", fetch=True)

def add_student(name, roll_no, email):
    query = "INSERT INTO students (name, roll_no, email) VALUES (%s, %s, %s)"
    return run_query(query, (name, roll_no, email))

def delete_student(student_id):
    query = "DELETE FROM students WHERE id = %s"
    return run_query(query, (student_id,))

def update_student(student_id, name, roll_no, email):
    query = "UPDATE students SET name=%s, roll_no=%s, email=%s WHERE id=%s"
    return run_query(query, (name, roll_no, email, student_id))

def render_student_management():
    st.header("🎓 Student Management")
    
    with st.expander("➕ Add New Student", expanded=False):
        with st.form("add_student_form"):
            name = st.text_input("Full Name")
            roll_no = st.text_input("Roll Number")
            email = st.text_input("Email Address")
            submitted = st.form_submit_button("Add Student")
            
            if submitted:
                if name and roll_no:
                    if add_student(name, roll_no, email):
                        st.success(f"✅ Added {name}")
                        st.rerun()
                else:
                    st.warning("⚠️ Name and Roll Number are required.")

    st.subheader("📋 Student List")
    students = get_all_students()
    if students:
        df = pd.DataFrame(students)
        st.dataframe(df, use_container_width=True)
        
        # Delete/Edit Section
        st.write("### Manage Records")
        col1, col2 = st.columns(2)
        with col1:
            student_to_delete = st.selectbox(
                "Select Student to Delete", 
                students, 
                format_func=lambda x: f"{x['name']} ({x['roll_no']})" if x['roll_no'] else x['name']
            )
            if st.button("🗑️ Delete Student"):
                if delete_student(student_to_delete['id']):
                    st.success("Deleted successfully")
                    st.rerun()
    else:
        st.info("No students found.")
