from pymongo import MongoClient
import os
from dotenv import load_dotenv

#load envs
result = load_dotenv()

mongodb_uri = os.environ['MONGO_URI']

client = MongoClient(mongodb_uri)

db = client['supportpilot']

