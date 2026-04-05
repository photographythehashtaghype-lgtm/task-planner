import streamlit as st
import pandas as pd
from datetime import datetime

# --- FORCE SETTINGS ---
st.set_page_config(page_title="TRC Task Planner", layout="wide")

# DIRECT LINK - This bypasses the need for the "gsheets" secret
SHEET_ID = "105IMC5zd_rEe-_RBTuwxA_xS9ItSmpENz4fbUjJUgXM"
GID = "1174333021"
CSV_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={GID}"

def load_data():
    # We use the raw CSV URL directly
    df = pd.read_csv(CSV_URL, skiprows=4)
    df = df.dropna(subset=['Description', 'Assigned to'])
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    return df

st.title("📋 TRC Task Management")

try:
    data = load_data()
    
    # Sidebar Login
    users = sorted(data['Assigned to'].unique().tolist())
    user = st.sidebar.selectbox("Select Employee", users)
    
    st.sidebar.divider()
    st.sidebar.write(f"Logged in: **{user}**")

    # Main Task List
    user_tasks = data[data['Assigned to'] == user]
    
    if user_tasks.empty:
        st.info(f"No tasks found for {user}.")
    else:
        for i, row in user_tasks.iterrows():
            with st.container(border=True):
                col1, col2 = st.columns([4, 1])
                col1.markdown(f"**{row['Description']}**")
                col1.caption(f"System: {row['System']} | Timeline: {row['Timeline']}")
                if col2.button("Done", key=f"btn_{i}"):
                    st.success("Completed!")

except Exception as e:
    st.error("Connection Failed")
    st.write(f"Error: {e}")
