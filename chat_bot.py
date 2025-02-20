import requests

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
