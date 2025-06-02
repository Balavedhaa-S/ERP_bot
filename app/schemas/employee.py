from pydantic import BaseModel
from uuid import UUID
from typing import Optional
from datetime import date

class EmployeeBase(BaseModel):
    name: str
    email: str
    department_id: Optional[UUID]
    designation: Optional[str]
    date_joined: Optional[date]

class EmployeeCreate(EmployeeBase):
    pass

class Employee(EmployeeBase):
    id: UUID

    class Config:
        from_attributes = True
