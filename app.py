import streamlit as st
import pandas as pd
from datetime import datetime

# --- PAGE CONFIG ---
st.set_page_config(page_title="TRC Task Planner", page_icon="📋")

# --- DATA LOADING ---
def load_data():
    # We fetch the URL from Streamlit Secrets for security
    try:
        base_url = st.secrets["gsheets"]["public_gsheets_url"]
        # This converts the link to a direct CSV export
        csv_url = base_url.replace("/edit?usp=sharing", "/export?format=csv&gid=1174333021")
        
        # Skipping the first 4 rows based on your "PLAN" sheet structure
        df = pd.read_csv(csv_url, skiprows=4)
        
        # Clean up empty columns (Unnamed)
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
        return df
    except Exception as e:
        st.error(f"Error connecting to Google Sheets: {e}")
        return None

# --- APP UI ---
st.title("📋 TRC Task Planner")

df = load_data()

if df is not None:
    # 1. User Selection Sidebar
    # Using 'Assigned to' column from your sheet
    users = df['Assigned to'].dropna().unique().tolist()
    selected_user = st.sidebar.selectbox("Select Employee", users)
    
    st.header(f"Today's Tasks: {selected_user}")
    
    # 2. Filtering Logic
    # Today's day of the week (e.g., 'Monday')
    today_day = datetime.now().strftime('%A')
    
    user_tasks = df[df['Assigned to'] == selected_user]
    
    if user_tasks.empty:
        st.info("No tasks assigned to this user.")
    else:
        for i, row in user_tasks.iterrows():
            with st.expander(f"🔹 {row['Description']}"):
                st.write(f"**System:** {row['System']}")
                st.write(f"**Timeline:** {row['Timeline']}")
                
                col1, col2, col3 = st.columns(3)
                if col1.button("✅ Done", key=f"done_{i}"):
                    st.success("Task completed!")
                if col2.button("⏳ Postpone", key=f"post_{i}"):
                    st.warning("Task postponed.")
                if col3.button("🔄 Transfer", key=f"trans_{i}"):
                    st.info("Task marked for transfer.")
