import os
from dotenv import load_dotenv
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from gtts import gTTS
import tempfile
import base64

# Load environment variables
load_dotenv()

# Initialize session state
if "memory" not in st.session_state:
    st.session_state.memory = None
if "messages" not in st.session_state:
    st.session_state.messages = []

def get_conversation_chain(chat):
    """Create a conversation chain with memory"""
    prompt = ChatPromptTemplate.from_template("""
    Respond to the following question as if you were a thoughtful and slightly witty human being. 
    Keep your answer concise, creative, and easy to understand, as if you were talking to a friend.
    Current conversation:
    {history}
    Human: {input}
    AI:""")
    
    if st.session_state.memory is None:
        st.session_state.memory = ConversationBufferMemory(return_messages=True)
    
    return ConversationChain(
        llm=chat,
        memory=st.session_state.memory,
        prompt=prompt,
        verbose=False
    )

def speak_text(text):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
            temp_filename = fp.name

        tts = gTTS(text=text, lang='en')
        tts.save(temp_filename)
        
        with open(temp_filename, 'rb') as audio_file:
            audio_bytes = audio_file.read()
        
        audio_base64 = base64.b64encode(audio_bytes).decode()
        audio_player = f'<audio autoplay><source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3"></audio>'
        st.markdown(audio_player, unsafe_allow_html=True)
        
        try:
            os.unlink(temp_filename)
        except Exception:
            pass
    except Exception as e:
        st.error(f"Text-to-Speech error: {e}")

def main():
    st.title("AI Powered Chatbot")
    
    # Add input for Gemini API Key
    gemini_api_key = st.text_input("Enter your Gemini API Key:", type="password")
    if gemini_api_key:
        chat = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            google_api_key=gemini_api_key,
            temperature=0.7,
            convert_system_message_to_human=True
        )
        conversation = get_conversation_chain(chat)

        # Display chat history
        for message in st.session_state.messages:
            st.chat_message(message["role"]).markdown(message["content"])

        # Get user input
        user_input = st.text_input("Type your message here:")

        if user_input:
            if user_input.lower() == "exit":
                st.write("Goodbye!")
                return
            
            try:
                bot_response = conversation.predict(input=user_input)
                
                if bot_response:
                    st.session_state.messages.append({"role": "user", "content": user_input})
                    st.session_state.messages.append({"role": "assistant", "content": bot_response})
                    st.chat_message("assistant").markdown(bot_response)
                    speak_text(bot_response)
            except Exception as e:
                st.error(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
