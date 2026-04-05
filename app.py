import streamlit as st
import pandas as pd
from datetime import datetime

# 1. PAGE SETUP
st.set_page_config(page_title="TRC Task Planner", layout="wide")

# 2. DIRECT LINK (No Secrets Required)
# This is the ID from your URL
SHEET_ID = "105IMC5zd_rEe-_RBTuwxA_xS9ItSmpENz4fbUjJUgXM"
# This is the GID for your 'PLAN' tab
GID = "1174333021"
# The magic URL that turns the sheet into a CSV for the app
CSV_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={GID}"

@st.cache_data(ttl=600) # Refreshes every 10 minutes
def load_data():
    # Skip 4 rows to get to your headers: System, Description, Assigned to
    df = pd.read_csv(CSV_URL, skiprows=4)
    # Remove empty rows and junk columns
    df = df.dropna(subset=['Description', 'Assigned to'])
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    return df

# 3. APP INTERFACE
st.title("📋 TRC Task Management Portal")

try:
    data = load_data()
    
    # SIDEBAR LOGIN
    all_users = sorted(data['Assigned to'].unique().tolist())
    user = st.sidebar.selectbox("User Login", all_users)
    
    st.sidebar.divider()
    st.sidebar.info(f"Today is {datetime.now().strftime('%A, %d %B')}")

    # MAIN VIEW
    user_tasks = data[data['Assigned to'] == user]
    
    if user_tasks.empty:
        st.warning(f"No tasks currently assigned to {user}.")
    else:
        st.subheader(f"Pending Tasks for {user}")
        
        for i, row in user_tasks.iterrows():
            with st.container(border=True):
                col_task, col_action = st.columns([4, 1])
                with col_task:
                    st.markdown(f"**{row['Description']}**")
                    st.caption(f"System: {row['System']} | Timeline: {row['Timeline']}")
                with col_action:
                    if st.button("Complete", key=f"btn_{i}"):
                        st.success("Done!")
                        st.balloons()

except Exception as e:
    st.error("⚠️ Connection Error")
    st.write("Streamlit is having trouble reaching your Google Sheet.")
    st.info("Ensure the Sheet is shared as: 'Anyone with the link can view'")
    st.divider()
    st.write(f"Debug Info: {e}")
