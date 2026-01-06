# Aadhar Hackathon API

This is a FastAPI-based application designed for the Aadhar Hackathon. It provides analytics and data synchronization capabilities for Aadhar enrolment data, allowing users to upload CSV files or sync data directly from the official government API.

## Features

- **CSV Upload**: Ingest enrolment data via CSV files.
- **API Sync**: Fetch and sync data directly from the official Aadhar Open Data API.
- **Analytics**: View trends by state, district, and age demographics.
- **Anomalies**: Detect low enrolment anomalies.
- **Data Management**: options to clear data and manage sync filters.

## Prerequisites

- Python 3.8+
- pip (Python package installer)

## Installation

1.  **Clone the repository** (if applicable) or navigate to the project directory.

2.  **Create a virtual environment** (recommended):
    ```bash
    python -m venv .venv
    # Windows
    .venv\Scripts\activate
    # Linux/Mac
    source .venv/bin/activate
    ```

3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## Configuration

1.  **Create a `.env` file** in the root directory.
2.  Add your API Key to the `.env` file:
    ```env
    API_KEY=your_api_key_here
    ```
    *(Note: A default key might be provided in `app/services/api_fetcher.py` fallback or documentation, but using `.env` is secure and recommended).*

## Running the Application

To start the server, run:

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

## API Documentation

Once the server is running, you can access the interactive API documentation (Swagger UI) at:
- `http://127.0.0.1:8000/docs`

### Key Endpoints

- **GET /**: Health check.
- **POST /upload**: Upload a CSV file containing enrolment data.
- **POST /sync-api**: Sync data from the external API (supports filtering by state/district).
- **GET /summary**: Get overall enrolment statistics.
- **GET /trends/state**: Get enrolment trends grouped by state.
- **GET /trends/district**: Get enrolment trends grouped by district.
- **GET /age-comparison**: Compare enrolment numbers across age groups.
- **GET /anomalies**: Get districts with low enrolment numbers.
- **DELETE /clear-data**: Clear all data from the database.

## Testing

Batch scripts are provided for easy verification:

- `verify.bat`: Runs the server and executes general API tests.
- `verify_api_sync.bat`: Tests the API synchronization feature.
- `verify_filtered_sync.bat`: Tests filtered synchronization.

To run a test (Windows):
```cmd
verify.bat
```
