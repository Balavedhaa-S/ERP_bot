from pydantic import BaseModel

class AssetVendorLinkBase(BaseModel):
    asset_id: int
    vendor_id: int

class AssetVendorLinkCreate(AssetVendorLinkBase):
    pass

class AssetVendorLinkResponse(AssetVendorLinkBase):
    id: int

    class Config:
        from_attributes = True 
