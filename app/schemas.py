from pydantic import BaseModel
from datetime import date as date_type
from typing import Optional

class EnrolmentBase(BaseModel):
    date: date_type
    state: str
    district: str
    pincode: str
    demo_age_0_5: int
    demo_age_5_17: int
    demo_age_17_plus: int

class EnrolmentCreate(EnrolmentBase):
    pass

class Enrolment(EnrolmentBase):
    id: int

    class Config:
        from_attributes = True

class SummaryStats(BaseModel):
    total_enrolments: int
    total_0_5: int
    total_5_17: int
    total_17_plus: int
    top_state: str
