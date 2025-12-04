import os
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.server_api import ServerApi

load_dotenv()
MONGO_DB_URL=os.getenv('MONGO_DB_URL')
uri = MONGO_DB_URL

client =MongoClient(uri, server_api=ServerApi('1'))
try:
    client.admin.command('ping')
    print("Connected to MongoDB")
except Exception as e:
    print(e)
