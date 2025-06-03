from sqlalchemy import create_engine
import os

DB_URL = "DATABASE_URL"
engine = create_engine(DB_URL)
