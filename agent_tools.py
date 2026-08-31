from langchain.tools import tool
from tools import lookup_order, check_refund_eligibility, create_ticket, escalate_to_human

@tool
def lookup_order_tool(order_id: str) -> dict:
     """Look up an order's status, items, and total by its order ID."""
     return lookup_order(order_id)

@tool
def check_refund_eligibility_tool(order_id: str) -> dict:
     """Check if an order is eligible for a refund based on delivery status and 30-day policy."""
     return check_refund_eligibility(order_id)


@tool
def create_ticket_tool(customer_id: str, issue: str, conversation_id: str) -> dict:
     """Create a support ticket for a customer issue that needs follow-up."""
     return create_ticket(customer_id, issue, conversation_id)

    
@tool
def escalate_to_human_tool(reason: str,conversation_id: str) -> dict:
     """Escalate the current conversation to a human agent, with a reason."""
     return escalate_to_human(reason, conversation_id)


