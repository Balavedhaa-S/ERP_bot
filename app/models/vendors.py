# app/models/vendors.py
from sqlalchemy import Column, Integer, String
from app.models.base import Base

class Vendor(Base):
    __tablename__ = "vendors"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    contact_person = Column(String)
    email = Column(String)
    phone = Column(String)
    address = Column(String)
