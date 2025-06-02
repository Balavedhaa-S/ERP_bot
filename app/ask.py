from rag_chain import get_qa_chain

qa = get_qa_chain()

def ask_question(question: str) -> str:
    return qa.run(question)
