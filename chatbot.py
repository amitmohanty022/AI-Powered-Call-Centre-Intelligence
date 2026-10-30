import base64
import os
from io import BytesIO

import streamlit as st
from dotenv import load_dotenv
from gtts import gTTS
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")

SYSTEM_PROMPT = (
    "Respond to the following question as if you were a thoughtful and slightly witty human being. "
    "Keep your answer concise, creative, and easy to understand, as if you were talking to a friend."
)

if "messages" not in st.session_state:
    st.session_state.messages = []


def get_reply(chat, user_input):
    """Send the full conversation (memory) plus the new message to Gemini."""
    history = [
        ("human" if m["role"] == "user" else "ai", m["content"]) for m in st.session_state.messages
    ]
    prompt = ChatPromptTemplate.from_messages(
        [("system", SYSTEM_PROMPT), ("placeholder", "{history}"), ("human", "{input}")]
    )
    return (prompt | chat).invoke({"history": history, "input": user_input}).text


def speak_text(text):
    try:
        buffer = BytesIO()
        gTTS(text=text, lang="en").write_to_fp(buffer)
        audio_base64 = base64.b64encode(buffer.getvalue()).decode()
        audio_player = f'<audio autoplay controls><source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3"></audio>'
        st.markdown(audio_player, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Text-to-Speech error: {e}")


def main():
    st.title("AI Powered Chatbot")

    gemini_api_key = os.getenv("GOOGLE_API_KEY") or st.text_input("Enter your Gemini API Key:", type="password")
    if not gemini_api_key:
        st.info("Add GOOGLE_API_KEY to your .env file or paste the key above.")
        return

    chat = ChatGoogleGenerativeAI(model=GEMINI_MODEL, google_api_key=gemini_api_key, temperature=0.7)

    for message in st.session_state.messages:
        st.chat_message(message["role"]).markdown(message["content"])

    user_input = st.chat_input("Type your message here:")

    if user_input:
        if user_input.lower() == "exit":
            st.write("Goodbye!")
            return
        st.chat_message("user").markdown(user_input)
        try:
            bot_response = get_reply(chat, user_input)
            if bot_response:
                st.session_state.messages.append({"role": "user", "content": user_input})
                st.session_state.messages.append({"role": "assistant", "content": bot_response})
                st.chat_message("assistant").markdown(bot_response)
                speak_text(bot_response)
        except Exception as e:
            st.error(f"Error: {str(e)}")


if __name__ == "__main__":
    main()
