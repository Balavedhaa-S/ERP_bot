from sqlalchemy.orm import Session
from app import models, schemas
import uuid

# Department CRUD
def create_department(db: Session, department: schemas.DepartmentCreate):
    db_dept = models.Department(
        id=uuid.uuid4(),
        name=department.name,
        head_id=department.head_id
    )
    db.add(db_dept)
    db.commit()
    db.refresh(db_dept)
    return db_dept

def get_department(db: Session, dept_id: uuid.UUID):
    return db.query(models.Department).filter(models.Department.id == dept_id).first()

def get_departments(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Department).offset(skip).limit(limit).all()


# Employee CRUD
def create_employee(db: Session, employee: schemas.EmployeeCreate):
    db_emp = models.Employee(
        id=uuid.uuid4(),
        name=employee.name,
        email=employee.email,
        department_id=employee.department_id,
        designation=employee.designation,
        date_joined=employee.date_joined
    )
    db.add(db_emp)
    db.commit()
    db.refresh(db_emp)
    return db_emp

def get_employee(db: Session, emp_id: uuid.UUID):
    return db.query(models.Employee).filter(models.Employee.id == emp_id).first()

def get_employees(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Employee).offset(skip).limit(limit).all()


# Asset CRUD
def create_asset(db: Session, asset: schemas.AssetCreate):
    db_asset = models.Asset(
        asset_tag=asset.asset_tag,
        name=asset.name,
        category=asset.category,
        location=asset.location,
        purchase_date=asset.purchase_date,
        warranty_until=asset.warranty_until,
        assigned_to=asset.assigned_to,
        department_id=asset.department_id,
        status=asset.status
    )
    db.add(db_asset)
    db.commit()
    db.refresh(db_asset)
    return db_asset

def get_asset(db: Session, asset_id: int):
    return db.query(models.Asset).filter(models.Asset.id == asset_id).first()

def get_assets(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Asset).offset(skip).limit(limit).all()
