# Aadhaar Analytics Dashboard

Interactive dashboard for visualizing Aadhaar enrolment trends and insights.

## Features

- 📊 **KPI Cards**: Total enrolments, age group breakdowns, top state
- 📈 **Time-series Chart**: Daily enrolment trends
- 👥 **Age Distribution**: Pie chart showing age group distribution
- 🗺️ **State Rankings**: Bar chart of top 10 states
- ⚠️ **Anomaly Alerts**: Table of low enrolment days
- 🔄 **Data Sync**: Manual sync with API filters

## Setup

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Ensure Backend is Running**:
   ```bash
   cd ..
   uvicorn app.main:app --reload
   ```

3. **Run Dashboard**:
   ```bash
   streamlit run dashboard.py
   ```

4. **Access Dashboard**:
   Open browser at `http://localhost:8501`

## Usage

### Syncing Data
1. Click "Sync Data from API" in the sidebar
2. Set the number of records to fetch
3. Optionally filter by state/district
4. Click "Sync Now"

### Filtering
- Enter state name (e.g., "Gujarat") to filter trends
- Enter district name (e.g., "Surat") for district-specific data
- Click "Refresh Data" to apply filters

## Tech Stack

- **Streamlit**: Dashboard framework
- **Plotly**: Interactive charts
- **Pandas**: Data manipulation
- **Requests**: API integration
