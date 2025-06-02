import pandas as pd
from app.db import engine

def load_all_data():
    query = """
    SELECT 
        a.name AS asset_name,
        a.status AS asset_status,
        a.purchase_date,
        e.name AS employee_name,
        d.name AS department_name,
        m.description AS issue_description,
        m.status AS maintenance_status,
        m.resolved_date,
        v.name AS vendor_name,
        v.email AS vendor_email,
        avl.service_type,
        avl.last_service_date
    FROM assets a
    LEFT JOIN employees e ON a.assigned_to = e.id
    LEFT JOIN departments d ON a.department_id = d.id
    LEFT JOIN maintenance_logs m ON m.asset_id = a.id
    LEFT JOIN asset_vendor_link avl ON avl.asset_id = a.id
    LEFT JOIN vendors v ON avl.vendor_id = v.id
    """
    df = pd.read_sql(query, engine)
    return df