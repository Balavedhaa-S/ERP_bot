from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from sqlalchemy import Column, Date
from app.database import Base  # Make sure this is the correct import

class MaintenanceLog(Base):
    __tablename__ = "maintenance_logs"

    id = Column(Integer, primary_key=True, index=True)
    asset_id = Column(Integer, nullable=False)
    maintenance_type = Column(String, nullable=False)
    description = Column(String)
    #maintenance_date = Column(DateTime)
    maintenance_date = Column(Date)