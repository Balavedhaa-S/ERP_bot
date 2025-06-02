from pydantic import BaseModel
from uuid import UUID
from typing import Optional
from datetime import date

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
    pass

class Asset(AssetBase):
    id: int

    class Config:
        from_attributes = True
class AssetResponse(Asset):
    assigned_to_name: Optional[str] = None
    department_name: Optional[str] = None