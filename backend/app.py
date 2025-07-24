# backend/app.py

from flask import Flask, request, jsonify
from flask_cors import CORS
from backend.chatbot_engine import ChatbotEngine

app = Flask(__name__)
CORS(app)

chatbot = ChatbotEngine()


@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_input = data.get('message')

    if not user_input:
        return jsonify({'error': 'No message provided'}), 400

    try:
        response = chatbot.ask(user_input)
        return jsonify({'response': response})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
