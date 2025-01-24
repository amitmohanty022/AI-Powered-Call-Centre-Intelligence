import os
from dotenv import load_dotenv
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langchain.memory import ConversationSummaryMemory
from langchain.chains import ConversationChain
import pyttsx3
import speech_recognition as sr
from langchain.agents import load_tools, initialize_agent, AgentType
from langsmith import traceable
from fastapi import FastAPI
from pydantic import BaseModel
import requests
import threading
import uvicorn

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# LLM
chat = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=GOOGLE_API_KEY, temperature=0.7)

# FastAPI Initialization
app = FastAPI()

# Prompt template
prompt_template = """You are a helpful chatbot.
Current conversation:
{history}
Human: {input}
AI:"""

def create_conversation_chain():
    prompt = ChatPromptTemplate.from_template(prompt_template)
    memory = ConversationSummaryMemory(llm=chat, return_messages=True)
    return ConversationChain(llm=chat, prompt=prompt, memory=memory)

# FastAPI Models
class ChatRequest(BaseModel):
    user_input: str

class ChatResponse(BaseModel):
    response: str

@app.post("/chat", response_model=ChatResponse)
def chat_api(request: ChatRequest):
    conversation = create_conversation_chain()
    response = conversation.predict(input=request.user_input)
    return ChatResponse(response=response)

# Function to call FastAPI endpoint
def call_fastapi_endpoint(user_input: str):
    url = "http://127.0.0.1:8001/chat"  # url FastAPI running
    data = {"user_input": user_input}
    
    # Sending the POST request to FastAPI
    response = requests.post(url, json=data)
    
    if response.status_code == 200:
        return response.json().get('response', '')
    else:
        st.error("Failed to communicate with FastAPI.")
        return None

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
        return None

# Streamlit Main Function
@traceable(project_name="chatbot")
def main():
    st.title("AI Powered Chatbot")
    conversation = create_conversation_chain()
    tools = load_tools(["llm-math"], llm=chat)
    agent = initialize_agent(tools, chat, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=False)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    voice_assistant_active = st.checkbox("Activate Voice Assistant")
    user_input = st.text_input("Type your query here or click the microphone to speak")

    if st.button("🎙️ Speak"):
        user_input = recognize_speech()

    if user_input:
        if user_input.lower() == "exit":
            st.write("Goodbye!")
            speak_text("Goodbye!")
            return
        elif user_input.lower().startswith("solve"):
            bot_response = agent.run(user_input[5:])
        else:
            # Call the FastAPI endpoint
            bot_response = call_fastapi_endpoint(user_input)
            
            if bot_response:
                st.session_state.messages.append({"role": "user", "content": user_input})
                st.session_state.messages.append({"role": "assistant", "content": bot_response})
                st.chat_message("assistant").markdown(bot_response)
                speak_text(bot_response)

    # Fixed Voice Assistant Loop
    if voice_assistant_active:
        st.warning("Voice Assistant is Active. Speak to interact.")
        while voice_assistant_active:
            user_input = recognize_speech()
            if user_input:
                bot_response = call_fastapi_endpoint(user_input)
                if bot_response:
                    st.session_state.messages.append({"role": "user", "content": user_input})
                    st.session_state.messages.append({"role": "assistant", "content": bot_response})
                    st.chat_message("assistant").markdown(bot_response)
                    speak_text(bot_response)

# Run FastAPI Server in a Separate Thread
def run_fastapi():
    uvicorn.run(app, host="0.0.0.0", port=8001)

# Start FastAPI server in the background
threading.Thread(target=run_fastapi, daemon=True).start()

if __name__ == "__main__":
    main()
