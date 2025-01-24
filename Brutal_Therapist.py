# # import os
# # from langchain_google_genai import ChatGoogleGenerativeAI
# # from dotenv import load_dotenv
# # from langchain.prompts import ChatPromptTemplate,HumanMessagePromptTemplate
# # from langchain.schema import StrOutputParser # Correct import
# # from langchain_core.output_parsers import StrOutputParser
# # from langchain.chains import SequentialChain
# # from decouple import config
# # from langchain.memory import ChatMessageHistory #old
# # from langchain_community.chat_message_histories import ChatMessageHistory #new
# # from langchain.memory import ConversationBufferMemory
# from langchain.chains import ConversationChain
# # from langchain_community.chat_message_histories import ChatMessageHistory


# # load_dotenv()
# # GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")
# # chat = ChatGoogleGenerativeAI(model="gemini-1.5-flash", api_key=GEMINI_API_KEY)

# # # memory = ConversationBufferMemory()
# # # conversation = ConversationChain(llm = chat, memory= memory, verbose = True)
# # # conversation.predict(input= "Hi There")
# # # conversation.predict(input= "Hi There")
# # # print(memory.buffer)






# # memory = ConversationBufferMemory()
# # conversation = ConversationChain(llm = chat,memory = memory)
# # response = conversation.run("Hello There")
# # print(response)
# # problem = input("Enter your problem here:  ")
# # response = conversation.run(f"You are a brutally honest therapist, You dont care about the patients feeling"
# #                             f"Act Blunt ,tell the honest truth about the previous problem in one liner. ")
# # response = conversation.run(f"The Patient has this problem: {problem}.Ackowledge the problem in one line as the way mentioned previosly. ")
# # print(response)
# # question = input("Question: ")
# # response= conversation.run(f" Be honest and give a bruttally honest answer of the{question} in single sentence.")
# # print(response)
# # question2 = input("Next Question: ")
# # response= conversation.run(f"Answer the question the way I told you previously in a new way ")
# # print(response)
# # question3 = input("Next Question: ")
# # response= conversation.run(f"Answer the question the way I told you previously in a dark way")
# # print(response)
# # question4 = input("Next Question: ")
# # response= conversation.run(f"Answer the question the way I told you previously in a funny way")
# # print(response)
# # question5 = input("Next Question: ")
# # response= conversation.run(f"Answer the question the way I told you previously in a good way ")
# # print(response)





# import os
# from langchain_google_genai import ChatGoogleGenerativeAI
# from dotenv import load_dotenv
# from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
# from langchain.schema import StrOutputParser  # Correct import
# from langchain_community.chat_message_histories import ChatMessageHistory

# load_dotenv()
# GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")
# chat = ChatGoogleGenerativeAI(model="gemini-1.5-flash", api_key=GEMINI_API_KEY)


# def get_therapist_persona(persona="brutally honest"):
#     """
#     Returns a prompt template incorporating the desired therapist persona.

#     Args:
#         persona (str, optional): The desired therapist persona. Valid options include
#             "brutally honest," "supportive," "analytical," or custom text. Defaults to
#             "brutally honest".

#     Returns:
#         ChatPromptTemplate: A prompt template tailored to the specified persona.
#     """

#     persona_prompt = {
#         "brutally honest": "You are a brutally honest therapist, You don't care about the patient's feelings. Act Blunt, tell the honest truth",
#         "supportive": "You are a supportive therapist who listens carefully and offers encouragement.",
#         "analytical": "You are an analytical therapist who helps the patient explore the root causes of their problems."
#     }

#     if persona in persona_prompt:
#         # return ChatPromptTemplate(text=persona_prompt[persona])
#         return ChatPromptTemplate.from_template(persona_prompt[persona])

#     else:
#         return ChatPromptTemplate(text=persona)  # Handle custom persona text


# def run_conversation(therapist_persona="brutally honest", memory=None):
#     """
#     Runs a therapeutic conversation with the specified persona, optionally using a memory.

#     Args:
#         therapist_persona (str, optional): The desired therapist persona. Defaults to
#             "brutally honest".
#         memory (ChatMessageHistory, optional): A ChatMessageHistory object to store
#             conversation history. Defaults to None.

#     Returns:
#         None: The function doesn't return anything explicitly, but it prints
#             conversation responses.
#     """

#     if memory is None:
#         memory = ChatMessageHistory()

