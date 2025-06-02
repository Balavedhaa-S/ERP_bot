from pydantic import BaseModel
from uuid import UUID
from typing import Optional

class DepartmentBase(BaseModel):
    name: str
    description: Optional[str] = None
    head_id: Optional[UUID] = None
    
class DepartmentCreate(DepartmentBase):
    pass

class Department(DepartmentBase):
    id: UUID

    class Config:
        from_attributes = True  # Use this instead of `orm_mode=True` (Pydantic v2+)
