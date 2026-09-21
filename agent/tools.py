from db.connection import db
from datetime import datetime
from agent.policy_sync import vectorStore
from typing import List
from db.schemas import Ticket
from pydantic import ValidationError



def lookup_order(order_id:str)->dict:
  order = db.orders.find_one({"id":order_id})
  if order:
    order['_id'] = str(order['_id'])
    return order
  else:
    return {'error':'Order not found.'}



def check_refund_eligibility(order_id:str)->dict:
    order = lookup_order(order_id)
    if 'error' in order:
       return order
    order_date = order['created_at']
    formatted = datetime.strptime(order_date,"%Y-%m-%d")
    days_elapsed = (datetime.now() - formatted).days

    if order['status'] == 'delivered' and days_elapsed<=30:
       return {"eligible":True, "reason": "Delivered within 30 days"}
    else:
       return {"eligible":False,"reason":"Not delivered or outside 30-day window"}



def create_ticket(customer_id: str, issue: str, aiSummary:str , conversation_id: str) -> dict:
   
    ticket = {
        "conversation_id": conversation_id,
        "customer_id": customer_id,
        "aiSummary":aiSummary,
        "issue": issue,
        "status": "open",
        "created_at": datetime.now().isoformat()
    }
    try:
        validated_ticket = Ticket(**ticket).model_dump()
    except ValidationError as e:
        return {"error": f"Failed to create ticket: invalid data ({e})"}

    try:
        result = db.tickets.insert_one(validated_ticket)
    except Exception as e:
        return {"error": f"Failed to save ticket: {e}"}

    validated_ticket["_id"] = str(result.inserted_id)
    return validated_ticket



def escalate_to_human(reason: str, conversation_id:str) -> dict:
   result = db.tickets.update_one(
      {"conversation_id":conversation_id},
      {"$set":{"status":"escalated","escalation_reason":reason}}
      )
   if result.matched_count == 0:
      return {"error":"No conversation found."}
   return {'escalated':True,"reason":reason}



def search_policies(query: str ) -> List[str] | str:
  result = vectorStore.similarity_search(query, k=3)
  if len(result)==0:
     return "Nothing relevant found"
  
  return "\n\n---\n\n".join(r.page_content for r in result)
     
  
  
    
