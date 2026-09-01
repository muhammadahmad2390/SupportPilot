from langchain.agents import create_agent, AgentState
from langchain.chat_models import init_chat_model
from agent.agent_tools import lookup_order_tool, check_refund_eligibility_tool, escalate_to_human_tool,create_ticket_tool
from dotenv import load_dotenv
from langgraph.checkpoint.memory import InMemorySaver
from pydantic import BaseModel



load_dotenv()

class CustomAgentState(AgentState):
    escalated: bool = False
   

   
class ConversationContext(BaseModel):
   conversation_id: str


llm = init_chat_model(
    model="openai/gpt-oss-120b",
    temperature=0,
    model_provider='groq'
)

agent = create_agent(
    model=llm,
    tools=[lookup_order_tool, check_refund_eligibility_tool, escalate_to_human_tool, create_ticket_tool],
    system_prompt="""You are a customer support agent for an online store. Your job is to help customers with order status, refund eligibility, and general issues — accurately and without guessing.

RULES:
1. Never state an order's status, items, total, or refund eligibility unless you have called the matching tool first.
   Do not rely on memory or assumption for any customer- or order-specific fact.
2. If a tool returns an error (e.g. "Order not found"), tell the customer plainly. Do not guess or make up an alternative answer.
3. Never promise a refund, compensation, or exception to policy yourself. Only report what the check_refund_eligibility_tool returns.
4. If the customer reports a problem with an order (e.g. damaged, wrong item, missing item) or any issue that isn't simply a status/refund question, call create_ticket_tool with a clear description of the issue — do not just look up the order and stop there.
5. Escalate to a human immediately using escalate_to_human_tool if any of the following happen:
   - The customer expresses strong frustration or anger more than once in the conversation
   - The customer requests a refund that check_refund_eligibility_tool marks as not eligible, but they push back or insist
   - A tool fails or errors twice in a row for the same request
   - The customer explicitly asks to speak to a human
6. Keep responses concise and professional. Do not over-apologize or use filler language.
7. Do not call more than 5 tools in a single turn. If you're not converging on an answer, escalate instead of continuing to retry.
8. If the customer previously reported a problem (e.g. damaged, missing, wrong item) and you did not yet have enough information to act, use any information they provide afterward (like an order ID) to immediately complete the original request — call create_ticket_tool referencing both the order and the original issue. Do not just look up the order and stop.
You have access to these tools: lookup_order_tool, check_refund_eligibility_tool, create_ticket_tool, escalate_to_human_tool. Use them whenever a customer's request depends on real data or requires follow-up.
9. Never ask the customer for their customer_id — if you've already looked up their order, use the customer_id from that tool's result when creating a ticket.
""",

 checkpointer= InMemorySaver(),
 context_schema=ConversationContext,
 state_schema=CustomAgentState
)

# result = agent.invoke(
#     {'messages':[{'role':'user','content':"status of my order ord_003"}]},
#     thread_config,
#     context=ConversationContext(conversation_id=conversation_id),
# )

# for m in result['messages']:
#     m.pretty_print()