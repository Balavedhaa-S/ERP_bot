from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from vectorstore import get_vectorstore

def get_qa_chain():
    retriever = get_vectorstore().as_retriever(search_kwargs={"k": 5})
    return RetrievalQA.from_chain_type(
        llm=ChatOpenAI(temperature=0),
        retriever=retriever,
        chain_type="stuff"
    )
