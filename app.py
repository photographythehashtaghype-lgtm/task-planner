import streamlit as st
import pandas as pd
from datetime import datetime

# 1. Setup Connection to your Google Sheet
# Replace this with your actual Google Sheet URL
SHEET_URL = "https://docs.google.com/spreadsheets/d/105IMC5zd_rEe-_RBTuwxA_xS9ItSmpENz4fbUjJUgXM/edit#gid=1174333021"

st.title("📋 TRC Task Planner")

# 2. Sidebar for Login
user = st.sidebar.selectbox("Select Employee", ["Kavya", "Jyothi"])
st.sidebar.write(f"Logged in as: **{user}**")

# 3. Load Data
try:
    # Adding /export?format=csv converts the link into a downloadable format for Python
    csv_url = SHEET_URL.replace("/edit#gid=", "/export?format=csv&gid=")
    df = pd.read_csv(csv_url)
    
    # Filter by User
    user_tasks = df[df['Assigned to'] == user]
    
    st.header(f"Today's Tasks for {user}")
    
    if user_tasks.empty:
        st.info("No tasks assigned for today!")
    else:
        for i, row in user_tasks.iterrows():
            with st.container():
                col1, col2 = st.columns([4, 1])
                col1.write(f"**{row['Description']}**")
                if col2.button("Done", key=f"btn_{i}"):
                    st.success("Marked as Completed!")

except Exception as e:
    st.error("Could not connect to Google Sheets. Check your URL and permissions.")
