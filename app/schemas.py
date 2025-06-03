from datetime import date
from typing import Optional
from pydantic import BaseModel, EmailStr
from uuid import UUID
import enum
#from app import schemas
#from app.schemas import AssetUpdate


# --------------------
# Enum Definitions
# --------------------
class AssetStatus(str, enum.Enum):
    in_use = "In Use"
    under_maintenance = "Under Maintenance"
    retired = "Retired"

class MaintenanceStatus(str, enum.Enum):
    reported = "Reported"
    in_progress = "In Progress"
    resolved = "Resolved"


# --------------------
# Department Schemas
# --------------------
class DepartmentBase(BaseModel):
    name: str
    description: Optional[str] = None
    head_id: Optional[UUID] = None

class DepartmentCreate(DepartmentBase):
    pass

class Department(DepartmentBase):
    id: UUID


# --------------------
# Employee Schemas
# --------------------
class EmployeeBase(BaseModel):
    name: str
    email: EmailStr
    department_id: Optional[UUID] = None
    designation: Optional[str] = None
    date_joined: Optional[date] = None

class EmployeeCreate(EmployeeBase):
    pass

class Employee(EmployeeBase):
    id: UUID

    class Config:
        from_attributes = True


# --------------------
# Asset Schemas
# --------------------
class AssetBase(BaseModel):
    asset_tag: str
    name: str
    category: Optional[str] = None
    location: Optional[str] = None
    purchase_date: Optional[date] = None
    warranty_until: Optional[date] = None
    assigned_to: Optional[UUID] = None
    department_id: Optional[UUID] = None
    status: AssetStatus = AssetStatus.in_use

class AssetCreate(AssetBase):
    pass

class Asset(AssetBase):
    id: int

    class Config:
        from_attributes = True

class AssetUpdate(BaseModel):
    asset_tag: Optional[str] = None
    name: Optional[str] = None
    category: Optional[str] = None
    location: Optional[str] = None
    purchase_date: Optional[date] = None
    warranty_until: Optional[date] = None
    assigned_to: Optional[UUID] = None
    department_id: Optional[UUID] = None
    status: Optional[AssetStatus] = None

# --------------------
# MaintenanceLog Schemas
# --------------------
class MaintenanceLogBase(BaseModel):
    asset_id: int
    reported_by: UUID
    description: Optional[str] = None
    status: MaintenanceStatus = MaintenanceStatus.reported
    assigned_technician: Optional[UUID] = None
    resolved_date: Optional[date] = None

class MaintenanceLogCreate(MaintenanceLogBase):
    pass

class MaintenanceLog(MaintenanceLogBase):
    id: int

    class Config:
        from_attributes = True


# --------------------
# Vendor Schemas
# --------------------
class VendorBase(BaseModel):
    name: str
    contact_person: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = None

class VendorCreate(VendorBase):
    pass

class Vendor(VendorBase):
    id: int

    class Config:
        from_attributes = True


# --------------------
# AssetVendorLink Schemas
# --------------------
class AssetVendorLinkBase(BaseModel):
    asset_id: int
    vendor_id: int
    service_type: Optional[str] = None
    last_service_date: Optional[date] = None

class AssetVendorLinkCreate(AssetVendorLinkBase):
    pass

class AssetVendorLink(AssetVendorLinkBase):
    id: int

    class Config:
        from_attributes = True
