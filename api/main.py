from fastapi import FastAPI
from pydantic import BaseModel
from agent.core import agent
from agent.core import ConversationContext
from agent.policy_sync import sync_policy, delete_policy


class ChatRequest(BaseModel):
    conversation_id:str
    customer_id:str
    message:str

class UpdatePolicyRequest(BaseModel):
    policy_id: str
    title: str
    content: str
class DeletePolicyRequest(BaseModel):
    policy_id: str



app = FastAPI()

@app.post('/chat')
def chat(req: ChatRequest):
    thread_config = {'configurable': {"thread_id": req.conversation_id}}
    agent_response = agent.invoke({'messages':[{'role':'user','content': req.message}]},
                                  thread_config,
                                  context = ConversationContext(conversation_id = req.conversation_id)
                                  )
    # escalated = agent_response.get('escalated',False)
    for m in agent_response['messages']:
     print(m.pretty_print())
    last_message = agent_response['messages'][-1].content
    
    return { 'reply': last_message }

@app.put('/update_policy')
def sync_policy_route(req: UpdatePolicyRequest)->dict:
   sync_policy(req.policy_id,req.title,req.content)
   return {'message': 'Policy updated successfully'}

@app.delete('/delete_policy/{policy_id}')
def delete_policy_route(req:DeletePolicyRequest)->dict:
   delete_policy(req.policy_id)
   return {'message': 'Policy deleted successfully'}
  