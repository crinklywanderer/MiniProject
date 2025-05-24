# Initializes the Flask app and registers Blueprints

from flask import Flask
from backend.chatbot_controller import chatbot_bp

def create_app():
    app = Flask(__name__)
    app.register_blueprint(chatbot_bp, url_prefix="/api/chatbot")
    return app
