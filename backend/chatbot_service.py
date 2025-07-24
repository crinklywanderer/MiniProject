# backend/chatbot_service.py


from backend.database.connector import MongoConnector

class ChatbotService:
    def __init__(self):
        self.db = MongoConnector()
        self.sessions = {}  # user_id: session state (can be expanded)

    def get_response(self, user_message, user_id="default"):
        msg = user_message.strip().lower()

        # Check session context
        session = self.sessions.get(user_id, {})

        if "specialist" in msg:
            return {
                "response": "Sure! What type of cancer are you concerned about?\n1. Breast\n2. Lung\n3. Prostate",
                "intent": "find_specialist"
            }

        elif msg in ["breast", "lung", "prostate"]:
            results = self.db.get_specialists_by_type(msg.capitalize())
            if results:
                self.sessions[user_id] = {"cancer_type": msg.capitalize()}
                response = "Here are some specialists:\n"
                for doc in results:
                    response += f"- Dr. {doc['name']} ({doc['specialty']})\n"
                response += "\nWho would you like to book with? (Type doctor name)"
                return { "response": response, "intent": "list_specialists" }

        elif "dr." in msg or any(word.istitle() for word in msg.split()):
            session["specialist_name"] = msg.title()
            self.sessions[user_id] = session
            return {
                "response": "Got it! Please share your full name for booking.",
                "intent": "await_name"
            }

        elif "name" not in session and session.get("specialist_name"):
            session["user_name"] = user_message.title()
            self.sessions[user_id] = session
            return {
                "response": "Thanks! Now tell me your preferred date (YYYY-MM-DD)",
                "intent": "await_date"
            }

        elif "user_name" in session and "preferred_date" not in session:
            session["preferred_date"] = user_message.strip()
            self.sessions[user_id] = session
            return {
                "response": "And what time do you prefer? (HH:MM format)",
                "intent": "await_time"
            }

        elif "preferred_date" in session and "preferred_time" not in session:
            session["preferred_time"] = user_message.strip()

            # Save to DB
            self.db.book_appointment(session)
            self.sessions.pop(user_id)  # clear session after booking

            return {
                "response": f"Booking confirmed with {session['specialist_name']} on {session['preferred_date']} at {session['preferred_time']}.\nWe’ve sent a confirmation message to your registered email!",
                "intent": "booking_complete"
            }

        return {
            "response": "I'm not sure I understand. Do you want to:\n1. Find a specialist\n2. Book an appointment\n3. Ask about symptoms?",
            "intent": "fallback"
        }
