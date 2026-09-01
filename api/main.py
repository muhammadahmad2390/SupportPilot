from fastapi import FastAPI
from pydantic import BaseModel

class ChatRequest(BaseModel):
    conversation_id:str
    customer_id:str
    message:str

app = FastAPI()

@app.post('/chat')
def chat(req: ChatRequest):
    return {'message':'working fine'}