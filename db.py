from pymongo import MongoClient
import os
from dotenv import load_dotenv

#load envs
result = load_dotenv()
print("dotenv loaded:", result)
print("MONGO_URI value:", os.getenv("MONGO_URI"))

mongodb_uri = os.environ['MONGO_URI']

client = MongoClient(mongodb_uri)

db = client['supportpilot']