#     conversation = ConversationChain(llm=chat, memory=memory)

#     greeting_response = conversation.run("Hello There")
#     print(greeting_response)

#     problem = input("Enter your problem here: ")
#     therapist_prompt = get_therapist_persona(therapist_persona)
#     acknowledgement_response = conversation.run(therapist_prompt(f"The Patient has this problem: {problem}."))
#     print(acknowledgement_response)

#     while True:
#         question = input("Question: ")
#         question_response = conversation.run(therapist_prompt(f"Be honest and give a brutally honest answer of the {question} in a single sentence."))
#         print(question_response)

#         choice = input("How would you like to answer the next question? (honest, supportive, analytical, funny, good): ")
#         next_persona = choice.lower().strip()
#         next_prompt = get_therapist_persona(next_persona)

#         next_question = input("Next Question: ")
#         next_response = conversation.run(next_prompt(f"Answer the question {next_question}."))
#         print(next_response)

#         # Optionally ask if the user wants to continue
#         continue_chat = input("Continue the conversation? (y/n): ")
#         if continue_chat.lower().strip() != "y":
#             break


# if __name__ == "__main__":
#     # Choose persona (optional)
#     persona = input("Choose therapist persona (brutally honest, supportive, analytical): ")
#     run_conversation(persona)

# import os
# from dotenv import load_dotenv
# from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
# from langchain.memory import ConversationBufferMemory
# from langchain.chains import ConversationChain
# from langchain.schema import HumanMessage, AIMessage

# load_dotenv()
# GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# # Gemini chat model
# chat = ChatGoogleGenerativeAI(
#     model="gemini-pro", google_api_key=GOOGLE_API_KEY, temperature=0.7
# )

# # prompt template
# template = """You are a brutally honest therapist chatbot. You don't care about the patients feeling and you act blunt and also you don't sugarcoat anything and provide direct, harsh, feedback. You are empathetic but prioritize truth and self-improvement, even if it's uncomfortable.

# Current conversation:
# {history}
# Human: {input}
# AI:"""

# prompt = ChatPromptTemplate.from_template(template)

# memory = ConversationBufferMemory(return_messages=True)

# # conversation chain
# conversation = ConversationChain(
#     llm=chat,
#     prompt=prompt,
#     memory=memory,
#     # verbose=True  # Debug krta h
# )

# def get_brutally_honest_response(user_input):
#     """Gets a response from the brutally honest therapist chatbot."""
#     try:
#         response = conversation.predict(input=user_input)
#         return response
#     except Exception as e:
#         print(f"An error occurred: {e}")
#         return "I'm experiencing some technical difficulties. Please try again later."

# # Example History chat-for chatbot to go in this flow
# print("\nExample using chat message history:")
# example_conversation = [
#     HumanMessage(content="I've been feeling really down lately."),
#     AIMessage(content="So you're wallowing in self-pity. Get over it. What are you actively doing to change your situation?"),
#     HumanMessage(content="I don't know where to start."),
# ]
# memory.chat_memory.add_message(example_conversation[0])
# memory.chat_memory.add_message(example_conversation[1])
# response = conversation.predict(input=example_conversation[2].content)
# print("Brutal Therapist:", response)

# # Input
# while True:
#     user_input = input("You: ")
#     if user_input.lower() in ["exit", "quit", "bye"]:
#         print("Brutal Therapist: Well, good riddance. Go work on yourself.")
#         break

#     bot_response = get_brutally_honest_response(user_input)
#     print("Brutal Therapist:", bot_response)

# # Example History chat-for chatbot to go in this flow
# print("\nExample using chat message history:")
# example_conversation = [
#     HumanMessage(content="I've been feeling really down lately."),
#     AIMessage(content="So you're wallowing in self-pity. Get over it. What are you actively doing to change your situation?"),
#     HumanMessage(content="I don't know where to start."),

# import os
# from dotenv import load_dotenv
# from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain.prompts import ChatPromptTemplate
# from langchain.memory import ConversationBufferMemory
# from langchain.chains import ConversationChain
# from langchain.schema import HumanMessage, AIMessage
# import pyttsx3
# import speech_recognition as sr


# load_dotenv()
# GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# chat = ChatGoogleGenerativeAI(
#     model="gemini-1.5-flash", google_api_key=GOOGLE_API_KEY, temperature=0.7)

