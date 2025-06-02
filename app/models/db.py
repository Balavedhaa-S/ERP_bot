from sqlalchemy import create_engine
import os

DB_URL = "postgresql+psycopg2://postgres:Admin!18@localhost:5432/erp_chatbot"
engine = create_engine(DB_URL)
