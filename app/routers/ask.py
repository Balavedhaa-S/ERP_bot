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

@router.post("/ask")
async def ask_chatbot(req: QueryRequest, db: Session = Depends(get_db)):
    # Generate SQL from natural language query using your nlp_sql.py
    sql = generate_sql(req.query)

    if sql:
        logging.info(f"Generated SQL:\n{sql}")  # Log the generated SQL query
        try:
            # Execute the generated SQL safely
            result = db.execute(text(sql))
            rows = result.fetchall()
            if not rows:
                return {"response": "No matching records found."}

            # Format the results as list of dicts (JSON serializable)
            records = [dict(row._mapping) for row in rows]

            return {"response": records}

        except Exception as e:
            logging.error(f"SQL Execution Error: {str(e)}")
            raise HTTPException(status_code=400, detail=f"SQL Execution Error: {str(e)}")

    else:
        # Fallback: Use your existing FAISS + LangChain chatbot
        try:
            from langchain.chains import RetrievalQA
            from langchain_community.chat_models import ChatOpenAI
            from langchain_community.vectorstores import FAISS
            from langchain_community.embeddings import OpenAIEmbeddings

            embedding = OpenAIEmbeddings()
            vectorstore = FAISS.load_local(
                "faiss_index",
                embedding,
                allow_dangerous_deserialization=True
            )
            retriever = vectorstore.as_retriever(search_type="similarity", k=2)
            qa_chain = RetrievalQA.from_chain_type(
                llm=ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo"),
                retriever=retriever,
                return_source_documents=False,
            )
            answer = qa_chain.run(req.query)
            return {"response": answer}
        except Exception as e:
            logging.error(f"FAISS/LLM Processing Error: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")
