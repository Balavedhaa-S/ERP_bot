from pydantic import BaseModel
from typing import Optional

# Base class with common vendor fields
class VendorBase(BaseModel):
    name: str
    contact_email: Optional[str] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None

# Used when creating a vendor (e.g., in POST request)
class VendorCreate(VendorBase):
    pass

# Used when responding with a vendor (e.g., in GET response)
class VendorResponse(VendorBase):
    id: int

    class Config:
        from_attributes = True

# Optional alias schema (can be same as VendorResponse)
class Vendor(VendorResponse):
    pass
