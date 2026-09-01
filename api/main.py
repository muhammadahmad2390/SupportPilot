from fastapi import FastAPI
from pydantic import BaseModel
from agent.core import agent
from agent.core import ConversationContext


class ChatRequest(BaseModel):
    conversation_id:str
    customer_id:str
    message:str

app = FastAPI()

@app.post('/chat')
def chat(req: ChatRequest):
    thread_config = {'configurable': {"thread_id": req.conversation_id}}
    agent_response = agent.invoke({'messages':[{'role':'user','content': req.message}]},
                                  thread_config,
                                  context = ConversationContext(conversation_id = req.conversation_id)
                                  )
    escalated = agent_response.get('escalated')
    last_message = agent_response['messages'][-1].content
    
    return { 'reply': last_message, 'escalated': escalated }
