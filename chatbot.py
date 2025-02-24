from flask import Flask, request, jsonify
import os
from rapidfuzz import fuzz
import logging

app = Flask(__name__)

# Set the maximum file size for uploads
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5 MB
app.config['UPLOAD_FOLDER'] = 'uploads/'  # Folder to save uploaded files

# In-memory storage for session data
user_sessions = {}

# Create the upload folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Define valid registration types
valid_types = ["doctor", "health facility", "school"]

# Set up logging
logging.basicConfig(level=logging.INFO)

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
        # Check if request is JSON
        if not request.is_json:
            return jsonify({"error": "Request must be JSON."}), 400
        
        data = request.json
        user_id = data.get("user_id")
        user_message = data.get("message", "").strip().lower()

        # Validate user ID and message
        if not user_id or not user_message:
            return jsonify({"error": "Invalid request. Provide a user ID and message."}), 400

        # Initialize user session if not exists
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
            return jsonify({"response": "Thank you! If you need to register another entity, specify: health facility, school, or doctor."})

        return jsonify({"response": "Unexpected input. Please follow the registration process."})

    except Exception as e:
        app.logger.error(f"Error processing request: {str(e)}")
        return jsonify({"error": "An error occurred while processing your request."}), 500

if __name__ == '__main__':
    # Start Flask without user input loop
    app.run(host='127.0.0.1', port=5000, debug=True)  # Debug mode for troubleshooting
