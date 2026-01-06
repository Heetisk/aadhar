import requests
import io
import os
import pandas as pd
from sqlalchemy.orm import Session
from .ingestion import process_csv_and_ingest

# API Configuration moved inside function to support late environment loading
RESOURCE_ID = "19eac040-0b94-49fa-b239-4f2fd8677d53"
BASE_URL = f"https://api.data.gov.in/resource/{RESOURCE_ID}"

def fetch_and_sync_data(db: Session, limit: int = 1000, offset: int = 0, state: str = None, district: str = None, fetch_all: bool = False):
    """
    Fetches data from Aadhar API and ingests it into the database.
    Supports filtering by state and district.
    If fetch_all is True, iteratively fetches all pages until no more data is returned.
    """
    api_key = os.getenv("API_KEY")
    if not api_key:
        print("Warning: API_KEY not found in environment variables.")
        # Fallback to module level if it was set (though we are moving it)
    
    total_synced = 0
    current_offset = offset
    
    # If fetch_all is requested, loop until no data is returned
    # Otherwise, run once with provided limit/offset
    
    while True:
        params = {
            "api-key": api_key,
            "format": "csv",
            "limit": limit,
            "offset": current_offset
        }
        
        # Add filters if provided
        if state:
            params["filters[state]"] = state
        if district:
            params["filters[district]"] = district
        
        try:
            response = requests.get(BASE_URL, params=params)
            response.raise_for_status()
            
            # Check if content is empty
            if not response.content:
                break
                
            content_str = response.content.decode('utf-8')
            if content_str.strip() == "":
                 break
                 
            count = process_csv_and_ingest(response.content, db)
            
            if count == 0:
                break
                
            total_synced += count
            
            if not fetch_all:
                break
                
            # Prepare for next page
            current_offset += limit
            print(f"Fetched {count} records. Next offset: {current_offset}")
            
        except requests.exceptions.RequestException as e:
            print(f"API Request Failed: {e}")
            raise e
        except Exception as e:
            print(f"Sync Failed: {e}")
            raise e
            
    return total_synced
