from pydantic import BaseModel
from datetime import date
from typing import Optional

class AssetVendorLinkBase(BaseModel):
    asset_id: int
    vendor_id: int
    service_type: str
    last_service_date: Optional[date]

class AssetVendorLinkCreate(AssetVendorLinkBase):
    pass

class AssetVendorLinkResponse(AssetVendorLinkBase):
    id: int

    class Config:
        from_attributes = True

# You can also alias it for FastAPI
class AssetVendorLink(AssetVendorLinkResponse):
    pass
