from flask import Flask, request, jsonify
import os
from rapidfuzz import fuzz

app = Flask(__name__)

# Set the maximum file size for uploads
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5 MB
app.config['UPLOAD_FOLDER'] = 'uploads/'  # Folder to save uploaded files

# In-memory storage for session data (for demo purposes)
user_sessions = {}

# Create the upload folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Define valid registration types
valid_types = ["doctor", "health facility", "school"]

def match_intent(user_message, options, threshold=80):
    """Match user input against a list of options with a similarity threshold."""
    for option in options:
        if fuzz.ratio(user_message.lower(), option.lower()) > threshold:
            return option
    return None

@app.route('/')
def home():
    return 'Welcome to the chatbot!'

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_id = data.get("user_id")
        user_message = data.get("message").strip().lower()

        if not user_id or not user_message:
            return jsonify({"response": "Invalid request. Please provide a user ID and message."}), 400

        if user_id not in user_sessions:
            user_sessions[user_id] = {"step": 0, "info": {}, "type": None}

        session = user_sessions[user_id]

        # Step 0: Initial Registration Selection
        if session["step"] == 0:
            matched_type = match_intent(user_message, valid_types)
            if matched_type:
                session["type"] = matched_type
                session["step"] = 1
                return jsonify({"response": f"What is the {matched_type}'s name?"})
            return jsonify({"response": "Would you like to register as a health facility, school, or a doctor?"})

        # Step 1: Collect Name
        elif session["step"] == 1:
            session["info"]["name"] = user_message
            session["step"] = 2
            return jsonify({"response": f"What is the {session['type']}'s email?"})

        # Step 2: Collect Email
        elif session["step"] == 2:
            session["info"]["email"] = user_message
            session["step"] = 3
            return jsonify({"response": f"What is the {session['type']}'s phone number?"})

        # Step 3: Collect Phone Number
        elif session["step"] == 3:
            session["info"]["phone"] = user_message
            session["step"] = 4
            return jsonify({"response": f"Please upload the {session['type']}'s license document (PDF)."})

        # Step 4: Handle License Upload Confirmation
        elif session["step"] == 4:
            if "upload" in user_message:
                session["step"] = 5
                return jsonify({"response": f"{session['type'].capitalize()} registration completed! Do you want to register another entity?"})
            return jsonify({"response": "Please confirm once you have uploaded the document by typing 'uploaded'."})

        # Step 5: Reset or Continue
        elif session["step"] == 5:
            matched_type = match_intent(user_message, valid_types)
            if matched_type:
                session["type"] = matched_type
                session["step"] = 1
                return jsonify({"response": f"What is the {matched_type}'s name?"})
            return jsonify({"response": "Thank you! If you need to register another entity, please specify: health facility, school, or doctor."})

        return jsonify({"response": "Unexpected input. Please follow the registration process."})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Start the Flask app
    app.run(host='0.0.0.0', port=5000, debug=False)  # Ensure debug is set to False

    # User interaction loop
    user_id = input("Enter your user ID: ")

    print("You can start chatting with the bot. Type 'exit' to quit.")
    
    while True:
        user_message = input("You: ")
        if user_message.lower() == "exit":
            break

        response = requests.post("http://127.0.0.1:5000/chat", json={"user_id": user_id, "message": user_message})
        
        if response.status_code == 200:
            print("Chatbot:", response.json().get("response"))
        else:
            print("Error:", response.text)
