# Professional Attendance App

A Streamlit-based attendance management system with authentication, student management, and analytics.

## Features
- **Authentication**: Login/Register (Admin role).
- **Student Management**: Add, edit, delete students.
- **Attendance**: Mark present/absent/late, bulk actions.
- **Reports**: View trends and export CSV.
- **Database**: SQLite (Portable).

## How to Run Locally
```bash
pip install -r requirements.txt
streamlit run main.py
```

## Deployment (Streamlit Community Cloud)
1. Push this code to GitHub.
2. Go to [share.streamlit.io](https://share.streamlit.io).
3. Connect your GitHub account.
4. Select this repository.
5. Set "Main file path" to `main.py`.
6. Click **Deploy**.
