schema_docs = {
    "Departments": (
        "The Departments table holds information about different departments "
        "within the company. Each department has a unique ID, a name, and the "
        "name of the department head responsible for operations."
    ),
    "Employees": (
        "This table stores details about employees, including their unique ID, "
        "full name, official email, job title, date of joining, and which "
        "department they belong to."
    ),
    "Assets": (
        "Assets table contains all company assets such as asset tag, name, category "
        "(e.g., laptop), location, purchase date, warranty, status, owner department, "
        "and assigned employee."
    ),
    "Maintenance_Logs": (
        "This records all maintenance activities related to assets. Each log includes "
        "a log ID, asset ID, issue, status, reporter, technician, and resolution date."
    ),
    "Vendors": (
        "The Vendors table contains info about vendors providing services/products. "
        "Includes name, contact person, email, phone, and address."
    ),
    "Asset_Vendor_Link": (
        "A linking table mapping assets to vendors. Specifies service type and "
        "last service date."
    )
}
