import re
from typing import Optional, Dict

def extract_entities(nl_query: str) -> Dict[str, Optional[str]]:
    entities = {"department": None, "employee_name": None, "asset_tag": None, "date": None}

    # Match department (e.g., "HR department", "IT department")
    #dept_match = re.search(r"(\b[A-Z][a-zA-Z]+\b)\s+department", nl_query, re.IGNORECASE)
    dept_match = re.search(r"(?:department of\s+|in\s+)?([A-Z][a-z]+)\s*department?", nl_query, re.IGNORECASE)
    if dept_match:
        entities["department"] = dept_match.group(1)

    # Match employee name (e.g., "assigned to Priya Nair", "of Riya Kapoor")
    emp_match = re.search(r"(?:assigned to|of)\s+([A-Z][a-z]+\s+[A-Z][a-z]+)", nl_query)
    if emp_match:
        entities["employee_name"] = emp_match.group(1)

    # Match asset tag (e.g., CAM-006)
    asset_match = re.search(r"\b([A-Z]{2,}-\d+)\b", nl_query.upper())
    if asset_match:
        entities["asset_tag"] = asset_match.group(1)

    # Match date (e.g., "after 2022-01-01")
    date_match = re.search(r"\bafter\s+(\d{4}-\d{2}-\d{2})", nl_query.lower())
    if date_match:
        entities["date"] = date_match.group(1)

    print("Extracted entities:", entities)  # Debug log for testing
    return entities

def generate_sql(nl_query: str) -> str | None:
    nl_query = nl_query.lower()

    # 1. Employees in a department
    if "employees" in nl_query and "department" in nl_query:
        match = re.search(r"in (the )?(?P<dept>[\w\s]+) department", nl_query)
        if match:
            dept = match.group("dept").strip().title()
            return f"""
                SELECT e.id, e.name, e.email
                FROM employees e
                JOIN departments d ON e.department_id = d.id
                WHERE d.name = '{dept}'
            """

    # 2. Employees joined after a date
    if "employees" in nl_query and "after" in nl_query:
        match = re.search(r"after (\d{4}-\d{2}-\d{2})", nl_query)
        if match:
            date = match.group(1)
            return f"""
                SELECT * FROM employees
                WHERE date_joined > '{date}'
            """

    # 3. Asset by tag
    if "asset tag" in nl_query:
        match = re.search(r"asset tag ['\"]?([A-Z0-9\-]+)['\"]?", nl_query)
        if match:
            tag = match.group(1)
            return f"""
                SELECT * FROM assets
                WHERE asset_tag = '{tag}'
            """

    # 4. Assets in location
    if "assets" in nl_query and "located in" in nl_query:
        match = re.search(r"located in (the )?(?P<location>[\w\s]+)", nl_query)
        if match:
            location = match.group("location").strip().title()
            return f"""
                SELECT * FROM assets
                WHERE location = '{location}'
            """

    # 5. Head of department
    if "head of" in nl_query and "department" in nl_query:
        match = re.search(r"head of (the )?(?P<dept>[\w\s]+) department", nl_query)
        if match:
            dept = match.group("dept").strip().title()
            return f"""
                SELECT e.name, e.email
                FROM employees e
                JOIN departments d ON e.department_id = d.id
                WHERE d.name = '{dept}' AND e.designation ILIKE 'Head%'
            """

    # 6. Assets in IT department
    if "assets" in nl_query and "it department" in nl_query:
        return """
            SELECT a.*
            FROM assets a
            JOIN departments d ON a.department_id = d.id
            WHERE d.name = 'IT'
        """

    return None  # fallback to FAISS RAG if nothing matches