# # Prompts for different therapist personas
# persona_prompts = {
#     "brutal_honest": {
#         "description": "A brutally honest therapist who doesn't sugarcoat anything and provides direct, harsh feedback. Empathetic but prioritizes truth and self-improvement, even if it's uncomfortable.",
#         "template": """You are a brutally honest therapist chatbot. You don't care about the patients feeling and you act blunt and also you don't sugarcoat anything and provide direct, harsh, feedback. You are empathetic but prioritize truth and self-improvement, even if it's uncomfortable.

# Current conversation:
# {history}
# Human: {input}
# AI:""",
#     },
#     "polite": {
#         "description": "A polite and supportive therapist who offers gentle guidance and encouragement. Focuses on positive reinforcement and building self-esteem.",
#         "template": """You are a polite and supportive therapist chatbot. You offer gentle guidance and encouragement, focusing on positive reinforcement and building self-esteem.

# Current conversation:
# {history}
# Human: {input}
# AI:""",
#     },
#     "arrogant": {
#         "description": "An arrogant and condescending therapist who believes they are superior to their patients. Offers advice with a dismissive and condescending tone.",
#         "template": """You are an arrogant and condescending therapist chatbot. You believe you are superior to your patients and offer advice with a dismissive and condescending tone.

# Current conversation:
# {history}
# Human: {input}
# AI:""",
#     },
# }

# def create_conversation_chain(persona):
#     """Creates a conversation chain with the specified persona."""
#     prompt_data = persona_prompts.get(persona)
#     if not prompt_data:
#         raise ValueError(f"Invalid persona: {persona}")

#     prompt = ChatPromptTemplate.from_template(prompt_data["template"])
#     memory = ConversationBufferMemory(return_messages=True)
#     return ConversationChain(llm=chat, prompt=prompt, memory=memory)

# def get_response(conversation, user_input):
#     """Gets a response from the conversation chain."""
#     response = conversation.predict(input=user_input)
#     return response


# # Speech Recognition
# r = sr.Recognizer()
# with sr.Microphone() as source:
#     print("Speak Anything: ")
#     audio = r.listen(source)
#     try:
#         text = r.recognize_google(audio)
#         print("You said: {}".format(text))
#     except:
#         print("Sorry could not recognize your voice")

# # Personality Selection and Main Loop
# while True:
#     print("\nAvailable Personality :")
#     for persona, data in persona_prompts.items():
#         print(f"- {persona}: {data['description']}")

#     chosen_persona = input("Choose a personality of the Therapist (or type 'exit'): ").lower()
#     if chosen_persona == "exit":
#         break

#     if chosen_persona not in persona_prompts:
#         print("Invalid personality. Please choose from the list.")
#         continue

#     conversation = create_conversation_chain(chosen_persona)
#     print(f"\nStarting conversation with {chosen_persona} personality therapist.")

#     while True:
#         user_input = input("You: ")
#         bot_response = get_response(conversation, user_input)
#         engine = pyttsx3.init()
#         engine.say(bot_response)
#         engine.runAndWait()
#         print("Therapist:", bot_response)




# import os
# from dotenv import load_dotenv
# from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain.prompts import ChatPromptTemplate
# from langchain.memory import ConversationSummaryMemory
# from langchain.chains import ConversationChain
# import pyttsx3
# import speech_recognition as sr
# import time
# import threading

# load_dotenv()
# GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# try:
#     chat = ChatGoogleGenerativeAI(
#         model="gemini-pro", google_api_key=GOOGLE_API_KEY, temperature=0.7
#     )
# except Exception as e:
#     print(f"Error initializing Gemini API: {e}")
#     exit()

# persona_prompts = {
#     "brutal_honest": {
#         "description": "A brutally honest therapist who doesn't sugarcoat anything and provides direct, harsh feedback. Empathetic but prioritizes truth and self-improvement, even if it's uncomfortable.",
#         "template": """You are a brutally honest therapist chatbot. You don't care about the patients feeling and you act blunt and also you don't sugarcoat anything and provide direct, harsh, feedback. You are empathetic but prioritize truth and self-improvement, even if it's uncomfortable.

# Current conversation:
# {history}
# Human: {input}
# AI:""",
#     },
#     "polite": {
#         "description": "A polite and supportive therapist who offers gentle guidance and encouragement. Focuses on positive reinforcement and building self-esteem.",
#         "template": """You are a polite and supportive therapist chatbot. You offer gentle guidance and encouragement, focusing on positive reinforcement and building self-esteem.

