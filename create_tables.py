# create_tables.py

from app.models.base import Base
from app.models import asset_vendor_link, assets, departments, employees, maintenance_logs, vendors
from app.models.db import engine  # Assuming engine is defined here

# This will create all tables based on Base metadata
Base.metadata.create_all(bind=engine)
  # adjust if needed

from app.database import Base, engine
import app.models.assets  # import all models to register them with Base
import app.models.maintenance_logs  # import other models similarly

Base.metadata.create_all(bind=engine)


print("✅ All tables created successfully.")

from app.database import Base, engine
from app import models

Base.metadata.create_all(bind=engine)
print("Tables created successfully.")
