from pydantic import BaseModel,EmailStr
from typing import Literal, List

class Customer(BaseModel):
    id:str
    name:str
    email:EmailStr
    tier:Literal["free","premium"]


class Order(BaseModel):
     id:str
     customer_id:str
     items:List[str]
     status:Literal["delivered","pending"]
     total:float
     created_at:str

class Ticket(BaseModel):
       conversation_id:str
       customer_id:str
       aiSummary:str
       issue:str
       status:Literal['open','resolved','escalated']
       created_at:str