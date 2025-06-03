from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import schemas, crud
from app.database import get_db

router = APIRouter(prefix="/asset-vendor-links", tags=["asset-vendor-links"])

@router.post("/", response_model=schemas.AssetVendorLink)
def create_asset_vendor_link(link: schemas.AssetVendorLinkCreate, db: Session = Depends(get_db)):
    return crud.create_asset_vendor_link(db=db, link=link)
