import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# Page configuration
st.set_page_config(
    page_title="Aadhaar Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API Configuration
API_BASE_URL = "http://127.0.0.1:8000"

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# Helper Functions
@st.cache_data(ttl=60)
def fetch_summary():
    """Fetch summary statistics from API"""
    try:
        response = requests.get(f"{API_BASE_URL}/summary")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Failed to fetch summary: {e}")
        return None

@st.cache_data(ttl=60)
def fetch_trends_state(state=None):
    """Fetch state trends from API"""
    try:
        url = f"{API_BASE_URL}/trends/state"
        if state:
            url += f"?state={state}"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Failed to fetch state trends: {e}")
        return []

@st.cache_data(ttl=60)
def fetch_trends_district(district=None):
    """Fetch district trends from API"""
    try:
        url = f"{API_BASE_URL}/trends/district"
        if district:
            url += f"?district={district}"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Failed to fetch district trends: {e}")
        return []

@st.cache_data(ttl=60)
def fetch_age_comparison():
    """Fetch age comparison data from API"""
    try:
        response = requests.get(f"{API_BASE_URL}/age-comparison")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Failed to fetch age comparison: {e}")
        return None

@st.cache_data(ttl=60)
def fetch_anomalies():
    """Fetch anomalies from API"""
    try:
        response = requests.get(f"{API_BASE_URL}/anomalies")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Failed to fetch anomalies: {e}")
        return []

@st.cache_data(ttl=60)
def fetch_state_options():
    """Fetch unique states from API"""
    try:
        response = requests.get(f"{API_BASE_URL}/options/states")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return []

@st.cache_data(ttl=60)
def fetch_district_options(state=None):
    """Fetch unique districts from API"""
    try:
        url = f"{API_BASE_URL}/options/districts"
        if state:
            url += f"?state={state}"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return []

def sync_api_data(limit, state=None, district=None, fetch_all=False):
    """Trigger API sync"""
    try:
        params = {"limit": limit, "fetch_all": fetch_all}
        if state:
            params["state"] = state
        if district:
            params["district"] = district
        
        response = requests.post(f"{API_BASE_URL}/sync-api", params=params)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Sync failed: {e}")
        return None

def upload_csv_file(uploaded_file):
    """Upload CSV file to backend"""
    try:
        files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "text/csv")}
        response = requests.post(f"{API_BASE_URL}/upload", files=files)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Upload failed: {e}")
        return None

def clear_database():
    """Clear all data from database"""
    try:
        response = requests.delete(f"{API_BASE_URL}/clear-data")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Clear failed: {e}")
        return None

# Main Dashboard
st.markdown('<h1 class="main-header">📊 Aadhaar Enrolment Analytics Dashboard</h1>', unsafe_allow_html=True)

# Session State Initialization
if 'initialized' not in st.session_state:
    st.session_state['initialized'] = True
    # Auto-clear DB on first load as requested
    with st.spinner("Initializing dashboard and clearing previous data..."):
        clear_database()
        st.toast("Database cleared for new session", icon="🧹")

# Sidebar - Filters
st.sidebar.header("🔍 Filters & Controls")

# --- GLOBAL FILTERS ---
st.sidebar.subheader("🗺️ Geographic Filters")

# Filter Mode Toggle
filter_mode = st.sidebar.radio("Filter Selection Mode", ["Dropdown", "Manual"], horizontal=True)

if filter_mode == "Dropdown":
    # Fetch available options
    state_options = fetch_state_options()
    state_options = ["All"] + state_options if state_options else ["All"]

    filter_state = st.sidebar.selectbox("Filter by State", options=state_options)

    # Filter districts based on selected state
    if filter_state != "All":
        district_options = fetch_district_options(filter_state)
    else:
        district_options = fetch_district_options()
        
    district_options = ["All"] + district_options if district_options else ["All"]
    filter_district = st.sidebar.selectbox("Filter by District", options=district_options)

    # Map "All" to None for API logic
    selected_state = filter_state if filter_state != "All" else None
    selected_district = filter_district if filter_district != "All" else None
else:
    # Manual Input Mode
    selected_state = st.sidebar.text_input("Enter State Name", placeholder="e.g. Gujarat")
    selected_district = st.sidebar.text_input("Enter District Name", placeholder="e.g. Surat")
    
    # Clean up empty strings to None
    selected_state = selected_state.strip() if selected_state else None
    selected_district = selected_district.strip() if selected_district else None
    
    # For display in info messages
    filter_state = selected_state if selected_state else "All"
    filter_district = selected_district if selected_district else "All"

st.sidebar.markdown("---")

# CSV Upload Section
with st.sidebar.expander("📤 Upload CSV File", expanded=True):
    uploaded_file = st.file_uploader("Choose a CSV file", type=['csv'])
    clear_before_upload = st.checkbox("Clear existing data before upload", value=True, key="clear_upload")
    
    if uploaded_file is not None:
        if st.button("📁 Upload & Process", type="primary", key="upload_btn"):
            with st.spinner("Processing..."):
                if clear_before_upload:
                    clear_database()
                
                result = upload_csv_file(uploaded_file)
                if result:
                    st.success(result.get("message", "Upload completed!"))
                    st.cache_data.clear()
                    st.rerun()

st.sidebar.markdown("---")

