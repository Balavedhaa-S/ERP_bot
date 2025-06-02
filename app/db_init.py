
# app/db_init.py

from sqlalchemy import create_engine
from app.models.base import Base

# Order matters! Define base tables FIRST
from app.models.departments import Department
from app.models.employees import Employee

# Then define dependent tables
from app.models.assets import Asset
from app.models.maintenance_logs import MaintenanceLog
from app.models.vendors import Vendor
from app.models.asset_vendor_link import AssetVendorLink
from database import engine, Base
from models import Employee, Asset
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

def init_db():
    Base.metadata.create_all(bind=engine)
    print("✅ All tables created!")

if __name__ == "__main__":
    init_db()
