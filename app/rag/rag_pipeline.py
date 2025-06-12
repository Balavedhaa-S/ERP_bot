import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

from langchain.text_splitter import CharacterTextSplitter
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain_core.documents import Document

# Load env vars
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
db_url = os.getenv("DATABASE_URL")

# Prepare FAISS docs from your asset_table
def build_documents_from_db():
    engine = create_engine(db_url)
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM asset_table"))  # Update if needed
        rows = result.fetchall()
        columns = result.keys()
        docs = []
        for row in rows:
            row_dict = dict(zip(columns, row))
            content = ". ".join([f"{col}: {val}" for col, val in row_dict.items()])
            docs.append(Document(page_content=content, metadata={"source": "asset_table"}))
    return docs

# Build conversational chain
def get_conversational_qa():
    documents = build_documents_from_db()

    # Split and embed
    text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=20)
    split_docs = text_splitter.split_documents(documents)
    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
    vectorstore = FAISS.from_documents(split_docs, embeddings)

    retriever = vectorstore.as_retriever(search_type="similarity", k=3)

    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    llm = ChatOpenAI(model_name="gpt-4o", temperature=0, openai_api_key=openai_api_key)

    qa_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=memory,
        verbose=True
    )
    return qa_chain
