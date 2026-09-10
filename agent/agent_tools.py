from langchain.tools import tool, ToolRuntime
from langchain.messages import ToolMessage
from agent.tools import lookup_order, check_refund_eligibility, create_ticket,search_policies
from langgraph.types import Command
from typing import List

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
def search_policies_tool(query: str):
     """
    Search the company's policy knowledge base for information about returns, 
    shipping, warranties, order tracking, error codes, escalation rules, and 
    frequently asked questions.

    Use this tool when the customer asks a question about company policy or 
    general procedures — e.g. "how long do I have to return an item", 
    "do you cover accidental damage", "what does error code ERR-201 mean", 
    "can I combine promo codes". 

    Do NOT use this tool for questions about a specific customer's order status, 
    account details, or ticket history — use the order-lookup tools for those instead.

    Args:
        query: The customer's question, in natural language, as close to their 
               original wording as possible.

    Returns:
        The most relevant policy texts list matching the query, to be used as context 
        for answering the customer. If no relevant policy is found, returns a 
        message indicating nothing matched.
    """
     results : List[str] | str = search_policies(query)
     
     return results
     
     

# @tool
# def escalate_to_human_tool(reason: str, runtime: ToolRuntime) -> dict:
#      """Escalate the current conversation to a human agent, with a reason."""
#      conversation_id = runtime.context.conversation_id
#      result = escalate_to_human(reason, conversation_id)
#      return Command(
#           update={
#                'escalated':True,
#                'messages':[
#                  ToolMessage(content=str(result), tool_call_id = runtime.tool_call_id)
#                ]
#           } 
#      )