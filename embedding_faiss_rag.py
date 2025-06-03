# embedding_faiss_rag.py

import os
from dotenv import load_dotenv
#from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAI, ChatOpenAI

from dotenv import load_dotenv

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
# Initialize the embeddings model with the key
#embeddings_model = OpenAIEmbeddings(openai_api_key=openai_api_key)
# Load .env with your OpenAI API key
import pandas as pd
import psycopg2
from langchain_core.documents import Document

# Load environment and OpenAI key
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname="erp_chatbot",
    user="postgres",
    password="Admin!18",
    host="localhost",  # or your DB host
    port="5432"
)

# Load your tables
assets_df = pd.read_sql("SELECT * FROM assets", conn)
departments_df = pd.read_sql("SELECT * FROM departments", conn)
#maintenance_df = pd.read_sql("SELECT * FROM maintenance", conn)
maintenance_df = pd.read_sql("SELECT * FROM maintenance_logs", conn)


# Convert DataFrames to LangChain Document objects
documents = [
    Document(page_content=assets_df.to_string(), metadata={"source": "Assets Table"}),
    Document(page_content=departments_df.to_string(), metadata={"source": "Departments Table"}),
    Document(page_content=maintenance_df.to_string(), metadata={"source": "Maintenance Table"})
]


# Initialize OpenAI Embeddings
embeddings_model = OpenAIEmbeddings()

# Build FAISS vector store
#vector_store = FAISS.from_documents(docs, embeddings_model)
vector_store = FAISS.from_documents(documents, embeddings_model)


# Save FAISS index
vector_store.save_local("faiss_index")

# Load FAISS index later if needed
#loaded_store = FAISS.load_local("faiss_index", embeddings_model)
loaded_store = FAISS.load_local("faiss_index", embeddings_model, allow_dangerous_deserialization=True)

# Sample query
query = "Where is the Laptop located?"
docs_and_scores = loaded_store.similarity_search_with_score(query, k=2)

# Output
print("\nResults for Query:", query)
for doc, score in docs_and_scores:
    print(f"- Score: {score:.4f}, Content: {doc.page_content}")

#doc_search.save_local("faiss_index")
