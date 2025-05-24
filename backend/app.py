from flask import Flask, request, jsonify
from flask_cors import CORS
from backend.chatbot_engine import ChatbotEngine
from pymongo import MongoClient
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)

# MongoDB setup
mongo_client = MongoClient("mongodb://localhost:27017/")
db = mongo_client["cancer_assistant"]
chat_collection = db["chats"]

# Load chatbot engine
csv_path = os.path.join(os.path.dirname(__file__), '..', 'train_data_chatbot.csv')
additional_csv_path = os.path.join(os.path.dirname(__file__), '..', 'ai-medical-chatbot.csv')
chatbot = ChatbotEngine(csv_path, additional_csv_path)

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_query = data.get('message')
        user_info = data.get('user', {
            "name": "User",
            "age": "Not provided",
            "gender": "Not specified"
        })

        if not user_query:
            return jsonify({'response': "Empty message received."}), 400

        response = chatbot.get_answer(user_query)
        personalized_response = f"{response}"

        # Save conversation to MongoDB
        chat_collection.insert_one({
            "timestamp": datetime.utcnow(),
            "user": user_info,
            "message": user_query,
            "response": response
        })

        return jsonify({'response': personalized_response})
    except Exception as e:
        print("Error:", e)
        return jsonify({'response': "Something went wrong."}), 500

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
