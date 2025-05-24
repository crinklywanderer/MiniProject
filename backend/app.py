# backend/app.py

from flask import Flask, request, jsonify
from flask_cors import CORS
from backend.chatbot_engine import ChatbotEngine
import os

app = Flask(__name__)
CORS(app)

# Paths to the CSV datasets
csv_path = os.path.join(os.path.dirname(__file__), '..', 'train_data_chatbot.csv')
additional_csv_path = os.path.join(os.path.dirname(__file__), '..', 'ai-medical-chatbot.csv')

# Load the chatbot engine with both datasets
chatbot = ChatbotEngine(csv_path, additional_csv_path)

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        print("Received from frontend:", data)

        user_query = data.get('message')
        if not user_query:
            return jsonify({'response': "Empty message received."}), 400

        response = chatbot.get_answer(user_query)
        return jsonify({'response': response})
    except Exception as e:
        print("Exception in /chat:", e)
        return jsonify({'response': "Something went wrong."}), 500

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
