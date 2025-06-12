# 🧠 ERP Chatbot – Assets and Maintenance Module

## 📌 Project Overview

This project is a **backend module** for an **ERP-integrated AI chatbot** that allows natural language queries about company **assets, vendors, employees, departments, and maintenance logs**. It enables users to ask questions like "Who are in IT department?" or "List all assets under maintenance" and get real-time, natural-sounding answers backed by actual relational data.

## 🎯 Goal

Develop an intelligent backend system that uses **AI + RAG (Retrieval-Augmented Generation)** to process natural language questions and respond with **accurate, human-like answers** by fetching relevant data from a **PostgreSQL ERP database**.

---

## 🛠️ Technical Implementation Overview

### 🌐 API Development

* **Framework**: FastAPI
* **Responsibilities**:

  * Expose RESTful endpoints for chatbot interactions (e.g., `/ask`)
  * Support both sync/async requests

### 🗃️ Database Layer

* **Database**: PostgreSQL
* **ORM**: SQLAlchemy
* **Responsibilities**:

  * Define models for `employees`, `departments`, `assets`, `vendors`, etc.
  * Query ERP data securely and efficiently

### 📚 Retrieval-Augmented Generation (RAG)

* **Library**: LangChain
* **Responsibilities**:

  * Parse user queries
  * Use `ChatOpenAI` (GPT-3.5 / GPT-4.0 / GPT-4.1) for SQL generation
  * Combine LLM-generated insights with live PostgreSQL query results
  * Return natural, context-aware responses

### 🔍 Vector Search Integration

* **Vector DB**: FAISS (or Chroma alternative)
* **Responsibilities**:

  * Generate semantic embeddings (via `OpenAIEmbeddings`) for schema + example Q\&A
  * Retrieve top-k relevant chunks/documents per query for RAG context

### 🧠 Natural Language Understanding (NLU)

* **Responsibilities**:

  * Recognize intent and extract structured entities (e.g., department name, asset type)
  * Direct queries to either SQL chain or vector retriever

### ⚡ Caching Layer (Optional)

* **Cache**: Redis (optional)
* **Responsibilities**:

  * Store frequently asked questions and their results
  * Minimize response latency and reduce load on DB/LLM

### 🔄 Real-Time Communication (Optional)

* **Protocol**: Socket.IO with FastAPI WebSockets
* **Responsibilities**:

  * Provide real-time status updates like "Generating SQL..."
  * Allow continuous chat experience (typing, follow-up context)

### 💻 Frontend Integration

* **Frontend**: React.js chatbot UI
* **Responsibilities**:

  * Handle chat input/output
  * Connect to REST endpoints (e.g., `/ask`)
  * Support real-time updates via WebSocket (optional)

---

## 📂 Project Structure

```
ERP-CHATBOT-BACKEND/
├── app/
│   ├── models/              # SQLAlchemy models
│   ├── routers/             # FastAPI routers (ask.py, assets.py, etc.)
│   ├── rag/                 # LangChain logic (RAG, SQL chain, embeddings)
│   ├── schemas/             # Pydantic schemas
│   ├── utils/               # Helpers: NLP, DB setup, vector store, etc.
├── faiss_index/             # FAISS vector store index files
├── create_tables.py         # DB model creation script
├── embedding_faiss_rag.py   # Embedding + FAISS index builder
├── requirements.txt         # Python dependencies
├── .env                     # Environment variables (DB, API keys)
└── main.py                  # FastAPI app entry point
```

---

## 🚀 How It Works

1. **User asks a question** → e.g., "Who are in IT department?"
2. **NLP + SQL Chain**:

   * Recognizes intent and relevant entity (`department = IT`)
   * Uses GPT-4 to generate dynamic SQL:

     ```sql
     SELECT name, email FROM employees WHERE department_id='XYZ'
     ```
3. **Query Execution**:

   * SQL runs against PostgreSQL via SQLAlchemy
   * Results are converted into a **natural language** answer

     > "People working in IT department are Nisha Roy, Manish Singh, and Vikram Desai."
4. **Fallback**:

   * If no SQL can be generated, fallback to FAISS RAG (LangChain) for document-style Q\&A

---

## ✅ Features

* ✅ Dynamic SQL generation from natural language
* ✅ LangChain + GPT-4 for RAG-based responses
* ✅ FAISS vectorstore for schema-aware retrieval
* ✅ PostgreSQL with normalized ERP data
* ✅ Modular FastAPI routers and schema definitions
* ✅ Support for natural, conversational answers

---

## 🧪 Sample Questions

* "List all assets in IT department"
* "Show employees who joined after 2022"
* "What assets are under maintenance?"
* "Who handles vendor Acme Corp?"

---

## 📦 Setup Instructions

```bash
# Clone the repo
$ git clone https://github.com/your-username/erp-chatbot-backend.git
$ cd erp-chatbot-backend

# Create a virtual environment and activate it
$ python -m venv .venv
$ source .venv/bin/activate  # or .venv\Scripts\activate on Windows

# Install dependencies
$ pip install -r requirements.txt

# Set up environment variables
$ cp .env.example .env
# Fill in: DATABASE_URL, OPENAI_API_KEY, etc.

# Run DB table creation
$ python create_tables.py

# Build FAISS index
$ python embedding_faiss_rag.py

# Start the FastAPI server
$ uvicorn app.utils.main:app --reload
```

---

## 🧠 Credits

Built using:

* [FastAPI](https://fastapi.tiangolo.com)
* [LangChain](https://docs.langchain.com)
* [PostgreSQL](https://www.postgresql.org)
* [OpenAI GPT-4](https://platform.openai.com/docs)
* [FAISS](https://github.com/facebookresearch/faiss)
* [React.js Chatbot UI](https://github.com/mckaywrigley/chatbot-ui)

---

## 📬 Contact

If you have questions or want to contribute:

* 📧 Email: [balavedhaa.larklabsai@gmail.com]
* 💼 GitHub: [https://github.com/Balavedhaa-S]

---

> 🚀 *“Turning raw ERP data into smart conversations!”*
