import google.generativeai as genai
from app.config import GOOGLE_API_KEY

# Configure Gemini
genai.configure(api_key=GOOGLE_API_KEY)

# Free working model
MODEL_NAME = "gemini-3-flash-preview"

def generate_answer(context: str, question: str, chat_history: str = ""):
    prompt = f"""
You are a helpful assistant.

Conversation history:
{chat_history}

Answer ONLY using the context below.
If the answer is not present, say "I don't know".

Context:
{context}

Question:
{question}
"""

    model = genai.GenerativeModel(MODEL_NAME)
    response = model.generate_content(prompt)

    return response.text
