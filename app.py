"""Dr. Amit: describe symptoms in the terminal and get causes, do's/don'ts and suggestions."""
import os

from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()
GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")

if not GEMINI_API_KEY:
    raise SystemExit("GOOGLE_API_KEY is not set. Copy .env.example to .env and paste your Gemini API key.")

llm = ChatGoogleGenerativeAI(model=GEMINI_MODEL, google_api_key=GEMINI_API_KEY)

# Multi-step chain prompts
chat_prompt1 = ChatPromptTemplate.from_template(
    "Write two sentences explaining the features and cause of {symptoms} in a simple and clear way."
)

chat_prompt2 = ChatPromptTemplate.from_template(
    "From the features and cause: {features}, what are the do's and don'ts in this situation? Give a concise 2-sentence summary for each."
    " Suggest 3 medicines based on the symptom in points like this"
    "1...."
    "2...."
    "3...."
)

# LCEL: the output of chain1 feeds into prompt 2
chain1 = chat_prompt1 | llm | StrOutputParser()
chain2 = {"features": chain1} | chat_prompt2 | llm | StrOutputParser()

symptoms = input("                                         PLEASE DESCRIBE PATIENT SYMPTOMS: ")

response = chain2.invoke({"symptoms": symptoms})
print("\n                                            DR. AMIT MOHANTY HERE TO SAVE YOU \n")
print(response)

try:
    rating = int(input("\n                                     GIVE RATING TO DR. AMIT MOHANTY FROM 1 TO 10 : "))
except ValueError:
    rating = None

if rating is None:
    print("Neither thanks nor get lost.")
elif rating >= 7:
    prompt = "Act as a true gentleman and say beautiful words and sentences like how beautiful you are,best person ever and more in a 3 line paragraph"
    print(llm.invoke(prompt).text)
else:
    prompt2 = "Roast me in the funniest way possible, but keep it light-hearted and friendly. Make sure it’s clever and not mean-spirited!"
    print(llm.invoke(prompt2).text)
print("\n THANKS FOR VISITING DR. AMIT MOHANTY MBBS                                                    YOUR BILL IS $1000 + TAX + GST ONLY ")
