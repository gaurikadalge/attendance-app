import streamlit as st
import pandas as pd
import altair as alt
from src.database import run_query

def get_attendance_report(start_date=None, end_date=None):
    query = """
        SELECT a.date, s.name, s.roll_no, a.status 
        FROM attendance a
        JOIN students s ON a.student_id = s.id
    """
    params = []
    if start_date and end_date:
        query += " WHERE a.date BETWEEN %s AND %s"
        params.extend([start_date, end_date])
    
    query += " ORDER BY a.date DESC, s.name ASC"
    return run_query(query, tuple(params), fetch=True)

def render_reports():
    st.header("📊 Analytics & Reports")
    
    # Filters
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date")
    with col2:
        end_date = st.date_input("End Date")
        
    if start_date > end_date:
        st.error("Start date cannot be after end date.")
        return

    data = get_attendance_report(start_date, end_date)
    
    if data:
        df = pd.DataFrame(data)
        
        # Metrics
        total_records = len(df)
        present_count = len(df[df['status'] == 'Present'])
        absent_count = len(df[df['status'] == 'Absent'])
        late_count = len(df[df['status'] == 'Late'])
        
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Total Records", total_records)
        m2.metric("Present", present_count)
        m3.metric("Absent", absent_count)
        m4.metric("Late", late_count)
        
        # Charts
        st.subheader("Attendance Trends")
        chart_data = df.groupby(['date', 'status']).size().reset_index(name='count')
        
        chart = alt.Chart(chart_data).mark_bar().encode(
            x='date:T',
            y='count:Q',
            color=alt.Color('status', scale=alt.Scale(domain=['Present', 'Absent', 'Late'], range=['#28a745', '#dc3545', '#ffc107'])),
            tooltip=['date', 'status', 'count']
        ).interactive()
        
        st.altair_chart(chart, use_container_width=True)
        
        # Data Table
        st.subheader("Detailed Records")
        st.dataframe(df, width='stretch')
        
        # Export
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            "📥 Download CSV",
            csv,
            "attendance_report.csv",
            "text/csv",
            key='download-csv'
        )
    else:
        st.info("No attendance records found for the selected period.")
