from langchain.chains import RetrievalQA
#from langchain.chat_models import ChatOpenAI
from vectorstore import get_vectorstore
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAI, ChatOpenAI

def get_qa_chain():
    retriever = get_vectorstore().as_retriever(search_kwargs={"k": 5})
    return RetrievalQA.from_chain_type(
        llm=ChatOpenAI(temperature=0),
        retriever=retriever,
        chain_type="stuff"
    )
