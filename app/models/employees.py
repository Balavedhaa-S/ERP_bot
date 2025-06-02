# app/models/employees.py
#from sqlalchemy import Column, String, Date, ForeignKey
#from sqlalchemy.dialects.postgresql import UUID
#from app.models.base import Base
#from database import Base
#from models import Asset, Employee  # both models imported

#class Employee(Base):
    #__tablename__ = "employees"
    #id = Column(UUID, primary_key=True)
    #name = Column(String)
    #email = Column(String)
    #department_id = Column(UUID, ForeignKey("departments.id"))
    #designation = Column(String)
    #date_joined = Column(Date)


from sqlalchemy import Column, String, Date, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
#from database import Base
from app.models.base import Base   
#from app.models.employees import Employee

class Employee(Base):
    __tablename__ = "employees"

    id = Column(UUID(as_uuid=True), primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    department_id = Column(UUID(as_uuid=True), ForeignKey("departments.id"))
    designation = Column(String)
    date_joined = Column(Date)

    # Relationship to Asset using string reference
    assets = relationship("Asset", back_populates="employee")
