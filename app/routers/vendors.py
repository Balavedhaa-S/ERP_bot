from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app import schemas, crud
from app.database import get_db

router = APIRouter(prefix="/vendors", tags=["vendors"])

@router.post("/", response_model=schemas.Vendor)
def create_vendor(vendor: schemas.VendorCreate, db: Session = Depends(get_db)):
    return crud.create_vendor(db=db, vendor=vendor)

@router.get("/", response_model=List[schemas.Vendor])
def get_vendors(db: Session = Depends(get_db)):
    return crud.get_vendors(db=db)