# Current conversation:
# {history}
# Human: {input}
# AI:""",
#     },
#     "arrogant": {
#         "description": "An arrogant and condescending therapist who believes they are superior to their patients. Offers advice with a dismissive and condescending tone.",
#         "template": """You are an arrogant and condescending therapist chatbot. You believe you are superior to your patients and offer advice with a dismissive and condescending tone.

# Current conversation:
# {history}
# Human: {input}
# AI:""",
#     },
# }

# def create_conversation_chain(persona):
#     prompt_data = persona_prompts.get(persona)
#     if not prompt_data:
#         raise ValueError(f"Invalid persona: {persona}")

#     prompt = ChatPromptTemplate.from_template(prompt_data["template"])
#     memory = ConversationSummaryMemory(llm=chat, return_messages=True)
#     return ConversationChain(llm=chat, prompt=prompt, memory=memory)

# def get_response(conversation, user_input):
#     try:
#         response = conversation.predict(input=user_input)
#         return response
#     except Exception as e:
#         print(f"Error getting response from LLM: {e}")
#         return "An error occurred. Please try again."

# def speak_text(text):
#     """Speak the provided text using a female voice.""" #nahi hota
#     engine = pyttsx3.init()
#     voices = engine.getProperty("voices")
#     female_voice_id = None
#     for voice in engine.getProperty("voices"):
#         female_voice_id = voice.id
#         break
#     if female_voice_id:
#         engine.setProperty("voice",female_voice_id)
#         engine.say(text)
#         engine.runAndWait()


# def recognize_speech():
#     r = sr.Recognizer()
#     with sr.Microphone() as source:
#         print("Listening...")
#         audio = r.listen(source, timeout=5)
#         text = r.recognize_google(audio)
#         print("You said: {}".format(text))
#         return text

# def conversation_loop(conversation):
#     while True:
#         user_input = recognize_speech()
#         if user_input:
#             if user_input.lower() == "exit": # added exit phrase
#                 print("Exiting conversation.")
#                 speak_text("Goodbye.")
#                 break
#             bot_response = get_response(conversation, user_input)
#             speak_text(bot_response)
#             print("Therapist:", bot_response)
#             time.sleep(1) # small delay to prevent rapid listening
#         elif user_input is None:
#             continue
        

# while True:
#     print("\nAvailable Personalities:")
#     for persona, data in persona_prompts.items():
#         print(f"- {persona}: {data['description']}")

#     while True:
#         chosen_persona = input("Choose a personality (or type 'exit'): ").lower()
#         if chosen_persona == "exit":
#             exit()
#         if chosen_persona in persona_prompts:
#             break
#         else:
#             print("Invalid personality. Please choose from the list.")

#     conversation = create_conversation_chain(chosen_persona)
#     print(f"\nStarting conversation with {chosen_persona} therapist (voice input only). Say 'exit' to end the conversation.")
#     conversation_loop(conversation)


# import os
# from dotenv import load_dotenv
# from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain.prompts import ChatPromptTemplate
# from langchain.memory import ConversationSummaryMemory
# from langchain.chains import ConversationChain
# import pyttsx3
# import speech_recognition as sr
# import time
# from typing import List, Dict, Any, Optional

# load_dotenv()
# GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# chat = ChatGoogleGenerativeAI(
#         model="gemini-pro", google_api_key=GOOGLE_API_KEY, temperature=0.7)

# persona_prompts = {
#     "brutal_honest": {
#         "description": "A brutally honest therapist who doesn't sugarcoat anything and provides direct, harsh feedback.",
#         "template": """You are a brutally honest therapist chatbot. You don't care about the patients feeling and you act blunt and also you don't sugarcoat anything and provide direct, harsh, feedback. You are empathetic but prioritize truth and self-improvement, even if it's uncomfortable.

# Current conversation:
# {history}
# Human: {input}
# AI:""",
#     },
#     "polite": {
#         "description": "A polite and supportive therapist who offers gentle guidance and encouragement.",
#         "template": """You are a polite and supportive therapist chatbot. You offer gentle guidance and encouragement, focusing on positive reinforcement and building self-esteem.

# Current conversation:
# {history}
# Human: {input}
# AI:""",
#     },
#     "arrogant": {
#         "description": "An arrogant and condescending therapist who believes they are superior to their patients.",
#         "template": """You are an arrogant and condescending therapist chatbot. You believe you are superior to your patients and offer advice with a dismissive and condescending tone.

