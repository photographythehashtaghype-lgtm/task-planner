import streamlit as st
import pandas as pd
from datetime import datetime

# --- SETTINGS ---
st.set_page_config(page_title="TRC Task Planner", layout="wide")

# This is your actual Google Sheet ID and the 'PLAN' tab GID
SHEET_ID = "105IMC5zd_rEe-_RBTuwxA_xS9ItSmpENz4fbUjJUgXM"
GID = "1174333021"

# This URL tells Google to give the data as a CSV file directly to the app
CSV_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={GID}"

def load_data():
    # We skip 4 rows because your sheet has 'WORK CHART' titles at the top
    # We use the direct CSV_URL so we don't need 'secrets'
    data = pd.read_csv(CSV_URL, skiprows=4)
    # Clean up: Remove empty rows and "Unnamed" columns
    data = data.dropna(subset=['Description', 'Assigned to'])
    data = data.loc[:, ~data.columns.str.contains('^Unnamed')]
    return data

# --- APP UI ---
st.title("📋 TRC Professional Task Planner")

try:
    df = load_data()
    
    # Sidebar Login
    user_list = sorted(df['Assigned to'].unique().tolist())
    user = st.sidebar.selectbox("Select Employee", user_list)
    
    st.sidebar.divider()
    st.sidebar.write(f"**Date:** {datetime.now().strftime('%d %B, %Y')}")

    # Task Display
    user_tasks = df[df['Assigned to'] == user]
    
    if user_tasks.empty:
        st.info(f"No tasks assigned to {user} today.")
    else:
        st.subheader(f"Tasks for {user}")
        for i, row in user_tasks.iterrows():
            with st.container(border=True):
                c1, c2 = st.columns([4, 1])
                c1.write(f"**{row['Description']}**")
                c1.caption(f"System: {row['System']} | Timeline: {row['Timeline']}")
                if c2.button("Done", key=f"btn_{i}"):
                    st.success("Completed!")
                    st.balloons()

except Exception as e:
    st.error("Connection Error")
    st.info("Check if your Google Sheet 'Sharing' is set to 'Anyone with the link can view'.")
    st.write(f"Technical details: {e}")
