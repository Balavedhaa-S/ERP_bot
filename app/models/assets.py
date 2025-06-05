#from sqlalchemy import Column, String, Integer, Date, Enum, ForeignKey
#from sqlalchemy.dialects.postgresql import UUID
#from app.models.base import Base
#from sqlalchemy.orm import relationship
#class Asset(Base):
    #__tablename__ = "assets"
    #id = Column(Integer, primary_key=True, autoincrement=True)
    #asset_tag = Column(String, unique=True)
    #name = Column(String)
    #category = Column(String)
    #location = Column(String)
    #purchase_date = Column(Date)
    #warranty_until = Column(Date)

    # ✅ Use UUID here to match employees.id and departments.id
    #assigned_to = Column(UUID, ForeignKey("employees.id"))
    #department_id = Column(UUID, ForeignKey("departments.id"))

    #status = Column(Enum("In Use", "Under Maintenance", "Retired", name="status_enum"))

from sqlalchemy import Column, String, Integer, Date, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.models.base import Base
from app.models.employees import Employee 
class Asset(Base):
    __tablename__ = "assets"

    id = Column(Integer, primary_key=True, autoincrement=True)
    asset_tag = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    category = Column(String)
    location = Column(String)
    purchase_date = Column(Date)
    warranty_until = Column(Date)

    assigned_to = Column(UUID(as_uuid=True), ForeignKey("employees.id"))
    department_id = Column(UUID(as_uuid=True), ForeignKey("departments.id"))

    status = Column(
        Enum("In Use", "Under Maintenance", "Retired", name="status_enum"),
        default="In Use",
        nullable=False,
    )

    # Relationship back to Employee
    employee = relationship("Employee", back_populates="assets")
    maintenance_logs = relationship("MaintenanceLog", back_populates="assets", cascade="all, delete-orphan")
    vendor_links = relationship("AssetVendorLink", back_populates="asset")