"""English teacher chatbot in the terminal, showing LangChain conversation memory."""
import os

from dotenv import load_dotenv
from langchain_classic.chains import ConversationChain
from langchain_classic.memory import ConversationBufferWindowMemory, ConversationSummaryMemory
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")

if not GOOGLE_API_KEY:
    raise SystemExit("GOOGLE_API_KEY is not set. Copy .env.example to .env and paste your Gemini API key.")

chat = ChatGoogleGenerativeAI(model=GEMINI_MODEL, google_api_key=GOOGLE_API_KEY, temperature=0.7)

# The prompt for the chatbot to act as an English teacher
prompt_template = PromptTemplate(
    input_variables=["history", "input"],
    template=(
        "You are an English teacher. Engage in a conversation to help improve the user's English."
        "Respond to their queries, correct their grammar, and provide examples if needed."
        "Conversation history:\n{history}\nUser: {input}\nTeacher:"
    ),
)

# Memory options: a window memory that keeps the last 2 exchanges, or a summary memory.
buffer_memory = ConversationBufferWindowMemory(k=2)
summary_memory = ConversationSummaryMemory(llm=chat)

# Swap memory=buffer_memory for memory=summary_memory to try the other type.
conversation = ConversationChain(
    llm=chat,
    prompt=prompt_template,
    memory=buffer_memory,
)

print("Welcome! I'm your English teacher. How can I assist you today?")

while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit"]:
        print("Goodbye! Keep practicing your English.")
        break
    response = conversation.invoke({"input": user_input})["response"]
    print(f"Teacher: {response}")
