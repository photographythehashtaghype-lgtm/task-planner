import streamlit as st
import pandas as pd
from datetime import datetime

# --- CONFIG ---
st.set_page_config(page_title="TRC Task Planner", layout="wide")

# The direct link to your 'PLAN' tab (GID 1174333021)
# Using the export format directly to bypass connection issues
SHEET_ID = "105IMC5zd_rEe-_RBTuwxA_xS9ItSmpENz4fbUjJUgXM"
GID = "1174333021"
CSV_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={GID}"

def load_data():
    # Skip the first 4 rows to reach the actual headers (System, Description, etc.)
    data = pd.read_csv(CSV_URL, skiprows=4)
    # Remove any completely empty rows or "Unnamed" columns
    data = data.dropna(subset=['Description', 'Assigned to'])
    data = data.loc[:, ~data.columns.str.contains('^Unnamed')]
    return data

st.title("📋 TRC Professional Task Planner")

try:
    df = load_data()
    
    # 1. Sidebar Login
    unique_users = sorted(df['Assigned to'].unique().tolist())
    user = st.sidebar.selectbox("Login as:", unique_users)
    
    st.sidebar.markdown("---")
    st.sidebar.write(f"**Date:** {datetime.now().strftime('%d %B, %Y')}")

    # 2. Filter tasks for the user
    user_tasks = df[df['Assigned to'] == user]
    
    if user_tasks.empty:
        st.info(f"No tasks found for {user} today.")
    else:
        st.subheader(f"Pending Tasks for {user}")
        
        for i, row in user_tasks.iterrows():
            with st.container():
                # Design a clean 'Card' for each task
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.markdown(f"### {row['Description']}")
                    st.caption(f"System: {row['System']} | Timeline: {row['Timeline']}")
                with col2:
                    st.write("") # Spacing
                    if st.button("Mark Done", key=f"btn_{i}"):
                        st.balloons()
                        st.success("Completed!")
                st.markdown("---")

except Exception as e:
    st.error("Connection Error")
    st.write("Make sure your Google Sheet is set to 'Anyone with the link can view'.")
    st.write(f"Technical details: {e}")
