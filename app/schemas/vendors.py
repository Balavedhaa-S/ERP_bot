from pydantic import BaseModel
from typing import Optional
#from .vendors import VendorCreate, VendorResponse

class VendorBase(BaseModel):
    name: str
    contact_email: Optional[str] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None

class VendorCreate(VendorBase):
    pass

class VendorResponse(VendorBase):
    id: int

    class Config:
       from_attributes = True 
