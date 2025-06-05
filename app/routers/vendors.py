from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
#from app import schemas, crud
from app.database import get_db
from app import crud
from app.schemas.vendors import Vendor, VendorCreate, VendorBase
#from app import schemas

router = APIRouter(prefix="/vendors", tags=["vendors"])

@router.post("/", response_model=Vendor)
def create_vendor(vendor: VendorCreate, db: Session = Depends(get_db)):
    return crud.create_vendor(db=db, vendor=vendor)

@router.get("/", response_model=List[Vendor])
def get_vendors(db: Session = Depends(get_db)):
    return crud.get_vendors(db=db)
