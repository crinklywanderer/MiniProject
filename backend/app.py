# backend/app.py

from flask import Flask, request, jsonify
from flask_cors import CORS
from backend.chatbot_engine import ChatbotEngine
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import requests

# Load environment variables from .env
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

app = Flask(__name__)
CORS(app)

# File paths for datasets
csv_path = os.path.join(os.path.dirname(__file__), '..', 'train_data_chatbot.csv')
additional_csv_path = os.path.join(os.path.dirname(__file__), '..', 'ai-medical-chatbot.csv')

# Hugging Face config
huggingface_api_key = os.getenv("HUGGINGFACE_API_KEY", "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")
huggingface_model = os.getenv("HUGGINGFACE_MODEL", "google/flan-t5-small")

# MongoDB config
mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017")
db_name = os.getenv("DB_NAME", "chatbot_db")

# Initialize services
chatbot = ChatbotEngine(csv_path, additional_csv_path)
mongo_client = MongoClient(mongo_uri)
db = mongo_client[db_name]
logs_collection = db["chat_logs"]

def query_huggingface(prompt):
    try:
        print("Hugging Face fallback query")
        url = f"https://api-inference.huggingface.co/models/{huggingface_model}"
        headers = {"Authorization": f"Bearer {huggingface_api_key}"}
        payload = {"inputs": prompt}

        response = requests.post(url, headers=headers, json=payload)
        print("Hugging Face Status:", response.status_code)
        print("Hugging Face Output:", response.text)

        if response.status_code == 200:
            output = response.json()
            if isinstance(output, list):
                if 'generated_text' in output[0]:
                    return output[0]['generated_text']
                elif 'answer' in output[0]:
                    return output[0]['answer']
            elif isinstance(output, dict) and 'generated_text' in output:
                return output['generated_text']

        return "I'm unable to connect to the external model at the moment."
    except Exception as e:
        print("Hugging Face fallback error:", e)
        return "Sorry, something went wrong with fallback response."

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_query = data.get('message', '').strip()
        user_name = data.get('name', 'User')
        user_age = data.get('age', '')

        if not user_query:
            return jsonify({'response': "Empty message received."}), 400

        # Step 1: Local response
        response = chatbot.get_answer(user_query)
        print("Local response:", response)
        # Step 2: Use Hugging Face if the response is vague
        # if response < 0.75:
        #    response = query_huggingface(user_query)
        if response.lower() in ["i'm sorry, i couldn't understand your question.",
                                "i do not understand.",
                                "not sure.",
                                "sorry"]:
            response = query_huggingface(user_query)

        # Step 3: Log conversation
        logs_collection.insert_one({
            "name": user_name,
            "age": user_age,
            "query": user_query,
            "response": response
        })

        return jsonify({'response': response})
    except Exception as e:
        print("Exception in /chat:", e)
        return jsonify({'response': "Something went wrong."}), 500

@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Welcome to the Cancer Chatbot API"})

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
