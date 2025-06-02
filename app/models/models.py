# models.py

import enum
import uuid
from sqlalchemy import Column, String, Integer, ForeignKey, Date, Enum, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from database import Base
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
from app.database import Base

class AssetStatus(enum.Enum):
    in_use = "In Use"
    under_maintenance = "Under Maintenance"
    retired = "Retired"

class MaintenanceStatus(enum.Enum):
    reported = "Reported"
    in_progress = "In Progress"
    resolved = "Resolved"

class Department(Base):
    __tablename__ = "departments"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, unique=True, nullable=False)
    head_id = Column(UUID(as_uuid=True), ForeignKey("employees.id"), nullable=True)

    head = relationship("Employee", foreign_keys=[head_id], backref="headed_department")
    employees = relationship("Employee", back_populates="department")
    assets = relationship("Asset", back_populates="department")

class Employee(Base):
    __tablename__ = "employees"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    department_id = Column(UUID(as_uuid=True), ForeignKey("departments.id"), nullable=True)
    designation = Column(String)
    date_joined = Column(Date)

    department = relationship("Department", back_populates="employees")
    assigned_assets = relationship("Asset", back_populates="assigned_to_emp", foreign_keys='Asset.assigned_to')
    reported_issues = relationship("MaintenanceLog", back_populates="reporter", foreign_keys='MaintenanceLog.reported_by')
    assigned_tickets = relationship("MaintenanceLog", back_populates="assigned_technician_emp", foreign_keys='MaintenanceLog.assigned_technician')

class Asset(Base):
    __tablename__ = "assets"
    id = Column(Integer, primary_key=True, autoincrement=True)
    asset_tag = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    category = Column(String)
    location = Column(String)
    purchase_date = Column(Date)
    warranty_until = Column(Date)
    assigned_to = Column(UUID(as_uuid=True), ForeignKey("employees.id"), nullable=True)
    department_id = Column(UUID(as_uuid=True), ForeignKey("departments.id"), nullable=True)
    status = Column(Enum(AssetStatus), default=AssetStatus.in_use)

    assigned_to_emp = relationship("Employee", back_populates="assigned_assets")
    department = relationship("Department", back_populates="assets")
    maintenance_logs = relationship("MaintenanceLog", back_populates="asset")
    vendor_links = relationship("AssetVendorLink", back_populates="asset")

class MaintenanceLog(Base):
    __tablename__ = "maintenance_logs"
    id = Column(Integer, primary_key=True, autoincrement=True)
    asset_id = Column(Integer, ForeignKey("assets.id"), nullable=False)
    reported_by = Column(UUID(as_uuid=True), ForeignKey("employees.id"), nullable=False)
    description = Column(Text)
    status = Column(Enum(MaintenanceStatus), default=MaintenanceStatus.reported)
    assigned_technician = Column(UUID(as_uuid=True), ForeignKey("employees.id"), nullable=True)
    resolved_date = Column(Date, nullable=True)

    asset = relationship("Asset", back_populates="maintenance_logs")
    reporter = relationship("Employee", back_populates="reported_issues", foreign_keys=[reported_by])
    assigned_technician_emp = relationship("Employee", back_populates="assigned_tickets", foreign_keys=[assigned_technician])

class Vendor(Base):
    __tablename__ = "vendors"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    contact_person = Column(String)
    email = Column(String)
    phone = Column(String)
    address = Column(String)

    asset_links = relationship("AssetVendorLink", back_populates="vendor")

class AssetVendorLink(Base):
    __tablename__ = "asset_vendor_link"
    id = Column(Integer, primary_key=True, autoincrement=True)
    asset_id = Column(Integer, ForeignKey("assets.id"), nullable=False)
    vendor_id = Column(Integer, ForeignKey("vendors.id"), nullable=False)
    service_type = Column(String)
    last_service_date = Column(Date)

    asset = relationship("Asset", back_populates="vendor_links")
    vendor = relationship("Vendor", back_populates="asset_links")