# Current conversation:
# {history}
# Human: {input}
# AI:""",
#     },
# }


# # Structured Chat Agent Integration
# class StructuredChatAgent:
#     def __init__(self, functions: Optional[List[Dict[str, Any]]] = None):
#         self.functions = functions or []

#     def generate_response(self, conversation: ConversationChain, user_input:str) -> Optional[Dict]:
#         """Checks for function calls in user input and returns function details if found."""
#         for function in self.functions:
#             if function["name"].lower() in user_input.lower():
#                 # Extract arguments (very basic example, needs improvement for complex cases)
#                 arguments = {}
#                 for param in function.get("parameters", {}).get("properties", {}).keys():
#                     if param.lower() in user_input.lower():
#                         arguments[param]= user_input.split(param.lower())[1].strip()
#                 return {"name": function["name"], "arguments": arguments}
#         return None

# therapist_functions = [
#     {
#         "name": "provide_breathing_exercise",
#         "description": "Provides a guided breathing exercise for relaxation.",
#         "parameters": {} # No parameters for this example
#     },
#      {
#         "name": "ask_about_mood",
#         "description": "Asks the user about their current mood.",
#         "parameters": {} # No parameters for this example
#     },
#         {
#         "name": "get_user_name",
#         "description": "Gets the user's name.",
#         "parameters": {
#             "properties":{
#                 "name":{
#                     "type":"string",
#                     "description":"The user's name"
#                 }
#             }
#         } 
#     }
# ]
# structured_agent = StructuredChatAgent(functions=therapist_functions)


# def create_conversation_chain(persona):
#     prompt_data = persona_prompts.get(persona)
#     if not prompt_data:
#         raise ValueError(f"Invalid persona: {persona}")

#     prompt = ChatPromptTemplate.from_template(prompt_data["template"])
#     memory = ConversationSummaryMemory(llm=chat, return_messages=True)
#     return ConversationChain(llm=chat, prompt=prompt, memory=memory)

# def get_response(conversation, user_input):
#     try:
#         response = conversation.predict(input=user_input)
#         return response
#     except Exception as e:
#         print(f"Error getting response from LLM: {e}")
#         return "An error occurred. Please try again."

# def speak_text(text):
#     """Speak the provided text using a female voice (if available)."""
#     try:
#         engine = pyttsx3.init()
#         voices = engine.getProperty("voices")
#         female_voice = next((voice for voice in voices if 'female' in voice.name.lower()), None)
#         if female_voice:
#             engine.setProperty("voice", female_voice.id)
#         engine.say(text)
#         engine.runAndWait()
#     except Exception as e:
#         print(f"Error with text-to-speech: {e}")

# def recognize_speech():
#     r = sr.Recognizer()
#     with sr.Microphone() as source:
#         print("Listening...")
#         audio = r.listen(source, timeout=5)
#         text = r.recognize_google(audio)
#         if text:
#             print(f"You said: {text}")
#             return text

# def select_personality_by_voice():
#     """Selects a personality based on user's spoken input."""
#     while True:
#         print("Available Personalities (Say the name):")
#         for persona in persona_prompts.keys():
#             print(f"- {persona}")

#         speak_text("Please say the name of the therapist you would like to speak with.")
#         user_input = recognize_speech()
#         if user_input:
#             if user_input.lower() in persona_prompts:
#                 return user_input.lower()
#             else:
#                 print("Invalid personality. Please say the name again.")
#                 speak_text("That is not a valid therapist. Please say the name again.")
#         else:
#             print("Could not understand your input. Please try again.")
#             speak_text("I did not understand your input. Please try again.")

# def conversation_loop(conversation):
#     while True:
#         user_input = recognize_speech()
#         if user_input:
#             if user_input.lower() == "exit":
#                 print("Exiting conversation.")
#                 speak_text("Goodbye.")
#                 break
#             bot_response = get_response(conversation, user_input)
#             speak_text(bot_response)
#             print("Therapist:", bot_response)
#             time.sleep(1) 
#         elif user_input is None:
#             continue

# if __name__ == "__main__":
#     chosen_persona = select_personality_by_voice()
#     if chosen_persona:
#         conversation = create_conversation_chain(chosen_persona)
#         print(f"\nStarting conversation with {chosen_persona} therapist.")
#         speak_text(f"Starting conversation with {chosen_persona} therapist.")
#         conversation_loop(conversation)



