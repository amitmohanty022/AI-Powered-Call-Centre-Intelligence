from langchain.chains import ConversationChain
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory, ConversationSummaryMemory
from langchain_google_genai import ChatGoogleGenerativeAI

# API
chat = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key="AIzaSyCNEvYTmW-C0fe9PbGbMd_CCsUa0JaYKRg", temperature=0.7)

# the prompt for the chatbot to act as an English teacher
prompt_template = PromptTemplate(
    input_variables=["history", "input"],
    template=(
        "You are an English teacher. Engage in a conversation to help improve the user's English."
        "Respond to their queries, correct their grammar, and provide examples if needed."
        "Conversation history:\n{history}\nUser: {input}\nTeacher:"
    )
)

# Set up memory modules
buffer_memory = ConversationBufferMemory(k=2) # A buffer memory with a fixed length of 2 previous exchanges
summary_memory = ConversationSummaryMemory(llm=chat)

# Combine memory modules into a single conversation chain      /// Change buffer memory ,summary memory
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
    # print(buffer_memory.chat_memory.messages)
    response = conversation.run(input=user_input)
    print(f"Teacher: {response}")
