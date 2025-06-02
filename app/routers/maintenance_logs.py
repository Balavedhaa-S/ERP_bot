# app/routers/maintenance_logs.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.maintenance_logs import MaintenanceLog
from app.schemas.maintenance_logs import MaintenanceLogCreate, MaintenanceLogResponse

router = APIRouter(prefix="/maintenance", tags=["Maintenance Logs"])

@router.post("/", response_model=MaintenanceLogResponse)
def create_maintenance_log(log: MaintenanceLogCreate, db: Session = Depends(get_db)):
    db_log = MaintenanceLog(**log.dict())
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log

@router.get("/asset/{asset_id}", response_model=list[MaintenanceLogResponse])
def get_logs_for_asset(asset_id: int, db: Session = Depends(get_db)):
    logs = db.query(MaintenanceLog).filter(MaintenanceLog.asset_id == asset_id).all()
    return logs
