from sqlalchemy import Column, Integer, String, Date, Float
from .database import Base

class EnrolmentData(Base):
    __tablename__ = "enrolment_data"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, index=True)
    state = Column(String, index=True)
    district = Column(String, index=True)
    pincode = Column(String, index=True)
    demo_age_0_5 = Column(Integer)
    demo_age_5_17 = Column(Integer)
    demo_age_17_plus = Column(Integer)
