import os
from dotenv import load_dotenv
from mock import orders, customers
from schemas import Order, Customer
from db import db

#validate both orders and customers list from pydantic model
validated_orders = [Order(**o).model_dump() for o in orders]
validated_customers = [Customer(**c).model_dump() for c in customers]

#insert validated orders and customers to db
db.orders.insert_many(validated_orders)
db.customers.insert_many(validated_customers)