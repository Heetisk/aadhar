# 📊 Aadhaar Analytics Dashboard

An interactive full-stack application for visualizing Aadhaar enrolment trends and insights. This project combines a **FastAPI** backend for robust data management and a **Streamlit** frontend for a premium analytical experience.

## 🚀 Features

### 📈 Real-time Analytics
- **KPI Cards**: Instantly view total enrolments, age group breakdowns (0-5, 5-17, 17+), and top-performing states.
- **Trend Analysis**: Interactive time-series charts showing daily enrolment patterns.
- **Geographic Insights**: Bar charts ranking states by enrolment volume.
- **Anomaly Detection**: Automatic identification of low enrolment days to flag potential data or operational issues.

### 🗺️ Advanced Filtering
- **Dropdown Mode**: Select from auto-populated states and districts available in the database.
- **Manual Mode [NEW]**: Type state and district names directly—perfect for syncing data for new regions.

### 🔄 Data Management
- **API Sync**: Seamless integration with the official Aadhaar Open Data API with customizable fetch limits.
- **CSV Upload**: Bulk ingest data via CSV files.
- **Safe State**: Automatic database clearing on new session starts (optional) and manual data management tools.

## 🛠️ Tech Stack

- **Frontend**: [Streamlit](https://streamlit.io/) + [Plotly](https://plotly.com/)
- **Backend**: [FastAPI](https://fastapi.tiangolo.com/) + [SQLAlchemy](https://www.sqlalchemy.org/)
- **Database**: SQLite (local)
- **Data Source**: Official Aadhaar Open Data API

## ⚙️ Setup & Installation

### 1. Environment Setup
```bash
# Clone the repository
git clone <repository-url>
cd aadhar-hackathon

# Create and activate virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configuration
Create a `.env` file in the root directory:
```env
API_KEY=your_aadhaar_data_gov_in_api_key
```

## 🏃 Running the Application

For the best experience, run both the backend and frontend simultaneously:

### Start the Backend (API)
```bash
uvicorn app.main:app --port 8000 --reload
```
Navigate to `http://127.0.0.1:8000/docs` to view the interactive API documentation.

### Start the Frontend (Dashboard)
```bash
streamlit run streamlit_app.py
```
The dashboard will be available at `http://localhost:8501`.

## 📂 Project Structure

- `app/`: FastAPI application logic.
  - `services/`: Core logic for API fetching, ingestion, and analytics.
  - `models.py`: Database schema definitions.
- `frontend/`: (Optional) Alternative dashboard entry points.
- `streamlit_app.py`: Main Streamlit dashboard file.
- `testing/`: Verification scripts and sample data.

---
*Developed for the Aadhaar Analytics Hackathon.*
