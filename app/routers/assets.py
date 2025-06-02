# app/routers/assets.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
#from app.schemas.assets import AssetCreate, AssetResponse
from app.schemas.assets import AssetCreate, AssetResponse
from app.models.assets import Asset
from app.database import get_db

router = APIRouter()

@router.post("/", response_model=AssetResponse)
def create_asset(asset: AssetCreate, db: Session = Depends(get_db)):
    db_asset = Asset(**asset.dict())
    db.add(db_asset)
    db.commit()
    db.refresh(db_asset)
    return db_asset
