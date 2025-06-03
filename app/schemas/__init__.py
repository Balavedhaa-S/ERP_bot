from .departments import Department, DepartmentCreate
#from .employees import Employee, EmployeeCreate,EmployeeBase,EmployeeResponse
from .assets import Asset, AssetCreate,AssetResponse,AssetUpdate

from .maintenance_logs import MaintenanceLog, MaintenanceLogCreate,MaintenanceLogResponse
from .vendors import VendorResponse, VendorCreate           # add this
from .asset_vendor_link import AssetVendorLinkCreate,AssetVendorLinkResponse  # add this if you have this file
# app/schemas/__init__.py
from .employees import Employee, EmployeeCreate, EmployeeBase, EmployeeUpdate
