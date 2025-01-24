import streamlit as st
import os
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langsmith import traceable
import pyttsx3
import speech_recognition as sr
import threading
from queue import Queue
import time
import re

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "customer_care_bot"

load_dotenv()
Langchain_api_key=os.environ["LANGCHAIN_API_KEY"]
speech_queue = Queue()
should_stop = False

def speech_worker():
    while True:
        if not speech_queue.empty():
            text = speech_queue.get()
            try:
                engine = pyttsx3.init()
                engine.setProperty('rate', 200)
                engine.setProperty('volume', 1.0)
                engine.say(text)
                engine.runAndWait()
                engine.stop()
            except Exception as e:
                print(f"TTS Error: {e}")
            finally:
                speech_queue.task_done()
        time.sleep(0.1)  # Small delay to prevent CPU overuse

# Start the worker thread
speech_thread = threading.Thread(target=speech_worker, daemon=True)
speech_thread.start()

# Initialize LLM
llm = ChatGoogleGenerativeAI(
    temperature=0.7,
    model="gemini-1.5-flash",
    google_api_key=os.environ["GOOGLE_API_KEY"]
)

memory = ConversationBufferMemory()

prompt = PromptTemplate(
    input_variables=["chat_history", "user_input", "product_problem"],
    template=(
        "You are a customer support representative. Answer user queries in **concise points** only. "
        "Do not write long paragraphs or unnecessary details.\n\n"
        "The user described their problem: {product_problem}\n\n"
        "Chat History:\n{chat_history}\n\n"
        "User: {user_input}\n\n"
        "Agent (in concise points):"
    )
)

chain = LLMChain(
    llm=llm,
    prompt=prompt
)


@traceable(project_name="customer_care_bot")
def run_chain(user_input, chat_history, product_problem):
    return chain.run(
        chat_history=chat_history,
        user_input=user_input,
        product_problem=product_problem
    )


# Manage session state for speaking and recording
if "is_speaking" not in st.session_state:
    st.session_state["is_speaking"] = False
if "is_recording" not in st.session_state:
    st.session_state["is_recording"] = False

# Clean response for speech
def clean_response_for_speech(response):
    response = re.sub(r"[*_\-\n]", " ", response)  # Remove *, _, -, and line breaks
    response = re.sub(r"\s+", " ", response)  # Remove extra spaces
    return response.strip()

# Handle audio input
def get_audio_input():
    recognizer = sr.Recognizer()
    
    # Adjust recognition parameters
    recognizer.dynamic_energy_threshold = True
    recognizer.energy_threshold = 300
    recognizer.pause_threshold = 1.2
    
    with sr.Microphone() as source:
        st.info("Adjusting for background noise... Please wait")
        # Longer ambient noise adjustment
        recognizer.adjust_for_ambient_noise(source, duration=2)
        
        st.info("🎤 Listening... Please speak now!")
        try:
            # Increased timeout and phrase time
            audio = recognizer.listen(
                source,
                timeout=12,  # Wait longer for speech to start
                phrase_time_limit=15  # Allow longer phrases
            )
            
            st.info("Processing your speech...")
            user_input = recognizer.recognize_google(audio, language='en-US')
            
            if user_input:
                st.success(f"You said: {user_input}")
                return user_input
            
        except sr.WaitTimeoutError:
            st.warning("⏱️ Listening timed out. Please try again and speak when prompted.")
        except sr.UnknownValueError:
            st.warning("🎯 Could not understand the audio. Please speak clearly and try again.")
        except sr.RequestError as e:
            st.error(f"🔧 Speech Recognition service error: {e}")
        except Exception as e:
            st.error(f"❌ An unexpected error occurred: {e}")
        
        return ""

# Speak in a thread
def speak_in_thread(response):
    if not st.session_state.get("is_speaking", False):
        st.session_state["is_speaking"] = True
        try:
            cleaned_text = clean_response_for_speech(response)
            speech_queue.put(cleaned_text)
        except Exception as e:
            print(f"Error queuing speech: {e}")
        finally:
            st.session_state["is_speaking"] = False

# Stop voice output
def stop_speech():
    if st.session_state.get("is_speaking", False):
        try:
            while not speech_queue.empty():
                speech_queue.get()
                speech_queue.task_done()
            st.session_state["is_speaking"] = False
            st.info("Speech paused.")
        except Exception as e:
            print(f"Error stopping speech: {e}")

st.set_page_config(page_title="Customer Care Chatbot", layout="centered")
st.title("Customer Care Chatbot")

# Initialize session state variables
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

if "product_problem" not in st.session_state:
    st.session_state["product_problem"] = ""

# Step 1: Describe the Problem
if not st.session_state["product_problem"]:
    st.subheader("Step 1: Describe Your Problem")
    product_problem_input = st.text_area("What issue are you facing with your product?")
    if st.button("Submit Problem"):
        if product_problem_input.strip():
            st.session_state["product_problem"] = product_problem_input.strip()
            st.success(f"Problem noted: {st.session_state['product_problem']}")
        else:
            st.warning("Please describe your problem.")
else:
    st.subheader(f"Problem: {st.session_state['product_problem']}")

    st.subheader("Chat with the Support Bot")

    # Display chat history
    for i, chat in enumerate(st.session_state["chat_history"]):
        st.text_area(f"User {i + 1}:", value=chat["user"], key=f"user_{i}", disabled=True)
        st.text_area(f"Agent {i + 1}:", value=chat["agent"], key=f"agent_{i}", disabled=True)

    # User Input
    user_input = ""
    if st.button("Use Voice Input"):
        st.session_state["is_recording"] = True
        user_input = get_audio_input()
        st.session_state["is_recording"] = False

    user_input = user_input or st.text_input("Or type your message below:", key="chat_input", label_visibility="collapsed")

    if user_input.strip():
        try:
            chat_history_text = "\n".join(
                [f"User: {item['user']}\nAgent: {item['agent']}" for item in st.session_state["chat_history"]]
            )
            response = chain.run(
                chat_history=chat_history_text,
                user_input=user_input,
                product_problem=st.session_state["product_problem"]
            )
            st.session_state["chat_history"].append({"user": user_input, "agent": response.strip()})
            st.text_area("Agent's Response (Text):", value=response.strip(), disabled=True)

            if st.button("Stop Voice"):
                stop_speech()
            else:
                speak_in_thread(response.strip())
        except Exception as e:
            st.error(f"An error occurred: {e}")

    if st.button("Stop Recording") and st.session_state["is_recording"]:
        st.session_state["is_recording"] = False
        st.warning("Recording stopped.")

    if st.button("Reset Chat"):
        st.session_state["product_problem"] = ""
        st.session_state["chat_history"] = []
        memory.clear()
        stop_speech()
        st.success("Chat reset successfully!")
