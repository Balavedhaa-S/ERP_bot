from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, crud
from app.database import get_db
import uuid

router = APIRouter(prefix="/departments", tags=["departments"])

@router.post("/", response_model=schemas.Department)
def create_department(dept: schemas.DepartmentCreate, db: Session = Depends(get_db)):
    return crud.create_department(db=db, department=dept)

@router.get("/", response_model=list[schemas.Department])
def read_departments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_departments(db=db, skip=skip, limit=limit)

@router.get("/{dept_id}", response_model=schemas.Department)
def read_department(dept_id: uuid.UUID, db: Session = Depends(get_db)):
    db_dept = crud.get_department(db, dept_id=dept_id)
    if db_dept is None:
        raise HTTPException(status_code=404, detail="Department not found")
    return db_dept
