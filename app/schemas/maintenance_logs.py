from pydantic import BaseModel
from uuid import UUID
from typing import Optional
from datetime import datetime
#from app.schemas.maintenance_logs import MaintenanceLogCreate, MaintenanceLogResponse

class MaintenanceLogBase(BaseModel):
    asset_id: int
    reported_by: UUID
    description: Optional[str]
    status: Optional[str] = "Reported"
    assigned_technician: Optional[UUID]
    resolved_date: Optional[datetime]

class MaintenanceLogCreate(MaintenanceLogBase):
    class Config:
        json_schema_extra = {
            "example": {
                "asset_id": 1,
                "reported_by": "123e4567-e89b-12d3-a456-426614174003",
                "description": "Battery issue",
                "status": "Reported",
                "assigned_technician": "123e4567-e89b-12d3-a456-426614174004",
                "resolved_date": None
            }
        }



class MaintenanceLog(MaintenanceLogBase):
    id: int

    class Config:
        from_attributes = True

class MaintenanceLogResponse(BaseModel):
    id: int
    asset_id: int
    description: Optional[str]
    status: Optional[str]
    assigned_technician: Optional[UUID]
    resolved_date: Optional[datetime]

    class Config:
        from_attributes = True  # (or orm_mode = True for Pydantic v1)