from fastapi import FastAPI, Depends, UploadFile, File, HTTPException
from dotenv import load_dotenv

load_dotenv()
from sqlalchemy.orm import Session
from . import models, database, schemas
from .services import ingestion, analytics, api_fetcher
from typing import List, Optional
from typing import List, Optional

# Create DB tables
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Aadhar Hackathon API")

@app.post("/upload")
async def upload_file(file: UploadFile = File(...), db: Session = Depends(database.get_db)):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a CSV.")
    
    content = await file.read()
    try:
        count = ingestion.process_csv_and_ingest(content, db)
        return {"message": f"Successfully processed {count} records."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/sync-api")
def sync_from_api(
    limit: int = 100, 
    offset: int = 0, 
    state: str = None, 
    district: str = None, 
    fetch_all: bool = False,
    db: Session = Depends(database.get_db)
):
    """
    Sync data from official Aadhar API.
    
    Parameters:
    - limit: Maximum number of records to fetch (default: 100)
    - offset: Number of records to skip for pagination (default: 0)
    - state: Filter by state name (optional)
    - district: Filter by district name (optional)
    - fetch_all: If true, loops through all pages until all data is fetched (ignores limit for pagination loop)
    """
    try:
        count = api_fetcher.fetch_and_sync_data(db, limit=limit, offset=offset, state=state, district=district, fetch_all=fetch_all)
        filters_msg = []
        if state:
            filters_msg.append(f"state={state}")
        if district:
            filters_msg.append(f"district={district}")
        if fetch_all:
            filters_msg.append("FETCH_ALL=True")
            
        filter_str = f" with filters: {', '.join(filters_msg)}" if filters_msg else ""
        return {"message": f"Successfully synced {count} records from API{filter_str}."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/options/states")
def get_state_options(db: Session = Depends(database.get_db)):
    """Get list of available states"""
    return analytics.get_unique_states(db)

@app.get("/options/districts")
def get_district_options(state: Optional[str] = None, db: Session = Depends(database.get_db)):
    """Get list of available districts (optionally filtered by state)"""
    return analytics.get_unique_districts(db, state)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Aadhar Hackathon API"}

# Analytics Endpoints

@app.get("/summary", response_model=schemas.SummaryStats)
def get_summary(db: Session = Depends(database.get_db)):
    return analytics.get_overall_summary(db)

@app.get("/trends/state")
def get_trends_state(state: Optional[str] = None, db: Session = Depends(database.get_db)):
    return analytics.get_trends_by_state(db, state)

@app.get("/trends/district")
def get_trends_district(district: Optional[str] = None, db: Session = Depends(database.get_db)):
    return analytics.get_trends_by_district(db, district)

@app.get("/age-comparison")
def get_age_comparison(db: Session = Depends(database.get_db)):
    return analytics.get_age_comparison(db)

@app.get("/anomalies")
def get_anomalies(db: Session = Depends(database.get_db)):
    return analytics.get_anomalies(db)

@app.delete("/clear-data")
def clear_all_data(db: Session = Depends(database.get_db)):
    """Clear all enrolment data from the database"""
    try:
        count = db.query(models.EnrolmentData).delete()
        db.commit()
        return {"message": f"Successfully deleted {count} records from database."}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
