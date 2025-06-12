import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from langchain_core.documents import Document
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.text_splitter import CharacterTextSplitter

from app.rag.schema_doc import schema_docs

# ------------------------------
# 1. Load environment variables
# ------------------------------
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
DATABASE_URL = os.getenv("DATABASE_URL")

# ------------------------------
# 2. Connect to PostgreSQL
# ------------------------------
engine = create_engine(DATABASE_URL)

# ------------------------------
# 3. Load all relevant tables
# ------------------------------
assets_df = pd.read_sql("SELECT * FROM assets", engine)
departments_df = pd.read_sql("SELECT * FROM departments", engine)
maintenance_df = pd.read_sql("SELECT * FROM maintenance_logs", engine)
employees_df = pd.read_sql("SELECT * FROM employees", engine)
vendors_df = pd.read_sql("SELECT * FROM vendors", engine)
asset_vendor_link_df = pd.read_sql("SELECT * FROM asset_vendor_link", engine)

# ------------------------------
# 4. Create LangChain Documents from tables
# ------------------------------
documents = [
    Document(page_content=assets_df.to_string(), metadata={"source": "Assets Table"}),
    Document(page_content=departments_df.to_string(), metadata={"source": "Departments Table"}),
    Document(page_content=maintenance_df.to_string(), metadata={"source": "Maintenance Logs Table"}),
    Document(page_content=employees_df.to_string(), metadata={"source": "Employees Table"}),
    Document(page_content=vendors_df.to_string(), metadata={"source": "Vendors Table"}),
    Document(page_content=asset_vendor_link_df.to_string(), metadata={"source": "Asset-Vendor Link Table"}),
]

# ------------------------------
# 5. Add schema_docs as context
# ------------------------------
for table, description in schema_docs.items():
    documents.append(Document(page_content=f"{table}:\n{description}", metadata={"source": "Schema"}))

# ------------------------------
# 6. Add natural language example queries
# ------------------------------
sample_questions = [
    "Which department does Priya Nair belong to?",
    "List all employees in the IT department.",
    "Get details of the asset with tag GEN-001.",
    "Show all assets currently under maintenance.",
    "Give me all assets assigned to Priya Nair.",
    "List assets located in the Server Room.",
    "Who is assigned to asset AC-002?",
    "Show employees who joined after 2022-01-01.",
    "List all assets in the Power category.",
    "Which vendor is linked to asset CAM-006?",
]
documents.extend([
    Document(page_content=q, metadata={"source": "Sample Query"}) for q in sample_questions
])

# ------------------------------
# 7. Initialize OpenAI Embeddings
# ------------------------------
embeddings_model = OpenAIEmbeddings(openai_api_key=openai_api_key)

# ------------------------------
# 8. Split documents and create vector store
# ------------------------------
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
split_docs = text_splitter.split_documents(documents)

vector_store = FAISS.from_documents(split_docs, embeddings_model)

# Save FAISS index
vector_store.save_local("faiss_index")

# ------------------------------
# 9. Setup RetrievalQA Chain
# ------------------------------
llm = ChatOpenAI(
    temperature=0,
    openai_api_key=openai_api_key,
    model_name="gpt-4.1"  # or "gpt-4"
)

qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=vector_store.as_retriever(search_type="similarity", k=3),
    return_source_documents=False
)

# ------------------------------
# 10. Query function to use in your API
# ------------------------------
def run_langchain_bot(query: str, db: Session) -> str:
    try:
        answer = qa_chain.run(query)
        return answer
    except Exception as e:
        return f"⚠️ Error: {str(e)}"