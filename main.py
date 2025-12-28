import streamlit as st
from src.database import init_db
from src.auth import login_user, logout_user, check_auth, register_user
from src.students import render_student_management
from src.attendance import render_attendance_taking
from src.reports import render_reports

# Page Config
st.set_page_config(page_title="Pro Attendance", page_icon="🎓", layout="wide")

# Custom CSS
st.markdown("""
    <style>
    .main .block-container { padding-top: 2rem; }
    .stButton button { width: 100%; }
    .css-1d391kg { padding-top: 3.5rem; }
    </style>
""", unsafe_allow_html=True)

def main():
    # Initialize DB on first run
    init_db()
    
    if not check_auth():
        st.title("🔐 Access Control")
        
        tab1, tab2 = st.tabs(["Login", "Register"])
        
        with tab1:
            with st.form("login_form"):
                username = st.text_input("Username")
                password = st.text_input("Password", type="password")
                submit = st.form_submit_button("Login")
                
                if submit:
                    login_user(username, password)
        
        with tab2:
            st.write("Create a new account")
            with st.form("register_form"):
                new_user = st.text_input("New Username")
                new_pass = st.text_input("New Password", type="password")
                reg_submit = st.form_submit_button("Register")
                
                if reg_submit:
                    if new_user and new_pass:
                        register_user(new_user, new_pass)
                    else:
                        st.warning("⚠️ Please fill all fields")
        return

    # Sidebar Navigation
    with st.sidebar:
        st.title("🎓 Pro Attendance")
        st.write(f"Logged in as: **{st.session_state.get('username', 'User')}**")
        
        menu = st.radio(
            "Navigation", 
            ["Dashboard", "Mark Attendance", "Students", "Reports"],
            label_visibility="collapsed"
        )
        
        st.write("---")
        if st.button("Logout"):
            logout_user()

    # Main Content
    if menu == "Dashboard":
        st.title("🚀 Dashboard")
        st.write("Welcome to the Professional Attendance Management System.")
        
        # Quick Stats (Placeholder for now, could fetch real real-time stats)
        c1, c2, c3 = st.columns(3)
        with c1:
            st.info("Navigate to **Mark Attendance** to take today's roll call.")
        with c2:
            st.info("Manage student records in the **Students** tab.")
        with c3:
            st.info("View insights in **Reports**.")

    elif menu == "Mark Attendance":
        render_attendance_taking()
    
    elif menu == "Students":
        render_student_management()
        
    elif menu == "Reports":
        render_reports()

if __name__ == "__main__":
    main()
