from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from retriever import retrieve_answer  # Assuming this is your chatbot logic function

app = FastAPI()

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    user_message = request.message
    try:
        bot_response = retrieve_answer(user_message)
        return {"response": bot_response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
