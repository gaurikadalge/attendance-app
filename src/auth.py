import streamlit as st
from src.database import run_query

def register_user(username, password):
    """Registers a new user."""
    # Check if user exists
    existing = run_query("SELECT * FROM users WHERE username = %s", (username,), fetch_one=True)
    if existing:
        st.error("⚠️ Username already exists.")
        return False
    
    # Insert new user
    # Default role is 'admin' for now as per schema default, or we can specify it.
    if run_query("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password)):
        st.success("✅ Registration successful! Please login.")
        return True
    return False

def login_user(username, password):
    """Checks credentials and logs in user."""
    # In a real app, hash the password before comparing!
    user = run_query("SELECT * FROM users WHERE username = %s AND password = %s", (username, password), fetch_one=True)
    if user:
        st.session_state['logged_in'] = True
        st.session_state['username'] = user['username']
        st.session_state['role'] = user['role']
        st.success(f"Welcome back, {user['username']}!")
        st.rerun()
    else:
        st.error("❌ Invalid username or password")

def logout_user():
    """Logs out the user."""
    st.session_state['logged_in'] = False
    st.session_state['username'] = None
    st.session_state['role'] = None
    st.rerun()

def check_auth():
    """Checks if user is logged in."""
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
    return st.session_state['logged_in']
