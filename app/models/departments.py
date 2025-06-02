# app/models/departments.py
from sqlalchemy import Column, String, Integer
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import Base
from sqlalchemy.orm import relationship
class Department(Base):
    __tablename__ = "departments"
    id = Column(UUID, primary_key=True)
    name = Column(String)
    head_id = Column(UUID)  # FK to employees.id
