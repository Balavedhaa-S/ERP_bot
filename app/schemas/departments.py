from pydantic import BaseModel
from uuid import UUID
from typing import Optional

class DepartmentBase(BaseModel):
    name: str
    description: Optional[str] = None
    head_id: Optional[UUID] = None
    
class DepartmentCreate(DepartmentBase):
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Finance",
                "description": "Handles company finances and budgeting.",
                "head_id": "123e4567-e89b-12d3-a456-426614174002"
            }
        }



class Department(DepartmentBase):
    id: UUID

    class Config:
        from_attributes = True  # Use this instead of `orm_mode=True` (Pydantic v2+)