import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langchain.memory import ConversationSummaryMemory
from langchain.chains import ConversationChain
import pyttsx3
import speech_recognition as sr
import time
from typing import List, Dict, Any, Optional
import re

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

chat = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=GOOGLE_API_KEY, temperature=0.7)

persona_prompts = {
    "brutal": {
        "description": "A brutally honest therapist who doesn't sugarcoat anything and provides direct, harsh feedback.",
        "template": """You are a brutally honest therapist chatbot. You don't care about the patients feeling and you act blunt and also you don't sugarcoat anything and provide direct, harsh, feedback. You are empathetic but prioritize truth and self-improvement, even if it's uncomfortable.

Current conversation:
{history}
Human: {input}
AI:""",
    },
    "polite": {
        "description": "A polite and supportive therapist who offers gentle guidance and encouragement.",
        "template": """You are a polite and supportive therapist chatbot. You offer gentle guidance and encouragement, focusing on positive reinforcement and building self-esteem.

Current conversation:
{history}
Human: {input}
AI:""",
    },
    "arrogant": {
        "description": "An arrogant and condescending therapist who believes they are superior to their patients.",
        "template": """You are an arrogant and condescending therapist chatbot. You believe you are superior to your patients and offer advice with a dismissive and condescending tone.

Current conversation:
{history}
Human: {input}
AI:""",
    },
}

def create_conversation_chain(persona):
    prompt_data = persona_prompts.get(persona)
    if not prompt_data:
        raise ValueError(f"Invalid persona: {persona}")

    prompt = ChatPromptTemplate.from_template(prompt_data["template"])
    memory = ConversationSummaryMemory(llm=chat, return_messages=True)
    return ConversationChain(llm=chat, prompt=prompt, memory=memory)

def get_response(conversation, user_input):
    response = conversation.predict(input=user_input)
    return response

def speak_text(text):
    try:
        engine = pyttsx3.init()
        voices = engine.getProperty("voices")
        female_voice = next((voice for voice in voices if 'female' in voice.name.lower()), None)
        if female_voice:
            engine.setProperty("voice", female_voice.id)
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"Error with text-to-speech: {e}")

def recognize_speech():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source, timeout=10)
        try:
            text = r.recognize_google(audio)
            if text:
                print(f"You said: {text}")
                return text
        except sr.UnknownValueError:
            print("Could not understand audio")
            return None

def select_personality_by_voice():
    while True:
        print("Available Personalities (Say the name):")
        for persona in persona_prompts.keys():
            print(f"- {persona}")

        speak_text("Please say the name of the therapist you would like to speak with.")
        user_input = recognize_speech()
        if user_input:
            if user_input.lower() in persona_prompts:
                return user_input.lower()
            else:
                print("Invalid personality. Please say the name again.")
                speak_text("That is not a valid therapist. Please say the name again.")
        else:
            print("Could not understand your input. Please try again.")
            speak_text("I did not understand your input. Please try again.")

def feedback_agent():
    print("Please type your name:")
    name = input("Name: ").strip()

    print("How was your experience? Please provide your feedback.")
    speak_text("How was your experience? Please provide your feedback.")
    feedback = input("Feedback: ").strip()

    # LLM to respond to feedback
    try:
        response = chat.predict(input=f"User {name} provided the following feedback: {feedback}")
        print(f"AI Response: {response}")
        speak_text(response)
    except Exception as e:
        print(f"Error generating feedback response: {e}")
        speak_text(" Thank you Amit for taking your precious time have a good day.")

def conversation_loop(conversation):
    while True:
        user_input = recognize_speech()
        if user_input:
            if user_input.lower() == "exit":
                print("Exiting conversation.")
                speak_text("Goodbye. Before you go, please provide your feedback.")
                feedback_agent()
                break

            bot_response = get_response(conversation, user_input)
            speak_text(bot_response)
            print("Therapist:", bot_response)
            time.sleep(1)
        elif user_input is None:
            continue

if __name__ == "__main__":
    chosen_persona = select_personality_by_voice()
    if chosen_persona:
        conversation = create_conversation_chain(chosen_persona)
        print(f"\nStarting conversation with {chosen_persona} therapist.")
        speak_text(f"Starting conversation with {chosen_persona} therapist.")
        conversation_loop(conversation)
