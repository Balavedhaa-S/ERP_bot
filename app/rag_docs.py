from langchain.text_splitter import CharacterTextSplitter

def prepare_documents(df):
    docs = []
    for _, row in df.iterrows():
        text = f"""
        Asset: {row.asset_name}
        Status: {row.asset_status}
        Purchase Date: {row.purchase_date}
        Assigned to: {row.employee_name}
        Department: {row.department_name}
        Issue: {row.issue_description}
        Issue Status: {row.maintenance_status}
        Resolved Date: {row.resolved_date}
        Vendor: {row.vendor_name}
        Vendor Email: {row.vendor_email}
        Service Type: {row.service_type}
        Last Service Date: {row.last_service_date}
        """
        docs.append(text.strip())

    text_splitter = CharacterTextSplitter(chunk_size=300, chunk_overlap=20)
    return text_splitter.split_text("\n".join(docs))