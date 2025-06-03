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
    class Config:
        json_schema_extra = {
            "example": {
                "name": "John Doe",
                "email": "john.doe@example.com",
                "department_id": "123e4567-e89b-12d3-a456-426614174001",
                "designation": "Software Engineer",
                "date_joined": "2023-08-15"
            }
        }

class EmployeeUpdate(BaseModel):
    name: Optional[str]
    email: Optional[str]
    department_id: Optional[UUID]
    designation: Optional[str]
    date_joined: Optional[date]

    class Config:
        json_schema_extra = {
            "example": {
                "name": "John Updated",
                "email": "updated.email@example.com",
                "department_id": "123e4567-e89b-12d3-a456-426614174001",
                "designation": "Senior Engineer",
                "date_joined": "2024-01-01"
            }
        }



class Employee(EmployeeBase):
    id: UUID

    class Config:
        from_attributes = True

class EmployeeResponse(Employee):
    department_name: Optional[str]
    
    class Config:
        from_attributes = True