cancer-assistant-chatbot/
│
├── backend/
│   ├── app.py
│   ├── chatbot_controller.py
│   ├── chatbot_service.py
│   ├── intents/
│   │   ├── __init__.py
│   │   ├── symptom_checker.py
│   │   ├── specialist_finder.py
│   └── database/
│       └── connector.py
│
├── frontend/
│   ├── index.html
│   ├── styles.css
│   └── main.js
│
└── .env


# backend
python -m backend.app


# frontend
cd frontend
python -m http.server

http://localhost:8000/frontend/
http://127.0.0.1:5000
http://localhost:8000