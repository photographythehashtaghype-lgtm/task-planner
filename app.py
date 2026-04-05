import streamlit as st
import pandas as pd
from datetime import datetime

# --- CONFIG ---
st.set_page_config(page_title="TRC Work Plan", layout="wide")

# Load your data (This would eventually link to a Google Sheet)
# For now, we simulate the data structure from your 'PLAN' sheet
def load_data():
    # In production, use: st.connection("gsheets", type=GSheetsConnection)
    data = {
        "Task": ["Cash Reconciliation", "DOSA Report", "Bank Entry Update", "Vendor Bills Filing"],
        "Assigned to": ["Jyothi", "Kavya", "Kavya", "Jyothi"],
        "Frequency": ["Daily", "Daily", "Weekly-Friday", "Weekly-Monday"],
        "Status": ["Pending", "Pending", "Pending", "Pending"]
    }
    return pd.DataFrame(data)

df = load_data()

# --- SIDEBAR ---
st.sidebar.title("User Portal")
user = st.sidebar.selectbox("Login as:", ["Jyothi", "Kavya"])
view = st.sidebar.radio("View", ["Today's Tasks", "Leave Planner", "Work Report"])

# --- MAIN INTERFACE ---
st.title(f"Welcome, {user}")

if view == "Today's Tasks":
    st.subheader(f"Tasks for {datetime.now().strftime('%A, %d %B')}")
    
    # Filter tasks for the logged-in user
    user_tasks = df[df["Assigned to"] == user]
    
    for index, row in user_tasks.iterrows():
        col1, col2, col3 = st.columns([3, 1, 1])
        with col1:
            st.write(f"**{row['Task']}** ({row['Frequency']})")
        with col2:
            if st.button("Complete", key=f"done_{index}"):
                st.success("Task Marked Done!")
        with col3:
            if st.button("Postpone", key=f"post_{index}"):
                reason = st.text_input("Reason for postponing", key=f"reason_{index}")

elif view == "Work Report":
    st.subheader("Daily Work Report Generator")
    # This section would aggregate the 'Done' tasks for the day
    st.info("This will generate a text block you can copy to WhatsApp/Email.")
    if st.button("Generate Report"):
        st.code(f"{user} - {datetime.now().date()} - Work Report\n1. Completed Daily Work\n2. Bank Statement Updated...")
