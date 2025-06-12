from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import text
import logging

from app.database import get_db
from app.nlp_sql import generate_sql  # your entity extraction + SQL generator

router = APIRouter()

class QueryRequest(BaseModel):
    query: str

# Initialize in-memory history (temporary)
chat_history = []

@router.post("/ask")
async def ask_chatbot(req: QueryRequest, db: Session = Depends(get_db)):
    print("🔹 Received Query:", req.query)

    # Try SQL generation first
    sql = generate_sql(req.query)
    print("🔸 Generated SQL:", sql)

    if sql:
        logging.info(f"Generated SQL:\n{sql}")
        try:
            result = db.execute(text(sql))
            rows = result.fetchall()
            if not rows:
                return {"response": "No matching records found."}
            records = [dict(row._mapping) for row in rows]
            return {"response": records}
        except Exception as e:
            logging.error(f"SQL Execution Error: {str(e)}")
            raise HTTPException(status_code=400, detail=f"SQL Execution Error: {str(e)}")
    else:
        # Fallback to Conversational RAG
        try:
            from langchain.chains import ConversationalRetrievalChain
            from langchain.memory import ConversationBufferMemory
            from langchain_community.chat_models import ChatOpenAI
            from langchain_community.vectorstores import FAISS
            from langchain_community.embeddings import OpenAIEmbeddings

            # Load FAISS vectorstore
            embedding = OpenAIEmbeddings()
            vectorstore = FAISS.load_local(
                "faiss_index",
                embedding,
                allow_dangerous_deserialization=True
            )

            retriever = vectorstore.as_retriever(search_type="similarity", k=2)
            memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

            # Build Conversational Chain
            qa_chain = ConversationalRetrievalChain.from_llm(
                llm=ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo"),
                retriever=retriever,
                memory=memory
            )

            # Provide chat history and query
            response = qa_chain({
                "question": req.query,
                "chat_history": chat_history
            })

            # Append to chat history manually
            chat_history.append((req.query, response["answer"]))

            return {"response": response["answer"]}
        except Exception as e:
            logging.error(f"Conversational QA Error: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")
