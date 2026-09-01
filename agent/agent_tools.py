from langchain.tools import tool, ToolRuntime
from langchain.messages import ToolMessage
from agent.tools import lookup_order, check_refund_eligibility, create_ticket, escalate_to_human
from langgraph.types import Command

@tool
def lookup_order_tool(order_id: str) -> dict:
     """Look up an order's status, items, and total by its order ID."""
     return lookup_order(order_id)


@tool
def check_refund_eligibility_tool(order_id: str) -> dict:
     """Check if an order is eligible for a refund based on delivery status and 30-day policy."""
     return check_refund_eligibility(order_id)


@tool
def create_ticket_tool(customer_id: str, issue: str, runtime:ToolRuntime) -> dict:
     """Create a support ticket for a customer issue that needs follow-up."""
     conversation_id = runtime.context.conversation_id
     return create_ticket(customer_id, issue, conversation_id)

    
@tool
def escalate_to_human_tool(reason: str, runtime: ToolRuntime) -> dict:
     """Escalate the current conversation to a human agent, with a reason."""
     conversation_id = runtime.context.conversation_id
     result = escalate_to_human(reason, conversation_id)
     return Command(
          update={
               'escalated':True,
               'messages':[
                 ToolMessage(content=str(result), tool_call_id = runtime.tool_call_id)
               ]
          } 
     )