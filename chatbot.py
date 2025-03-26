import os
from dotenv import load_dotenv
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.memory import ConversationSummaryMemory
from langchain_core.runnables import RunnableWithMessageHistory
from langchain.chains import LLMChain
import pyttsx3
import speech_recognition as sr
from langchain_community.agent_toolkits.load_tools import load_tools
from langchain.agents import initialize_agent, AgentType
from langsmith import traceable

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# LLM
chat = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=GOOGLE_API_KEY, temperature=0.7)

# Prompt template
prompt_template = """Respond to the following question as if you were a thoughtful and slightly witty human being. Keep your answer concise, creative, and easy to understand, as if you were talking to a friend.
Current conversation:
{history}
Human: {input}
AI:"""

def create_conversation_chain():
    prompt = ChatPromptTemplate.from_template(prompt_template)
    memory = ConversationSummaryMemory(llm=chat, return_messages=True)
    chain = LLMChain(llm=chat, prompt=prompt, memory=memory)
    return chain

# Text-to-Speech Function
def speak_text(text):
    try:
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        st.error(f"Text-to-Speech error: {e}")

# Speech Recognition Function
def recognize_speech():
    try:
        r = sr.Recognizer()
        with sr.Microphone() as source:
            st.info("Listening... Speak now.")
            r.adjust_for_ambient_noise(source)
            try:
                audio = r.listen(source, timeout=10)
                return r.recognize_google(audio)
            except sr.UnknownValueError:
                st.warning("Speech not recognized.")
            except sr.WaitTimeoutError:
                st.warning("Timeout error: No speech detected.")
    except AttributeError as e:
        st.error("Error: PyAudio is not installed. Voice input is unavailable.")
        return None
    except Exception as e:
        st.error(f"Error initializing microphone: {str(e)}")
        return None
    return None

# Streamlit Main Function
@traceable(project_name="chatbot")
def main():
    st.title("AI Powered Chatbot")
    
    # Add input for Gemini API Key
    gemini_api_key = st.text_input("Enter your Gemini API Key:")
    if gemini_api_key:
        chat = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=gemini_api_key, temperature=0.7)
        conversation = create_conversation_chain()
        tools = load_tools(["llm-math"], llm=chat)
        agent = initialize_agent(tools, chat, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=False)

        if "messages" not in st.session_state:
            st.session_state.messages = []

        # Check if voice input is available
        try:
            sr.Microphone()
            voice_available = True
        except:
            voice_available = False
            st.warning("Voice input is not available. Please install PyAudio for voice functionality.")

        if voice_available:
            voice_assistant_active = st.checkbox("Activate Voice Assistant")
        user_input = st.text_input("Type your query here or click the microphone to speak")

        if voice_available and st.button("🎙️ Speak"):
            user_input = recognize_speech()

        if user_input:
            if user_input.lower() == "exit":
                st.write("Goodbye!")
                speak_text("Goodbye!")
                return
            elif user_input.lower().startswith("solve"):
                bot_response = agent.run(user_input[5:])
            else:
                # Directly use the conversation chain
                bot_response = conversation.run(input=user_input)
                
                if bot_response:
                    st.session_state.messages.append({"role": "user", "content": user_input})
                    st.session_state.messages.append({"role": "assistant", "content": bot_response})
                    st.chat_message("assistant").markdown(bot_response)
                    speak_text(bot_response)

        # Fixed Voice Assistant Loop (only if voice is available)
        if voice_available and voice_assistant_active:
            st.warning("Voice Assistant is Active. Speak to interact.")
            while voice_assistant_active:
                user_input = recognize_speech()
                if user_input:
                    bot_response = conversation.run(input=user_input)
                    if bot_response:
                        st.session_state.messages.append({"role": "user", "content": user_input})
                        st.session_state.messages.append({"role": "assistant", "content": bot_response})
                        st.chat_message("assistant").markdown(bot_response)
                        speak_text(bot_response)

if __name__ == "__main__":
    main()
