import os
from dotenv import load_dotenv
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.memory import ConversationSummaryMemory
from langchain.chains import ConversationChain
from langchain_community.agent_toolkits.load_tools import load_tools
from langchain.agents import initialize_agent, AgentType
from gtts import gTTS
import tempfile
import base64

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# LLM
chat = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=GOOGLE_API_KEY, temperature=0.7)

# Initialize session state for memory
if "memory" not in st.session_state:
    st.session_state.memory = None

@st.cache_resource
def get_conversation_chain(_chat):
    """Create a conversation chain with memory"""
    prompt = ChatPromptTemplate.from_template("""
    Respond to the following question as if you were a thoughtful and slightly witty human being. 
    Keep your answer concise, creative, and easy to understand, as if you were talking to a friend.
    Current conversation:
    {history}
    Human: {input}
    AI:""")
    
    if st.session_state.memory is None:
        st.session_state.memory = ConversationSummaryMemory(llm=_chat, return_messages=True)
    
    return ConversationChain(
        llm=_chat,
        memory=st.session_state.memory,
        prompt=prompt,
        verbose=False
    )

# Text-to-Speech Function
def speak_text(text):
    try:
        # Create a temporary file with a unique name
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
            temp_filename = fp.name

        # Generate and save audio outside the file context
        tts = gTTS(text=text, lang='en')
        tts.save(temp_filename)
        
        # Read the audio file
        with open(temp_filename, 'rb') as audio_file:
            audio_bytes = audio_file.read()
        
        # Create an HTML audio player
        audio_base64 = base64.b64encode(audio_bytes).decode()
        audio_player = f'<audio autoplay><source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3"></audio>'
        st.markdown(audio_player, unsafe_allow_html=True)
        
        # Clean up - make sure file handle is closed before trying to delete
        try:
            os.unlink(temp_filename)
        except Exception:
            pass  # Ignore deletion errors
            
    except Exception as e:
        st.error(f"Text-to-Speech error: {e}")

# Speech Recognition Function
def recognize_speech():
    st.warning("Voice input is not available in the cloud deployment. Please use text input instead.")
    return None

# Streamlit Main Function
def main():
    st.title("AI Powered Chatbot")
    
    # Add input for Gemini API Key
    gemini_api_key = st.text_input("Enter your Gemini API Key:", type="password")
    if gemini_api_key:
        chat = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=gemini_api_key, temperature=0.7)
        conversation = get_conversation_chain(chat)

        if "messages" not in st.session_state:
            st.session_state.messages = []

        # Display chat history
        for message in st.session_state.messages:
            st.chat_message(message["role"]).markdown(message["content"])

        # Get user input
        user_input = st.text_input("Type your message here:")

        if user_input:
            if user_input.lower() == "exit":
                st.write("Goodbye!")
                return
            elif user_input.lower().startswith("solve"):
                tools = load_tools(["llm-math"], llm=chat)
                agent = initialize_agent(tools, chat, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=False)
                bot_response = agent.invoke({"input": user_input[5:]})["output"]
            else:
                bot_response = conversation.predict(input=user_input)
                
                if bot_response:
                    st.session_state.messages.append({"role": "user", "content": user_input})
                    st.session_state.messages.append({"role": "assistant", "content": bot_response})
                    st.chat_message("assistant").markdown(bot_response)
                    speak_text(bot_response)

if __name__ == "__main__":
    main()
