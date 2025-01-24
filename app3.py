import requests
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os


load_dotenv()
GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")


# Function to call Gemini API and generate a report
def generate_health_report(health_condition, additional_details=""):
    try:
        

        #prompt for the Gemini API
        prompt = (
            f"You are a highly experienced doctor. A patient has the following health condition: {health_condition}. "
            f"Additional details provided: {additional_details}. "
            f"Please provide a detailed report including the following sections:\n"
            f"1. Summary of the condition\n"
            f"2. Dos (recommendations to follow)\n"
            f"3. Don'ts (actions to avoid)."
        )

        # Example response simulation based on the prompt
        response = {
            "summary": f"The patient is experiencing issues related to {health_condition}.",
            "dos": ["Maintain a balanced diet", "Regular check-ups", "Stay hydrated"],
            "donts": ["Avoid excessive sugar", "Limit physical strain"]
        }

        print("Prompt processed successfully!")
        return response

    except Exception as e:
        print(f"Error: {e}")
        return None
    


llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")

# Main execution
def main():
    print("Welcome to the Health Report Generator")
    health_condition = input("Enter your health condition: ")
    additional_details = input("Enter any additional details (optional): ")

    report = generate_health_report(health_condition, additional_details)

    if report:
        print("\nGenerated Health Report:")
        print(f"Summary: {report['summary']}")
        print("\nDos:")

        for do in report["dos"]:
            print(f"- {do}")
        print("\nDon'ts:")
        for dont in report["donts"]:
            print(f"- {dont}")
    else:
        print("Failed to generate report.")

if __name__ == "__main__":
    main()
    
