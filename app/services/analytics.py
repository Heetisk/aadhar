from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from .. import models
import pandas as pd

def get_overall_summary(db: Session):
    total_enrolments = db.query(
        func.sum(models.EnrolmentData.demo_age_0_5 + models.EnrolmentData.demo_age_5_17 + models.EnrolmentData.demo_age_17_plus)
    ).scalar() or 0
    
    total_0_5 = db.query(func.sum(models.EnrolmentData.demo_age_0_5)).scalar() or 0
    total_5_17 = db.query(func.sum(models.EnrolmentData.demo_age_5_17)).scalar() or 0
    total_17_plus = db.query(func.sum(models.EnrolmentData.demo_age_17_plus)).scalar() or 0
    
    # Top state by enrolment
    top_state = db.query(
        models.EnrolmentData.state,
        func.sum(models.EnrolmentData.demo_age_0_5 + models.EnrolmentData.demo_age_5_17 + models.EnrolmentData.demo_age_17_plus).label("total")
    ).group_by(models.EnrolmentData.state).order_by(desc("total")).first()
    
    return {
        "total_enrolments": total_enrolments,
        "total_0_5": total_0_5,
        "total_5_17": total_5_17,
        "total_17_plus": total_17_plus,
        "top_state": top_state[0] if top_state else "N/A"
    }

def get_trends_by_state(db: Session, state: str = None):
    query = db.query(
        models.EnrolmentData.date,
        models.EnrolmentData.state,
        func.sum(models.EnrolmentData.demo_age_0_5 + models.EnrolmentData.demo_age_5_17 + models.EnrolmentData.demo_age_17_plus).label("count")
    )
    if state:
        query = query.filter(models.EnrolmentData.state == state)
        
    results = query.group_by(models.EnrolmentData.date, models.EnrolmentData.state).all()
    # Format for chart: [{date: '...', value: ...}]
    return [{"date": r.date, "state": r.state, "enrolments": r.count} for r in results]

def get_trends_by_district(db: Session, district: str = None):
    query = db.query(
        models.EnrolmentData.date,
        models.EnrolmentData.district,
        func.sum(models.EnrolmentData.demo_age_0_5 + models.EnrolmentData.demo_age_5_17 + models.EnrolmentData.demo_age_17_plus).label("count")
    )
    if district:
        query = query.filter(models.EnrolmentData.district == district)
        
    results = query.group_by(models.EnrolmentData.date, models.EnrolmentData.district).all()
    return [{"date": r.date, "district": r.district, "enrolments": r.count} for r in results]

def get_age_comparison(db: Session):
    # Overall split
    total_0_5 = db.query(func.sum(models.EnrolmentData.demo_age_0_5)).scalar() or 0
    total_5_17 = db.query(func.sum(models.EnrolmentData.demo_age_5_17)).scalar() or 0
    total_17_plus = db.query(func.sum(models.EnrolmentData.demo_age_17_plus)).scalar() or 0
    
    return {
        "age_0_5": total_0_5,
        "age_5_17": total_5_17,
        "age_17_plus": total_17_plus
    }

def get_anomalies(db: Session, threshold: int = 10):
    # Find districts with very low enrolment on specific days
    results = db.query(
        models.EnrolmentData.date,
        models.EnrolmentData.district,
        (models.EnrolmentData.demo_age_0_5 + models.EnrolmentData.demo_age_5_17 + models.EnrolmentData.demo_age_17_plus).label("total")
    ).filter(
        (models.EnrolmentData.demo_age_0_5 + models.EnrolmentData.demo_age_5_17 + models.EnrolmentData.demo_age_17_plus) < threshold
    ).all()
    
    return [{"date": r.date, "district": r.district, "total_enrolment": r.total, "type": "Low Enrolment"} for r in results]

def get_unique_states(db: Session):
    """Get list of unique states in the database"""
    results = db.query(models.EnrolmentData.state).distinct().filter(models.EnrolmentData.state != None).order_by(models.EnrolmentData.state).all()
    return [r[0] for r in results]

def get_unique_districts(db: Session, state: str = None):
    """Get list of unique districts in the database (optionally filtered by state)"""
    query = db.query(models.EnrolmentData.district).distinct().filter(models.EnrolmentData.district != None)
    if state:
        query = query.filter(models.EnrolmentData.state == state)
    results = query.order_by(models.EnrolmentData.district).all()
    return [r[0] for r in results]
