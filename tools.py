from db import db
from datetime import datetime



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



def create_ticket(customer_id: str, issue: str, conversation_id: str) -> dict:
   
   ticket = {
              "conversation_id":conversation_id,
              "customer_id":customer_id,
              "issue":issue,
              "status":"open",
              "created_at":datetime.now().isoformat()
            }
   result = db.tickets.insert_one(ticket)
   ticket["_id"] = str(result.inserted_id)
   return ticket



def escalate_to_human(reason: str, conversation_id:str) -> dict:
   result = db.tickets.update_one(
      {"conversation_id":conversation_id},
      {"$set":{"status":"escalated","escalation_reason":reason}}
      )
   if result.matched_count == 0:
      return {"error":"No conversation found."}
   return {'escalated':True,"reason":reason}
    
