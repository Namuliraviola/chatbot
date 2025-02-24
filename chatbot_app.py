import streamlit as st
import subprocess

class StreamlitApp:
    def __init__(self, port=8501):
        self.port = port

    def run_streamlit(self):
        # Set Streamlit page config
        st.set_page_config(
            page_title="Chatbot App",
            layout="wide",
            initial_sidebar_state="expanded"
        )

        st.title("Chatbot")

        # Initialize chat history if not present
        if "messages" not in st.session_state:
            st.session_state.messages = []

        # Display chat history
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Chat input
        if prompt := st.chat_input("What's on your mind?"):
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})

            # Display user message
            with st.chat_message("user"):
                st.markdown(prompt)

            # Generate assistant response (replace this logic with your chatbot logic)
            response = self.get_chatbot_response(prompt)

            # Display assistant response
            with st.chat_message("assistant"):
                st.markdown(response)

            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": response})

    def get_chatbot_response(self, user_message):
        # This is where you can implement your chatbot logic
        # For now, it just echoes the user message
        return f"You said: {user_message}"

    def create_application(self):
        # Start the Streamlit server
        command = ["streamlit", "run", __file__, f"--server.port={self.port}", "--server.headless=true"]
        subprocess.Popen(command)

if __name__ == "__main__":
    app = StreamlitApp()
    app.create_application()
