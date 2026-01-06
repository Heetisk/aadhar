import pandas as pd
from sqlalchemy.orm import Session
from .. import models
from datetime import datetime
import io

def process_csv_and_ingest(file_content: bytes, db: Session):
    try:
        # Read CSV
        df = pd.read_csv(io.BytesIO(file_content))
        
        # Standardize column names (stripping spaces, lowercase)
        df.columns = df.columns.str.strip()
        
        # Mapping CSV columns to DB columns
        # Expected: Date, State, District, Pincode, Demo_age_5_17, Demo_age_17+
        # DB: date, state, district, pincode, demo_age_5_17, demo_age_17_plus
        
        column_map = {
            "Date": "date",
            "State": "state",
            "District": "district",
            "Pincode": "pincode",
            "Demo_age_5_17": "demo_age_5_17",
            "Demo_age_17+": "demo_age_17_plus",
            # New format support
            "date": "date",
            "state": "state",
            "district": "district",
            "pincode": "pincode",
            "age_0_5": "demo_age_0_5",
            "age_5_17": "demo_age_5_17",
            "age_18_greater": "demo_age_17_plus",
            # Another format variation
            "demo_age_17_": "demo_age_17_plus"
        }
        
        # Renaissance checks / renaming
        # Check if columns exist, if not try case insensitive search
        
        df = df.rename(columns=column_map)
        
        # Drop rows where critical fields are null
        df = df.dropna(subset=['date', 'state', 'district'])
        
        # Fill numeric nulls with 0
        numeric_cols = ['demo_age_0_5', 'demo_age_5_17', 'demo_age_17_plus']
        for col in numeric_cols:
            if col not in df.columns:
                df[col] = 0
            df[col] = df[col].fillna(0)
        
        # Date parsing
        # Assuming format might vary, but standard is usually YYYY-MM-DD or DD-MM-YYYY
        # We will use pd.to_datetime with infer_datetime_format and dayfirst=True to handle DD-MM-YYYY
        df['date'] = pd.to_datetime(df['date'], errors='coerce', dayfirst=True)
        df = df.dropna(subset=['date']) # Drop invalid dates
        
        # Convert to dictionary records
        records = df.to_dict(orient='records')
        
        # Bulk Insert
        db.bulk_insert_mappings(models.EnrolmentData, records)
        db.commit()
        
        return len(records)
        
    except Exception as e:
        db.rollback()
        raise e
