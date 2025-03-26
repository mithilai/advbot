from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from retriever import retrieve_answer  # Your chatbot logic function

app = FastAPI()

# Request Model
class ChatRequest(BaseModel):
    message: str
    history: list[list[str]] = []  # Default to empty history if not provided

# Response Model
class ChatResponse(BaseModel):
    response: str

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    user_message = request.message
    history = request.history

    # Handle empty or missing history gracefully
    if not history:
        history = [["Advaidh", "Hello! How can I help you today?"]]

    try:
        # Pass the chat history to the chatbot
        bot_response = retrieve_answer(user_message, history)
        return {"response": bot_response}
    except Exception as e:
        print(f"❌ Internal Server Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

