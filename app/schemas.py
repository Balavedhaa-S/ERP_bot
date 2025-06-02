from datetime import date
from typing import Optional
from pydantic import BaseModel, EmailStr
import enum
import uuid

class AssetStatus(str, enum.Enum):
    in_use = "In Use"
    under_maintenance = "Under Maintenance"
    retired = "Retired"

class MaintenanceStatus(str, enum.Enum):
    reported = "Reported"
    in_progress = "In Progress"
    resolved = "Resolved"

class Department(BaseModel):
    id: uuid.UUID
    name: str
    head_id: uuid.UUID



class DepartmentBase(BaseModel):
    name: str
    description: Optional[str] = None
    head_id: Optional[uuid.UUID] = None

class DepartmentCreate(DepartmentBase):
    pass

#class Department(DepartmentBase):
 #   id: uuid.UUID

  #  class Config:
  #      orm_mode = True

class EmployeeBase(BaseModel):
    name: str
    email: EmailStr
    department_id: Optional[uuid.UUID] = None
    designation: Optional[str] = None
    date_joined: Optional[date] = None

class EmployeeCreate(EmployeeBase):
    pass

class Employee(EmployeeBase):
    id: uuid.UUID

    class Config:
        orm_mode = True

class AssetBase(BaseModel):
    asset_tag: str
    name: str
    category: Optional[str] = None
    location: Optional[str] = None
    purchase_date: Optional[date] = None
    warranty_until: Optional[date] = None
    assigned_to: Optional[uuid.UUID] = None
    department_id: Optional[uuid.UUID] = None
    status: AssetStatus = AssetStatus.in_use

class AssetCreate(AssetBase):
    pass

class Asset(AssetBase):
    id: int

    class Config:
        orm_mode = True

class MaintenanceLogBase(BaseModel):
    asset_id: int
    reported_by: uuid.UUID
    description: Optional[str] = None
    status: MaintenanceStatus = MaintenanceStatus.reported
    assigned_technician: Optional[uuid.UUID] = None
    resolved_date: Optional[date] = None

class MaintenanceLogCreate(MaintenanceLogBase):
    pass

class MaintenanceLog(MaintenanceLogBase):
    id: int

    class Config:
        orm_mode = True

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
        orm_mode = True

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
        orm_mode = True
