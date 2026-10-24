# AI-Powered Call Centre Intelligence

A set of LLM-powered assistants for call-centre style conversations, built with **Streamlit**, **LangChain** and **Google Gemini**. It includes a web chatbot with spoken replies, a voice-driven customer-care agent with LangSmith tracing, a voice "therapist" with selectable personalities, and a symptom-to-advice chain.

## 🔗 Live demo

Not hosted yet. The web chatbot (`chatbot.py`) can be deployed for free on Streamlit Community Cloud: click the badge (or go to https://share.streamlit.io → **Create app**) and use repository `amitmohanty022/AI-Powered-Call-Centre-Intelligence`, branch `main`, main file `chatbot.py`.

[![Deploy on Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/deploy?repository=amitmohanty022/AI-Powered-Call-Centre-Intelligence&branch=main&mainModule=chatbot.py)

Users type their own Gemini API key into the app, so no secrets are required. The voice apps (`talking_customer_care_langsmith.py`, `Brutal_Therapist.py`) use your computer's microphone and speakers, so run those locally.

## What's inside

| File | Type | What it does |
| --- | --- | --- |
| `chatbot.py` | Streamlit web app | Friendly, slightly witty chatbot with conversation memory; replies are read aloud with gTTS |
| `talking_customer_care_langsmith.py` | Streamlit app (local) | Customer-support agent: describe the product problem, then chat by typing or by voice; answers are spoken with pyttsx3 and traced in LangSmith |
| `Brutal_Therapist.py` | Voice CLI (local) | Pick a therapist personality (brutal, polite, arrogant) by voice and talk to it; collects feedback at the end |
| `app.py` | CLI | Two-step LangChain (LCEL) chain: explains symptoms, then gives do's and don'ts |
| `app3.py` | CLI | Health-report generator prototype |

## Tech stack

Python, Streamlit, LangChain (`langchain-core`, `langchain-google-genai`), Google Gemini 3.8 Flash, LangSmith, gTTS, pyttsx3, SpeechRecognition

## Run locally

```bash
git clone https://github.com/amitmohanty022/AI-Powered-Call-Centre-Intelligence.git
cd AI-Powered-Call-Centre-Intelligence
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Create a `.env` file:

```env
GOOGLE_API_KEY=your_gemini_api_key        # https://aistudio.google.com/apikey
GEMINI_MODEL=gemini-3.8-flash             # optional, this is the default
LANGSMITH_API_KEY=your_langsmith_api_key  # optional, enables tracing in the customer-care app
```

Run an app:

```bash
streamlit run chatbot.py                              # web chatbot
streamlit run talking_customer_care_langsmith.py      # voice customer-care agent
python Brutal_Therapist.py                            # voice therapist
python app.py                                         # symptom chain (CLI)
```

Voice input needs a microphone and PyAudio (`pip install pyaudio`; on Linux install `portaudio19-dev` first).

## License

MIT. See [LICENSE](LICENSE).

## Contact

**Amit Kumar Mohanty** · [GitHub @amitmohanty022](https://github.com/amitmohanty022) · mohantyamit2003@gmail.com
