from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# Set the maximum file size for uploads
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5 MB
app.config['UPLOAD_FOLDER'] = 'uploads/'  # Folder to save uploaded files

# In-memory storage for session data (for demo purposes)
user_sessions = {}

# Create the upload folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/chat', methods=['POST'])
def chat():
    user_id = request.json.get("user_id")  # Unique identifier for the user
    user_message = request.json.get("message").lower()

    if user_id not in user_sessions:
        user_sessions[user_id] = {"step": 0, "info": {}, "type": None}

    session = user_sessions[user_id]

    if session["step"] == 0:
        if "register doctor" in user_message:
            session["type"] = "doctor"
            session["step"] = 1
            return jsonify({"response": "What is the doctor's name?"})
        elif "register health facility" in user_message:
            session["type"] = "health facility"
            session["step"] = 1
            return jsonify({"response": "What is the health facility's name?"})
        elif "register school" in user_message:
            session["type"] = "school"
            session["step"] = 1
            return jsonify({"response": "What is the school's name?"})

    elif session["step"] == 1:
        session["info"]["name"] = user_message
        session["step"] = 2
        return jsonify({"response": f"What is the {session['type']}'s email?"})

    elif session["step"] == 2:
        session["info"]["email"] = user_message
        session["step"] = 3
        return jsonify({"response": f"What is the {session['type']}'s phone number?"})

    elif session["step"] == 3:
        session["info"]["phone"] = user_message
        session["step"] = 4
        return jsonify({"response": f"Please upload the {session['type']}'s license document (PDF)."})


    elif session["step"] == 4:
        if 'file' not in request.files:
            return jsonify({"response": "No file uploaded."}), 400
        file = request.files['file']

        if file.filename == '':
            return jsonify({"response": "No file selected."}), 400

        if file and file.filename.endswith('.pdf'):
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)

            # Save the license file path in session info
            session["info"]["license_file"] = file_path

            # Here, you can save the information to a database
            info = session["info"]
            # Reset the session after registration is complete
            type_name = session["type"]
            session["step"] = 0
            session["info"] = {}
            session["type"] = None
            return jsonify({
                "response": f"{type_name.capitalize()} {info['name']} registered successfully!"
            })
        else:
            return jsonify({"response": "Please upload a valid PDF file."}), 400

    else:
        return jsonify({"response": "I can help with registering health facilities, doctors, and schools. What would you like to do?"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
