from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List
from app import models, schemas, crud
from app.database import get_db

router = APIRouter(prefix="/assets", tags=["assets"])

@router.post("/", response_model=schemas.Asset)
def create_asset(asset: schemas.AssetCreate, db: Session = Depends(get_db)):
    return crud.create_asset(db=db, asset=asset)

@router.get("/", response_model=List[schemas.Asset])
def read_assets(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_assets(db=db, skip=skip, limit=limit)

@router.get("/{asset_id}", response_model=schemas.Asset)
def read_asset(asset_id: UUID, db: Session = Depends(get_db)):
    db_asset = crud.get_asset(db, asset_id=asset_id)
    if db_asset is None:
        raise HTTPException(status_code=404, detail="Asset not found")
    return db_asset

@router.put("/{asset_id}", response_model=schemas.Asset)
def update_asset(asset_id: UUID, asset: schemas.AssetUpdate, db: Session = Depends(get_db)):
    db_asset = crud.get_asset(db, asset_id=asset_id)
    if db_asset is None:
        raise HTTPException(status_code=404, detail="Asset not found")
    return crud.update_asset(db=db, asset_id=asset_id, asset_update=asset)

@router.delete("/{asset_id}")
def delete_asset(asset_id: UUID, db: Session = Depends(get_db)):
    db_asset = crud.get_asset(db, asset_id=asset_id)
    if db_asset is None:
        raise HTTPException(status_code=404, detail="Asset not found")
    crud.delete_asset(db=db, asset_id=asset_id)
    return {"message": "Asset deleted successfully"}