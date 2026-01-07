import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# --- App Configuration ---
app = FastAPI()

# Allow all origins for CORS (useful for development)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Knowledge Base ---
def load_knowledge_base():
    """Loads all .txt files from the knowledge_base directory."""
    knowledge = ""
    kb_path = 'knowledge_base'
    if not os.path.exists(kb_path):
        return "Error: La carpeta 'knowledge_base' no fue encontrada."
        
    for filename in os.listdir(kb_path):
        if filename.endswith(".txt"):
            with open(os.path.join(kb_path, filename), 'r', encoding='utf-8') as f:
                knowledge += f.read() + "\n---\n"
    return knowledge

# --- API Endpoints ---
@app.post("/ask")
async def ask_question(request: dict):
    """
    Receives a question, simulates a RAG query, and returns an answer.
    """
    user_question = request.get("question", "")
    if not user_question:
        return {"answer": "Por favor, haz una pregunta."}

    # 1. Load the knowledge from documents
    context = load_knowledge_base()

    # 2. Simulate the AI call (RAG)
    # In a real scenario, you would pass the context and question to an LLM API.
    # Here, we just show that we have the context and return a simulated response.
    
    # --- THIS IS THE SIMULATED PART ---
    # A real implementation would look something like:
    # response = openai.ChatCompletion.create(
    #     model="gpt-4",
    #     messages=[
    #         {"role": "system", "content": f"Eres un asistente de ProDig. Responde la pregunta del usuario basándote únicamente en este contexto: {context}"},
    #         {"role": "user", "content": user_question}
    #     ]
    # )
    # simulated_answer = response.choices[0].message.content
    # --- END OF SIMULATION ---

    simulated_answer = f"(Respuesta Simulada de IA) Basado en mis documentos, he encontrado información relevante para tu pregunta sobre '{user_question}'. La IA procesaría esta información para darte una respuesta completa."

    return {"answer": simulated_answer}

@app.get("/")
def read_root():
    return {"message": "El servidor del chatbot de ProDig está funcionando. Usa el endpoint /ask para hacer preguntas."}

# --- Main Execution ---
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
