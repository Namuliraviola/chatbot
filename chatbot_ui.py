import streamlit as st
import requests

# Define the Flask chatbot API endpoint
CHATBOT_API_URL = "http://127.0.0.1:5000/chat"

# Streamlit UI setup
st.set_page_config(page_title="Chatbot", layout="centered")
st.title("WELCOME TO KETI AI")

# Initialize user session
if "user_id" not in st.session_state:
    st.session_state.user_id = "user_123"

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
user_input = st.text_input("Type your message:", key="user_input", on_change=lambda: send_message())

def send_message():
    """Handles sending messages to the Flask chatbot API."""
    user_message = st.session_state.user_input.strip()

    if user_message:
        # Append user message to chat history
        st.session_state.messages.append({"role": "user", "content": user_message})

        # Send user input to Flask chatbot API
        try:
            response = requests.post(
                CHATBOT_API_URL,
                json={"user_id": st.session_state.user_id, "message": user_message},
            )

            if response.status_code == 200:
                bot_reply = response.json().get("response", "No response from chatbot.")
            else:
                bot_reply = f"Error: {response.status_code} - {response.text}"

        except Exception as e:
            bot_reply = f"Error communicating with chatbot: {str(e)}"

        # Append chatbot response to chat history
        st.session_state.messages.append({"role": "assistant", "content": bot_reply})

        # Clear the text input field by using the Streamlit API
        st.session_state.user_input = ""  # This is fine to reset here after the callback

# The text input will trigger the send_message function when the user presses Enter.
