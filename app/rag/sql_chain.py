# app/rag/sql_chain.py

import os
from dotenv import load_dotenv
from langchain_experimental.sql import SQLDatabaseChain  # ✅ updated import
from langchain_community.utilities import SQLDatabase
from langchain.chat_models import ChatOpenAI

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize database and LLM
db = SQLDatabase.from_uri(DATABASE_URL)
llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo", openai_api_key=OPENAI_API_KEY)

# SQL-to-NL chain
sql_chain = SQLDatabaseChain.from_llm(llm, db, verbose=True)

def run_sql_chain(nl_query: str) -> str:
    return sql_chain.run(nl_query)