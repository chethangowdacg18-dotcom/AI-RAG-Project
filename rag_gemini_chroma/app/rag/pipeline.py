from app.rag.retriever import retrieve_context
from app.rag.generator import generate_answer

def rag_pipeline(question: str, chat_history: str = ""):
    context = retrieve_context(question)
    answer = generate_answer(context, question, chat_history)
    return answer
