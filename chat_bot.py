import requests

# Get user ID
user_id = input("Enter your user ID: ").strip()
print("You can start chatting with the bot. Type 'exit' to quit.")

while True:
    user_message = input("You: ").strip()

    # Exit condition
    if user_message.lower() == "exit":
        print("Goodbye!")
        break

    try:
        # Send user input to chatbot API
        response = requests.post(
            "http://127.0.0.1:5000/chat",  # Change to HTTP
            json={"user_id": user_id, "message": user_message},
            timeout=5  # Add timeout to prevent hanging
        )

        if response.status_code == 200:
            print("Chatbot:", response.json().get("response", "No response from chatbot."))
        else:
            print(f"Error: {response.status_code} - {response.text}")

    except requests.exceptions.ConnectionError:
        print("Error: Unable to connect to chatbot server. Is Flask running?")
        break
    except requests.exceptions.Timeout:
        print("Error: The chatbot took too long to respond. Try again.")
    except Exception as e:
        print(f"Unexpected error: {e}")
