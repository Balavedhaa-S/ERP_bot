from fastapi import FastAPI, Depends, HTTPException 
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session
import uuid
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

from app.rag.sql_chain import run_sql_chain
from app.routers.ask import router as ask_router
from app.routers import (
    asset_vendor_link,
    assets,
    ask,
    departments,
    employees,
    maintenance_logs,
    vendors,
    custom_queries,
)
from app.data_loader import load_all_data
from app.rag_docs import prepare_documents
from app import models, schemas, crud
from app.database import engine, get_db, Base
from app.models.base import Base
from app.utils.exception_handler import validation_exception_handler

load_dotenv()

# --- App & CORS Setup ---
origins = ["http://localhost:5173"]

app = FastAPI(
    title="ERP Chatbot Backend",
    description="ERP backend with chatbot RAG functionality",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Database Setup ---
Base.metadata.create_all(bind=engine)

# --- Include Routers ---
app.include_router(assets.router, prefix="/assets", tags=["Assets"])
app.include_router(maintenance_logs.router, prefix="/maintenance", tags=["Maintenance Logs"])
app.include_router(employees.router, prefix="/employees", tags=["Employees"])
app.include_router(vendors.router, prefix="/vendors", tags=["Vendors"])
app.include_router(departments.router, prefix="/departments", tags=["Departments"])
app.include_router(asset_vendor_link.router, prefix="/asset-vendor", tags=["Asset Vendor Links"])
app.include_router(ask_router, prefix="/chat", tags=["Chatbot"])

# --- FAISS + LangChain Setup ---
from langchain.chains import RetrievalQA
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAI

openai_api_key = os.getenv("OPENAI_API_KEY")
doc_search = None
qa_chain = None

def run_langchain_bot(query: str) -> str:
    if qa_chain is None:
        return "RAG model not ready. Please run the embedding script first."
    try:
        return qa_chain.run(query)
    except Exception as e:
        return f"⚠️ Error: {str(e)}"

@app.on_event("startup")
def load_faiss_index():
    global doc_search, qa_chain
    if os.path.exists("faiss_index"):
        embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
        doc_search = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
        qa_chain = RetrievalQA.from_chain_type(
            llm=OpenAI(temperature=0, openai_api_key=openai_api_key),
            retriever=doc_search.as_retriever()
        )
        print("✅ FAISS index loaded successfully.")
    else:
        print("⚠️ WARNING: FAISS index not found. Run embedding_faiss_rag.py first.")

# --- RAG Chat Endpoints ---
class Question(BaseModel):
    query: str

@app.post("/ask/")
def ask(query: Question):
    response = run_langchain_bot(query.query)
    return {"response": response}

class ChatRequest(BaseModel):
    query: str

@app.post("/chatbot")
async def chatbot_endpoint(request: ChatRequest):
    if qa_chain is None:
        raise HTTPException(status_code=503, detail="Chatbot not ready. FAISS index not loaded.")
    response = qa_chain.run(request.query)
    return {"response": response}

# --- New Chat + SQL Chain Endpoint ---
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL environment variable not set!")

engine_sql = create_engine(DATABASE_URL)
SessionLocal_sql = sessionmaker(autocommit=False, autoflush=False, bind=engine_sql)

class ChatSQLRequest(BaseModel):
    query: str

@app.post("/chat")
async def chat_sql(request: ChatSQLRequest):
    try:
        response = run_sql_chain(request.query)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"❌ SQL generation failed: {e}")

# --- Static NL → SQL logic (commented out) ---
# def generate_sql_from_query(nl_query: str) -> str | None:
#     nl = nl_query.lower()
#     if "laptop" in nl and "it department" in nl:
#         return """
#         SELECT asset_tag, name, category, location 
#         FROM assets 
#         WHERE category ILIKE '%laptop%' 
#         AND department_id = (
#             SELECT id FROM departments WHERE name ILIKE 'IT'
#         );
#         """
#     if "details" in nl and "gen-001" in nl:
#         return "SELECT * FROM assets WHERE asset_tag = 'GEN-001';"
#     if "list all assets assigned to the it department" in nl:
#         return """
#         SELECT * FROM assets WHERE department_id = (
#             SELECT id FROM departments WHERE name ILIKE 'IT'
#         );
#         """
#     if "employees in it department" in nl or "who are the employees in it" in nl:
#         return """
#         SELECT e.id, e.name, e.email
#         FROM employees e
#         WHERE e.department_id = (
#             SELECT id FROM departments WHERE name ILIKE 'IT'
#         );
#         """
#     if "assets assigned to priya" in nl or "assets of priya" in nl or "assigned to priya nair" in nl:
#         return """
#         SELECT a.asset_tag, a.name, a.category, a.location
#         FROM assets a
#         JOIN employees e ON a.assigned_to = e.id
#         WHERE e.name ILIKE '%Priya Nair%';
#         """
#     if "vendor" in nl and "linked to asset" in nl:
#         return """
#         SELECT v.name, v.contact_info
#         FROM vendors v
#         JOIN asset_vendor_link avl ON v.id = avl.vendor_id
#         WHERE avl.asset_tag = 'CAM-006';
#         """
#     if "employees who joined after" in nl:
#         return "SELECT * FROM employees WHERE date_joined > '2022-01-01';"
#     return None

# --- Core CRUD Endpoints ---
@app.get("/")
def root():
    return {"message": "🚀 ERP Chatbot backend is running!"}

@app.post("/departments/", response_model=schemas.Department)
def create_department(department: schemas.DepartmentCreate, db: Session = Depends(get_db)):
    return crud.create_department(db, department)

@app.get("/departments/{dept_id}", response_model=schemas.Department)
def read_department(dept_id: uuid.UUID, db: Session = Depends(get_db)):
    db_dept = crud.get_department(db, dept_id)
    if not db_dept:
        raise HTTPException(status_code=404, detail="Department not found")
    return db_dept

@app.get("/departments/", response_model=list[schemas.Department])
def read_departments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_departments(db, skip=skip, limit=limit)

@app.post("/employees/", response_model=schemas.Employee)
def create_employee(employee: schemas.EmployeeCreate, db: Session = Depends(get_db)):
    return crud.create_employee(db, employee)

@app.get("/employees/{emp_id}", response_model=schemas.Employee)
def read_employee(emp_id: uuid.UUID, db: Session = Depends(get_db)):
    db_emp = crud.get_employee(db, emp_id)
    if not db_emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    return db_emp

@app.get("/employees/", response_model=list[schemas.Employee])
def read_employees(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_employees(db, skip=skip, limit=limit)

@app.get("/health", tags=["System"])
def health_check():
    return {"status": "ok"}

# --- Error Handling ---
app.add_exception_handler(RequestValidationError, validation_exception_handler)

# --- Run Server (Standalone) ---
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
