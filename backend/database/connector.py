# backend/database/connector.py
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

class MongoConnector:
    def __init__(self):
        self.client = MongoClient(os.getenv("MONGO_URI"))
        self.db = self.client["cancer_assistant"]
        self.specialists = self.db["specialists"]

    def get_specialists_by_type(self, cancer_type):
        return list(self.specialists.find({"cancer_type": cancer_type}))

    def book_appointment(self, data):
        return self.db["booking"].insert_one(data)