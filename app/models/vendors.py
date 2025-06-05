# app/models/vendors.py
from sqlalchemy import Column, Integer, String
from app.models.base import Base
from sqlalchemy.orm import relationship
class Vendor(Base):
    __tablename__ = "vendors"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    contact_person = Column(String)
    email = Column(String)
    phone = Column(String)
    address = Column(String)

asset_links = relationship("AssetVendorLink", back_populates="vendor")