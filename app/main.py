from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
import uuid
import os

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Local app modules
from app.routers import assets, maintenance_logs
from app.data_loader import load_all_data
from app.rag_docs import prepare_documents
from app import models, schemas, crud
from app.database import engine, get_db,Base

# LangChain / OpenAI
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
from langchain_community.embeddings import OpenAIEmbeddings

# --- Initialize FastAPI ---
app = FastAPI(
    title="ERP Chatbot Backend",
    description="Assets, Maintenance, Departments, and Employees APIs with RAG Chatbot"
)

# --- Database Setup ---
Base.metadata.create_all(bind=engine)

# --- Routers for Assets & Maintenance ---
app.include_router(assets.router, prefix="/assets", tags=["Assets"])
app.include_router(maintenance_logs.router, prefix="/maintenance", tags=["Maintenance Logs"])

# --- FAISS + RAG Setup ---
openai_api_key = os.getenv("OPENAI_API_KEY")
embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)

# Load existing FAISS index
if os.path.exists("faiss_index"):
    doc_search = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
else:
    raise RuntimeError("FAISS index not found. Run embedding_faiss_rag.py first.")

# Initialize RAG chain
qa_chain = RetrievalQA.from_chain_type(
    llm=OpenAI(temperature=0, openai_api_key=openai_api_key),
    retriever=doc_search.as_retriever()
)

# Pydantic schema for chatbot query
class Question(BaseModel):
    query: str

# --- RAG Endpoint ---
@app.post("/ask/")
def ask(query: Question):
    response = qa_chain.run(query.query)
    return {"response": response}

# --- Root Endpoint ---
@app.get("/")
def root():
    return {"message": "🚀 ERP Chatbot backend is running!"}

# --- Department CRUD Endpoints ---
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

# --- Employee CRUD Endpoints ---
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
