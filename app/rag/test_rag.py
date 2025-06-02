from app.rag.rag_pipeline import ask_question

query = "When is the next maintenance for Asset A?"
answer = ask_question(query)
print("Answer:", answer)
