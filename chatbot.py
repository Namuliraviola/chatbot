from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get("message").lower()

    if "register health facility" in user_message:
        return jsonify({"response": "What is the name of the health facility?"})

    elif "register doctor" in user_message:
        return jsonify({"response": "Please provide the doctor's name and license number."})

    elif "register patient" in user_message:
        return jsonify({"response": "What is the patient's name and contact number?"})

    else:
        return jsonify({"response": "I can help with registering health facilities, doctors, and patients. What would you like to do?"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
