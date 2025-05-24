from flask import Blueprint, request, jsonify

chatbot_bp = Blueprint('chatbot', __name__)


@chatbot_bp.route('/respond', methods=['POST'])
def chatbot_respond():
    data = request.get_json()
    prompt = data.get('prompt', '').lower()

    # Basic keyword-based logic
    if "specialist" in prompt or "doctor" in prompt:
        response = (
            "Sure! Here are some top cancer specialists available on our portal:\n"
            "1. Dr. Ayesha Verma – Oncologist (Mumbai)\n"
            "2. Dr. Rajesh Patel – Radiation Specialist (Delhi)\n"
            "3. Dr. Neha Sharma – Surgical Oncologist (Bangalore)\n\n"
            "You can book an appointment from the 'Specialists' section."
        )
    elif "navigate" in prompt or "how to use" in prompt:
        response = (
            "To navigate this website:\n"
            "👉 Use the top menu to access 'Home', 'Specialists', 'Book Appointment', or 'Chatbot'.\n"
            "👉 You can ask me to find doctors, symptoms, or book appointments anytime."
        )
    elif "appointment" in prompt or "book" in prompt:
        response = (
            "To book an appointment:\n"
            "1. Go to the 'Specialists' section.\n"
            "2. Choose a doctor.\n"
            "3. Click 'Book Appointment' and select your preferred time slot."
        )
    elif "symptoms" in prompt:
        response = (
            "Some general symptoms to watch for:\n"
            "- Unusual lumps or swelling\n"
            "- Persistent fatigue or weight loss\n"
            "- Unexplained bleeding\n"
            "- Changes in skin or moles\n\n"
            "Please consult a doctor for diagnosis."
        )
    elif "connect me" in prompt or "talk to doctor" in prompt:
        response = (
            "Connecting you to a doctor...\n"
            "Please wait while we match you with the best available specialist. Alternatively, you can visit the 'Live Chat' or 'Book Appointment' section."
        )
    elif "what is this" in prompt or "portal" in prompt:
        response = (
            "This portal is your personal assistant for cancer-related care.\n"
            "You can find specialists, learn about symptoms, and book appointments easily.\n"
            "Let me know how I can assist you!"
        )
    else:
        response = (
            "I'm here to help! You can ask things like:\n"
            "- 'I need a cancer specialist'\n"
            "- 'How do I navigate this website?'\n"
            "- 'How to book an appointment?'\n"
            "- 'Tell me symptoms of cancer'\n"
            "- 'What is this portal about?'\n"
            "- 'Connect me to a doctor'"
        )

    return jsonify({'response': response})
