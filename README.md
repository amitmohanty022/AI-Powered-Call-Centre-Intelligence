# AI-Powered-Call-Centre-Intelligence
AI-Powered Chatbot with Voice Assistant
This repository contains an AI-powered chatbot application built using **Streamlit** for the frontend and **FastAPI** for the backend. The chatbot is powered by **Google Generative AI (Gemini)** via LangChain and features a voice assistant for speech-to-text and text-to-speech interaction.

---
pip install -r requirements.txt

## Required Libraries
- **python-dotenv** – To manage environment variables.
- **streamlit** – For building the web app interface.
- **langchain**-google-genai – LangChain integration for Google Gemini AI.
- **langchain** – Framework for conversational AI workflows.
- **pyttsx3** – Text-to-speech functionality.
- **SpeechRecognition** – For capturing and processing voice input.
- **langsmith** – Monitoring and tracing LangChain workflows.
- **fastapi** – For building the REST API.
- **pydantic** – For validating API request/response models.
- **requests** – For making HTTP requests to FastAPI.
- **uvicorn** – ASGI server for running FastAPI.
---
## Features

- **Conversational AI**: Integrates Google Generative AI (Gemini) for natural and intelligent responses.
- **Voice Assistant**:
  - Recognizes speech input using `speech_recognition`.
  - Converts chatbot responses to audio using `pyttsx3`.
- **Streamlit Frontend**: Provides an intuitive user interface for text and voice-based interaction.
- **FastAPI Backend**: Efficient and lightweight REST API for chatbot processing.
- **Math Solving Agent**: Supports solving math queries via LangChain tools.
- **Traceable Conversations**: Tracks and summarizes chat history using LangSmith.

---

## Requirements

### Libraries

Ensure you have Python 3.8 or higher installed. Install the following libraries using `pip`:

## Project Architecture
- **Backend (FastAPI)**
Handles chatbot queries via a REST API (/chat).
Uses LangChain and Google Generative AI to process inputs and generate responses.
- **Frontend (Streamlit)**
User-friendly interface for interaction.
Handles voice and text input/output.
- **Voice Assistant**
  Speech-to-text: Uses SpeechRecognition.
  Text-to-speech: Uses pyttsx3.
- **Conversation Memory**
Maintains session-level memory using LangChain's ConversationSummaryMemory.

## Future Enhancements
Add multi-language support for voice input and output.
Implement advanced error handling and retry mechanisms.
Optimize voice assistant performance for long-running interactions.
Add deployment instructions for Docker or cloud platforms (e.g., AWS, GCP).

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Contact
For questions or support, contact:

- *Amit Kumar Mohanty*
- *GitHub: @amitmohanty022*
- *Email: mohantyamit2003@gmail.com*
