from .departments import Department, DepartmentCreate
#from .employees import Employee, EmployeeCreate,EmployeeBase,EmployeeResponse
from .assets import Asset, AssetCreate,AssetResponse,AssetUpdate
from .asset_vendor_link import AssetVendorLink, AssetVendorLinkCreate, AssetVendorLinkResponse

from .maintenance_logs import MaintenanceLog, MaintenanceLogCreate,MaintenanceLogResponse
from .vendors import Vendor,VendorResponse, VendorCreate           # add this
#from .asset_vendor_link import AssetVendorLinkCreate,AssetVendorLinkResponse  # add this if you have this file
# app/schemas/__init__.py
from .employees import Employee, EmployeeCreate, EmployeeBase, EmployeeUpdate
