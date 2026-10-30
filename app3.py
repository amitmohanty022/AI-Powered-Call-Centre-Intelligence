"""Health report generator: asks Gemini for a summary, do's and don'ts."""
import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel, Field

load_dotenv()
GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")

if not GEMINI_API_KEY:
    raise SystemExit("GOOGLE_API_KEY is not set. Copy .env.example to .env and paste your Gemini API key.")


class HealthReport(BaseModel):
    summary: str = Field(description="Summary of the condition")
    dos: list[str] = Field(description="Recommendations to follow")
    donts: list[str] = Field(description="Actions to avoid")


llm = ChatGoogleGenerativeAI(model=GEMINI_MODEL, google_api_key=GEMINI_API_KEY)
structured_llm = llm.with_structured_output(HealthReport)


def generate_health_report(health_condition, additional_details=""):
    """Call Gemini and return a dict with summary, dos and donts (or None on error)."""
    try:
        prompt = (
            f"You are a highly experienced doctor. A patient has the following health condition: {health_condition}. "
            f"Additional details provided: {additional_details or 'none'}. "
            "Please provide a detailed report including the following sections:\n"
            "1. Summary of the condition\n"
            "2. Dos (recommendations to follow)\n"
            "3. Don'ts (actions to avoid)."
        )
        report = structured_llm.invoke(prompt)
        print("Prompt processed successfully!")
        return report.model_dump()
    except Exception as e:
        print(f"Error: {e}")
        return None


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
