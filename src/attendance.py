import streamlit as st
from datetime import date
from src.database import run_query

def mark_attendance(student_id, attendance_date, status, notes=""):
    query = """
        INSERT INTO attendance (student_id, date, status)
        VALUES (%s, %s, %s)
        ON CONFLICT(student_id, date) DO UPDATE SET status=excluded.status
    """
    # Note: I'm not storing notes yet as the table doesn't have it, but I'll add it to the UI logic.
    # If I want notes, I need to alter the table. For now, I'll skip saving notes to DB to keep it simple or alter DB.
    # Let's stick to status for now.
    return run_query(query, (student_id, attendance_date, status))

def mark_bulk_attendance(student_ids, attendance_date, status):
    # This is inefficient (N queries), but safe. Batch insert would be better.
    for sid in student_ids:
        mark_attendance(sid, attendance_date, status)
    return True

def render_attendance_taking():
    st.header("📝 Mark Attendance")
    
    selected_date = st.date_input("Date", date.today(), max_value=date.today())
    
    # Role Filter
    role_filter = st.selectbox("Filter by Role", ["All", "Student", "Teacher", "Worker"])
    
    query = "SELECT * FROM students"
    params = []
    if role_filter != "All":
        query += " WHERE role = ?"
        params.append(role_filter)
    query += " ORDER BY name ASC"
    
    students = run_query(query, tuple(params), fetch=True)
    
    if not students:
        st.warning("No members found to mark.")
        return

    # Bulk Actions
    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ Mark All Present"):
            mark_bulk_attendance([s['id'] for s in students], selected_date, "Present")
            st.success("Marked all present!")
            st.rerun()
    with col2:
        if st.button("❌ Mark All Absent"):
            mark_bulk_attendance([s['id'] for s in students], selected_date, "Absent")
            st.success("Marked all absent!")
            st.rerun()

    st.write("---")
    
    # Individual Marking
    with st.form("attendance_form"):
        attendance_data = {}
        for student in students:
            col_a, col_b = st.columns([3, 2])
            with col_a:
                roll_text = f"({student['roll_no']})" if student['roll_no'] else ""
                st.markdown(f"**{student['name']}** {roll_text}")
            with col_b:
                # Fetch existing status if any
                existing = run_query(
                    "SELECT status FROM attendance WHERE student_id=%s AND date=%s", 
                    (student['id'], selected_date), 
                    fetch_one=True
                )
                default_idx = 0
                if existing:
                    if existing['status'] == 'Present': default_idx = 0
                    elif existing['status'] == 'Absent': default_idx = 1
                    elif existing['status'] == 'Late': default_idx = 2
                
                status = st.radio(
                    "Status", 
                    ["Present", "Absent", "Late"], 
                    key=f"status_{student['id']}", 
                    horizontal=True,
                    index=default_idx,
                    label_visibility="collapsed"
                )
                attendance_data[student['id']] = status
        
        if st.form_submit_button("💾 Save Attendance"):
            for sid, status in attendance_data.items():
                mark_attendance(sid, selected_date, status)
            st.success("Attendance Saved Successfully!")
