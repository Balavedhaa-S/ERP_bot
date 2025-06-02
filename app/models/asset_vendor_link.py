# app/models/asset_vendor_link.py
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from app.models.base import Base

class AssetVendorLink(Base):
    __tablename__ = "asset_vendor_link"
    id = Column(Integer, primary_key=True)
    asset_id = Column(Integer, ForeignKey("assets.id"))
    vendor_id = Column(Integer, ForeignKey("vendors.id"))
    service_type = Column(String)
    last_service_date = Column(Date)
