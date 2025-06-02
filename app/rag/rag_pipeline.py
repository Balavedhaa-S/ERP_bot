from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
from langchain.text_splitter import CharacterTextSplitter

from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
db_url = os.getenv("DATABASE_URL")

# Step 0: Connect to PostgreSQL and fetch real data
engine = create_engine(db_url)

with engine.connect() as conn:
    result = conn.execute(text("SELECT * FROM asset_table"))  # Replace with your actual table
    rows = result.fetchall()
    columns = result.keys()
    
    # Convert each row to a descriptive string
    docs = []
    for row in rows:
        row_dict = dict(zip(columns, row))
        doc_str = ". ".join([f"{col}: {val}" for col, val in row_dict.items()])
        docs.append(doc_str)

# Step 1: Split documents
text_splitter = CharacterTextSplitter(chunk_size=300, chunk_overlap=20)
split_docs = text_splitter.split_text("\n".join(docs))

# Step 2: Create embeddings
embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)

# Step 3: Index with FAISS
doc_search = FAISS.from_texts(split_docs, embeddings)

# Step 4: Create RAG QA Chain
qa_chain = RetrievalQA.from_chain_type(
    llm=OpenAI(temperature=0, openai_api_key=openai_api_key),
    retriever=doc_search.as_retriever()
)

def ask_question(query: str):
    response = qa_chain.run(query)
    return response