# Data Sync Section
with st.sidebar.expander("🔄 Sync Data from API", expanded=True):
    st.info(f"Syncing data for: {filter_state} / {filter_district}")
    fetch_all = st.checkbox("Fetch All Records (ignores limit)", value=False)
    sync_limit = st.number_input("Records to fetch", min_value=10, max_value=1000, value=100, step=10, disabled=fetch_all)
    
    clear_before_sync = st.checkbox("Clear existing data before sync", value=True, key="clear_sync")
    
    if st.button("🚀 Sync Now", type="primary"):
        with st.spinner("Syncing data..."):
            if clear_before_sync:
                clear_database()
                
            # Use selected_state and selected_district from Global Filters
            result = sync_api_data(sync_limit, selected_state, selected_district, fetch_all=fetch_all)
            if result:
                st.success(result.get("message", "Sync completed!"))
                st.cache_data.clear()  # Clear cache to refresh data
                st.rerun()

st.sidebar.markdown("---")

# Clear Database Section
st.sidebar.subheader("🗑️ Data Management")
if st.sidebar.button("🗑️ Clear All Data", type="secondary"):
    if st.sidebar.checkbox("⚠️ Confirm deletion (this cannot be undone)"):
        with st.spinner("Clearing database..."):
            result = clear_database()
            if result:
                st.sidebar.success(result.get("message", "Database cleared!"))
                st.cache_data.clear()
                st.rerun()

if st.sidebar.button("🔄 Refresh Data"):
    st.cache_data.clear()
    st.rerun()

# Main Content
# KPI Cards
st.subheader("📈 Key Performance Indicators")
summary = fetch_summary()

if summary:
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("Total Enrolments", f"{summary.get('total_enrolments', 0):,}")
    with col2:
        st.metric("Age 0-5", f"{summary.get('total_0_5', 0):,}")
    with col3:
        st.metric("Age 5-17", f"{summary.get('total_5_17', 0):,}")
    with col4:
        st.metric("Age 17+", f"{summary.get('total_17_plus', 0):,}")
    with col5:
        st.metric("Top State", summary.get('top_state', 'N/A'))

st.markdown("---")

# Charts Section
col_left, col_right = st.columns(2)

# Time-series Chart
with col_left:
    st.subheader("📊 Enrolment Trends Over Time")
    trends_data = fetch_trends_state(selected_state)
    
    if trends_data:
        df_trends = pd.DataFrame(trends_data)
        df_trends['date'] = pd.to_datetime(df_trends['date'])
        
        fig_trends = px.line(
            df_trends, 
            x='date', 
            y='enrolments',
            color='state' if 'state' in df_trends.columns else None,
            title="Daily Enrolments",
            labels={'enrolments': 'Number of Enrolments', 'date': 'Date'}
        )
        fig_trends.update_layout(height=400)
        st.plotly_chart(fig_trends, use_container_width=True)
    else:
        st.info("No trend data available. Sync data first.")

# Age Group Pie Chart
with col_right:
    st.subheader("👥 Age Group Distribution")
    age_data = fetch_age_comparison()
    
    if age_data:
        age_df = pd.DataFrame([
            {"Age Group": "0-5", "Count": age_data.get('age_0_5', 0)},
            {"Age Group": "5-17", "Count": age_data.get('age_5_17', 0)},
            {"Age Group": "17+", "Count": age_data.get('age_17_plus', 0)}
        ])
        
        fig_age = px.pie(
            age_df,
            values='Count',
            names='Age Group',
            title="Enrolments by Age Group",
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig_age.update_layout(height=400)
        st.plotly_chart(fig_age, use_container_width=True)
    else:
        st.info("No age comparison data available.")

# State-wise Bar Chart
st.subheader("🗺️ Top States by Enrolment")
# Use filtered data if state filter is provided, otherwise show all
state_trends = fetch_trends_state(selected_state)

if state_trends:
    df_states = pd.DataFrame(state_trends)
    if 'state' in df_states.columns:
        state_summary = df_states.groupby('state')['enrolments'].sum().reset_index()
        state_summary = state_summary.sort_values('enrolments', ascending=False).head(10)
        
        # Update title based on filter
        chart_title = f"Top 10 States" if not selected_state else f"Enrolments for {selected_state}"
        
        fig_states = px.bar(
            state_summary,
            x='state',
            y='enrolments',
            title=chart_title,
            labels={'enrolments': 'Total Enrolments', 'state': 'State'},
            color='enrolments',
            color_continuous_scale='Blues'
        )
        fig_states.update_layout(
            height=400,
            xaxis={'categoryorder': 'total descending'}
        )
        st.plotly_chart(fig_states, use_container_width=True)
    else:
        st.info("No state-level data available.")

# Anomalies Table
st.subheader("⚠️ Anomaly Alerts (Low Enrolment Days)")
anomalies = fetch_anomalies()

if anomalies:
    df_anomalies = pd.DataFrame(anomalies)
    df_anomalies['date'] = pd.to_datetime(df_anomalies['date']).dt.date
    st.dataframe(
        df_anomalies[['date', 'district', 'total_enrolment', 'type']].head(20),
        use_container_width=True,
        hide_index=True
    )
else:
    st.info("No anomalies detected.")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666;'>
    <p>Aadhaar Analytics Dashboard | Powered by FastAPI + Streamlit</p>
    </div>
    """,
    unsafe_allow_html=True
)
