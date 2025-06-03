from pydantic import BaseModel
from uuid import UUID
from typing import Optional
from datetime import date
from app.schemas.enums import AssetStatus
import enum

class AssetBase(BaseModel):
    asset_tag: str
    name: str
    category: Optional[str]
    location: Optional[str]
    purchase_date: Optional[date]
    warranty_until: Optional[date]
    assigned_to: Optional[UUID]
    department_id: Optional[UUID]
    status: str  # Could be "In Use", "Under Maintenance", etc.

class AssetCreate(AssetBase):
    class Config:
        json_schema_extra = {
            "example": {
                "asset_tag": "ASSET-12345",
                "name": "Dell Laptop",
                "category": "Electronics",
                "location": "Head Office",
                "purchase_date": "2024-06-01",
                "warranty_until": "2027-06-01",
                "assigned_to": "123e4567-e89b-12d3-a456-426614174000",  # sample UUID
                "department_id": "123e4567-e89b-12d3-a456-426614174001",  # sample UUID
                "status": "In Use"
            }
        }



class Asset(AssetBase):
    id: int

    class Config:
        from_attributes = True
class AssetResponse(Asset):
    assigned_to_name: Optional[str] = None
    department_name: Optional[str] = None
    
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

class AssetStatus(str, enum.Enum):
    in_use = "In Use"
    under_maintenance = "Under Maintenance"
    retired = "Retired"
