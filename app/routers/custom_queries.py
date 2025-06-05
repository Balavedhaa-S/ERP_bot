# app/routers/custom_queries.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app import schemas, crud
from app.database import get_db

router = APIRouter(prefix="/custom", tags=["custom"])

@router.get("/assets-under-maintenance/{location}", response_model=List[schemas.Asset])
def get_assets_under_maintenance(location: str, db: Session = Depends(get_db)):
    return crud.get_assets_under_maintenance_by_location(db, location)

@router.get("/service-history/{asset_tag}", response_model=List[schemas.AssetVendorLink])
def get_service_history(asset_tag: str, db: Session = Depends(get_db)):
    return crud.get_service_history_by_asset(db, asset_tag)

@router.get("/last-service/{asset_id}", response_model=schemas.AssetVendorLink)
def get_last_service(asset_id: int, db: Session = Depends(get_db)):
    result = crud.get_last_service_for_asset(db, asset_id)
    if result is None:
        raise HTTPException(status_code=404, detail="No service record found")
    return result

@router.get("/department-head/{dept_name}")
def get_department_head(dept_name: str, db: Session = Depends(get_db)):
    result = crud.get_department_head(db, dept_name)
    if not result:
        raise HTTPException(status_code=404, detail="No department head found")
    return {"name": result.name, "email": result.email}

@router.get("/vendor-for-asset/{asset_tag}")
def get_vendor_for_asset(asset_tag: str, db: Session = Depends(get_db)):
    result = crud.get_vendor_for_asset(db, asset_tag)
    if not result:
        raise HTTPException(status_code=404, detail="No vendor found for asset")
    return {"vendor_name": result.name, "email": result.email}

@router.get("/assets-assigned-to/{employee_name}", response_model=List[schemas.Asset])
def get_assets_assigned_to(employee_name: str, db: Session = Depends(get_db)):
    return crud.get_assets_assigned_to_employee(db, employee_name)
