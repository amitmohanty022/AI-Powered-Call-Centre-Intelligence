import os
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser # Correct import
from langchain.chains import SequentialChain

load_dotenv()
GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")

llm = ChatGoogleGenerativeAI(model="gemini-1.5-flashgemini-1.5-flash", api_key=GEMINI_API_KEY)





#MultiLine Chain Prompts
chat_prompt1 = ChatPromptTemplate.from_template(
    "Write two sentences explaining the features and cause of {symptoms} in a simple and clear way."
)

chat_prompt2 = ChatPromptTemplate.from_template(
    "From the features: {features} and cause: {cause}, what are the do's and don'ts in this situation? Give a concise 2-sentence summary for each."
    " Suggest 3 medicines based on the symptom in points like this"
    "1...."
    "2...."
    "3...."
)
# chat_prompt3 = ChatPromptTemplate.from_template(
#     "From The don'ts: {donts}, make a one liner good humor joke."
# )

# LCEL
chain1 = chat_prompt1 | llm | StrOutputParser()
chain2 = {"features": chain1, "cause": chain1} | chat_prompt2 | llm | StrOutputParser()
# chain3 = {"features": chain1, "cause": chain1, "donts": chain2} | chat_prompt3 | llm | StrOutputParser

symptoms = input("                                         PLEASE DESCRIBE PATIENT SYMPTOMS: ")


response = chain2.invoke({"symptoms": symptoms})
print("\n                                            DR. AMIT MOHANTY HERE TO SAVE YOU \n")
print(response)

rating = int(input("\n                                     GIVE RATING TO DR. AMIT MOHANTY FROM 1 TO 10 : "))

if rating >= 7:
    prompt= "Act as a true gentleman and say beautiful words and sentences like how beautiful you are,best person ever and more in a 3 line paragraph"
    response1 = llm.invoke(prompt)
    print(response1.content)
elif rating < 7:
    prompt2= "Roast me in the funniest way possible, but keep it light-hearted and friendly. Make sure it’s clever and not mean-spirited!"
    response2 = llm.invoke(prompt2)
    print(response2.content)
else:
    print("Neither thanks nor get lost.")
print("\n THANKS FOR VISITING DR. AMIT MOHANTY MBBS                                                    YOUR BILL IS $1000 + TAX + GST ONLY ")
