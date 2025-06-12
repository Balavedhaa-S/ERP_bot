# app/crud.py

from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models import Asset, Vendor, MaintenanceLog, AssetVendorLink, Employee, Department
from app.schemas import AssetCreate, VendorCreate, MaintenanceLogCreate, AssetVendorLinkCreate

# ------------------------ Asset CRUD ------------------------
def create_asset(db: Session, asset: AssetCreate):
    db_asset = Asset(**asset.dict())
    db.add(db_asset)
    db.commit()
    db.refresh(db_asset)
    return db_asset

def get_asset(db: Session, asset_id: int):
    asset = db.query(Asset).filter(Asset.id == asset_id).first()
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    return asset

def update_asset(db: Session, asset_id: int, updated_data: dict):
    db_asset = db.query(Asset).filter(Asset.id == asset_id).first()
    if not db_asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    for key, value in updated_data.items():
        setattr(db_asset, key, value)
    db.commit()
    return db_asset

def delete_asset(db: Session, asset_id: int):
    db_asset = db.query(Asset).filter(Asset.id == asset_id).first()
    if not db_asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    db.delete(db_asset)
    db.commit()
    return {"msg": "Deleted successfully"}

# ------------------------ Vendor CRUD ------------------------
def create_vendor(db: Session, vendor: VendorCreate):
    db_vendor = Vendor(**vendor.dict())
    db.add(db_vendor)
    db.commit()
    db.refresh(db_vendor)
    return db_vendor

def get_vendors(db: Session):
    return db.query(Vendor).all()

# ------------------------ Maintenance Log CRUD ------------------------
def create_maintenance_log(db: Session, log: MaintenanceLogCreate):
    db_log = MaintenanceLog(**log.dict())
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log

def get_maintenance_logs(db: Session, asset_id: int):
    return db.query(MaintenanceLog).filter(MaintenanceLog.asset_id == asset_id).all()

# ------------------------ Asset-Vendor Link CRUD ------------------------
def create_asset_vendor_link(db: Session, link: AssetVendorLinkCreate):
    db_link = AssetVendorLink(**link.dict())
    db.add(db_link)
    db.commit()
    db.refresh(db_link)
    return db_link

def update_asset_vendor_link(db: Session, link_id: int, updated_data: dict):
    db_link = db.query(AssetVendorLink).filter(AssetVendorLink.id == link_id).first()
    if not db_link:
        raise HTTPException(status_code=404, detail="Link not found")
    for key, value in updated_data.items():
        setattr(db_link, key, value)
    db.commit()
    db.refresh(db_link)
    return db_link

def delete_asset_vendor_link(db: Session, link_id: int):
    db_link = db.query(AssetVendorLink).filter(AssetVendorLink.id == link_id).first()
    if not db_link:
        raise HTTPException(status_code=404, detail="Link not found")
    db.delete(db_link)
    db.commit()
    return {"msg": "Asset-Vendor link deleted successfully"}

# ------------------------ Custom Queries ------------------------
def get_assets_under_maintenance_by_location(db: Session, location: str):
    return db.query(Asset).filter(Asset.status == "Under Maintenance", Asset.location == location).all()

def get_service_history_by_asset(db: Session, asset_tag: str):
    asset = db.query(Asset).filter(Asset.asset_tag == asset_tag).first()
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    return db.query(AssetVendorLink).filter(AssetVendorLink.asset_id == asset.id).all()

def get_last_service_for_asset(db: Session, asset_id: int):
    return db.query(AssetVendorLink).filter(AssetVendorLink.asset_id == asset_id).order_by(AssetVendorLink.last_service_date.desc()).first()

def get_department_head(db: Session, dept_name: str):
    return db.query(Employee).join(Department).filter(
        Department.name == dept_name,
        Employee.designation.ilike("Head%")
    ).first()

def get_vendor_for_asset(db: Session, asset_tag: str):
    asset = db.query(Asset).filter(Asset.asset_tag == asset_tag).first()
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    return db.query(Vendor).join(AssetVendorLink).filter(AssetVendorLink.asset_id == asset.id).first()

def get_assets_assigned_to_employee(db: Session, employee_name: str):
    return db.query(Asset).join(Employee).filter(Employee.name == employee_name).all()