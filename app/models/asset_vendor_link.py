from sqlalchemy import Column, Integer, ForeignKey, String, Date, UniqueConstraint
from sqlalchemy.orm import relationship
from app.database import Base

class AssetVendorLink(Base):
    __tablename__ = "asset_vendor_link"
    id = Column(Integer, primary_key=True, index=True)
    asset_id = Column(Integer, ForeignKey("assets.id"), nullable=False)
    vendor_id = Column(Integer, ForeignKey("vendors.id"), nullable=False)
    service_type = Column(String, nullable=False)
    last_service_date = Column(Date, nullable=True)

    # Relationships (optional for ORM navigation)
    asset = relationship("Asset", back_populates="vendor_links")
    vendor = relationship("Vendor", back_populates="asset_links")

    __table_args__ = (UniqueConstraint('asset_id', 'vendor_id', name='_asset_vendor_uc'),)
