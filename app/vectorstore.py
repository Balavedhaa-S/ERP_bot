from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
import os

# Load saved FAISS vectorstore from disk
def get_vectorstore():
    return FAISS.load_local("faiss_index", OpenAIEmbeddings())
