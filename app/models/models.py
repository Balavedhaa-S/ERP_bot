from sqlalchemy import Column, String, Integer, Date, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from app.database import Base
import enum

# Optional: for status field in Asset
class AssetStatus(str, enum.Enum):
    available = "Available"
    assigned = "Assigned"
    in_maintenance = "In Maintenance"
    retired = "Retired"

class Department(Base):
    __tablename__ = "departments"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, unique=True, nullable=False)
    head_id = Column(UUID(as_uuid=True), ForeignKey("employees.id"), nullable=True)

    head = relationship("Employee", foreign_keys=[head_id], back_populates="headed_department", uselist=False)
    employees = relationship("Employee", back_populates="department", cascade="all, delete")
    assets = relationship("Asset", back_populates="department", cascade="all, delete")


class Employee(Base):
    __tablename__ = "employees"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    department_id = Column(UUID(as_uuid=True), ForeignKey("departments.id"))
    designation = Column(String)
    date_joined = Column(Date)

    department = relationship("Department", back_populates="employees")
    assets = relationship("Asset", back_populates="assigned_employee")
    headed_department = relationship("Department", foreign_keys=[Department.head_id], back_populates="head", uselist=False)


class Asset(Base):
    __tablename__ = "assets"
    id = Column(Integer, primary_key=True, index=True)
    asset_tag = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    category = Column(String)
    location = Column(String)
    purchase_date = Column(Date)
    warranty_until = Column(Date)
    assigned_to = Column(UUID(as_uuid=True), ForeignKey("employees.id"), nullable=True)
    department_id = Column(UUID(as_uuid=True), ForeignKey("departments.id"))
    status = Column(Enum(AssetStatus), default=AssetStatus.available)

    assigned_employee = relationship("Employee", back_populates="assets")
    department = relationship("Department", back_populates="assets")

    vendor_links = relationship(
        "AssetVendorLink", back_populates="asset", cascade="all, delete"
    )
    maintenance_logs = relationship(
        "MaintenanceLog", back_populates="asset", cascade="all, delete"
    )

#from sqlalchemy import Column, String, Integer, Date, ForeignKey, Enum, Text, Table
#from sqlalchemy.dialects.postgresql import UUID
#from sqlalchemy.orm import relationship
#import uuid
#import enum
#from app.database import Base  # your Base class import

# Assuming you already have AssetStatus and previous models here...

# Vendor model
class Vendor(Base):
    __tablename__ = "vendors"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False, unique=True)
    contact_email = Column(String, unique=True, nullable=True)
    phone_number = Column(String, nullable=True)
    address = Column(Text, nullable=True)

    # relationship with AssetVendorLink - many-to-many
    assets = relationship(
        "AssetVendorLink", back_populates="vendor", cascade="all, delete"
    )


# Association table for many-to-many Asset <-> Vendor relationship
class AssetVendorLink(Base):
    __tablename__ = "asset_vendor_link"
    id = Column(Integer, primary_key=True, autoincrement=True)
    asset_id = Column(Integer, ForeignKey("assets.id"), nullable=False)
    vendor_id = Column(UUID(as_uuid=True), ForeignKey("vendors.id"), nullable=False)

    asset = relationship("Asset", back_populates="vendor_links")
    vendor = relationship("Vendor", back_populates="assets")


# MaintenanceLog model
class MaintenanceLog(Base):
    __tablename__ = "maintenance_logs"
    id = Column(Integer, primary_key=True, index=True)
    asset_id = Column(Integer, ForeignKey("assets.id"), nullable=False)
    performed_on = Column(Date, nullable=False)
    description = Column(Text, nullable=True)
    performed_by = Column(String, nullable=True)  # could be a person or company name

    asset = relationship("Asset", back_populates="maintenance_logs")
