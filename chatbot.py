import os
import base64
from io import BytesIO

import streamlit as st
from dotenv import load_dotenv
from gtts import gTTS
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI

# Load environment variables
load_dotenv()

GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")
SYSTEM_PROMPT = (
    "Respond to the following question as if you were a thoughtful and slightly witty human being. "
    "Keep your answer concise, creative, and easy to understand, as if you were talking to a friend."
)

# Initialize session state. The message list doubles as the conversation memory
# (this replaces the removed LangChain ConversationChain + ConversationBufferMemory).
if "messages" not in st.session_state:
    st.session_state.messages = []


def get_response(chat, user_input):
    """Send the full conversation so far plus the new message to Gemini."""
    history = [SystemMessage(content=SYSTEM_PROMPT)]
    for message in st.session_state.messages:
        if message["role"] == "user":
            history.append(HumanMessage(content=message["content"]))
        else:
            history.append(AIMessage(content=message["content"]))
    history.append(HumanMessage(content=user_input))
    return chat.invoke(history).text


def speak_text(text):
    try:
        audio = BytesIO()
        gTTS(text=text, lang="en").write_to_fp(audio)
        audio_base64 = base64.b64encode(audio.getvalue()).decode()
        audio_player = f'<audio autoplay><source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3"></audio>'
        st.markdown(audio_player, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Text-to-Speech error: {e}")


def main():
    st.title("AI Powered Chatbot")

    # Add input for Gemini API Key (falls back to GOOGLE_API_KEY from .env)
    gemini_api_key = st.text_input("Enter your Gemini API Key:", type="password") or os.getenv("GOOGLE_API_KEY")
    if not gemini_api_key:
        st.info("Please add your Gemini API key to continue.", icon="🗝")
        return

    chat = ChatGoogleGenerativeAI(
        model=GEMINI_MODEL,
        google_api_key=gemini_api_key,
        temperature=0.7,
    )

    # Display chat history
    for message in st.session_state.messages:
        st.chat_message(message["role"]).markdown(message["content"])

    # Get user input
    user_input = st.chat_input("Type your message here:")

    if user_input:
        if user_input.lower() == "exit":
            st.write("Goodbye!")
            return

        st.chat_message("user").markdown(user_input)
        try:
            bot_response = get_response(chat, user_input)

            if bot_response:
                st.session_state.messages.append({"role": "user", "content": user_input})
                st.session_state.messages.append({"role": "assistant", "content": bot_response})
                st.chat_message("assistant").markdown(bot_response)
                speak_text(bot_response)
        except Exception as e:
            st.error(f"Error: {str(e)}")


if __name__ == "__main__":
    main()
