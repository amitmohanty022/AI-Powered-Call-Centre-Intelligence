# AI-Powered Call Centre Intelligence

A set of AI chatbots built with **Streamlit**, **LangChain** and **Google Gemini**, including voice assistants (speech-to-text and text-to-speech) and LangSmith tracing.

| File | What it is | How you use it |
|---|---|---|
| `talking_customer_care_langsmith.py` | Customer care bot with voice input/output and optional LangSmith tracing | Web app |
| `chatbot.py` | Witty chatbot that remembers the conversation and speaks its replies | Web app |
| `Brutal_Therapist.py` | Voice-only therapist bot with 3 personalities: brutal, polite, arrogant | Terminal + microphone |
| `Memory.py` | English teacher bot that shows LangChain conversation memory | Terminal |
| `app.py` | "Dr. Amit": symptoms in, causes/do's/don'ts out, then a rating | Terminal |
| `app3.py` | Health report generator (summary, do's, don'ts) | Terminal |

## How to run (step by step)

You need **Python 3.10 or newer** ([download](https://www.python.org/downloads/)).

**1. Download the project**

```bash
git clone https://github.com/amitmohanty022/AI-Powered-Call-Centre-Intelligence.git
cd AI-Powered-Call-Centre-Intelligence
```

**2. Create a virtual environment and activate it**

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate
```

**3. Install the requirements**

```bash
pip install -r requirements.txt
```

> **If `PyAudio` fails to install** (needed for the microphone only):
> - macOS: `brew install portaudio`, then run the command again
> - Ubuntu/Debian: `sudo apt install portaudio19-dev espeak`, then run the command again
> - Windows: it normally installs without extra steps
>
> The text-only scripts (`chatbot.py`, `Memory.py`, `app.py`, `app3.py`) work even if PyAudio fails.

**4. Add your Gemini API key**

- Get a free key at https://aistudio.google.com/apikey
- Copy `.env.example` to a new file named `.env`
  - Windows: `copy .env.example .env`
  - macOS / Linux: `cp .env.example .env`
- Open `.env` and paste your key after `GOOGLE_API_KEY=`
- Optional: add a LangSmith key after `LANGCHAIN_API_KEY=` to see traces at https://smith.langchain.com

**5. Run the app you want**

Web apps (your browser opens at http://localhost:8501):

```bash
streamlit run talking_customer_care_langsmith.py
streamlit run chatbot.py
```

Terminal apps:

```bash
python app.py
python app3.py
python Memory.py            # type "exit" to quit
python Brutal_Therapist.py  # say "brutal", "polite" or "arrogant", then talk; say "exit" to finish
```

## Settings

| Variable in `.env` | Default | What it does |
|---|---|---|
| `GOOGLE_API_KEY` | (empty, required) | Gemini key |
| `GEMINI_MODEL` | `gemini-3.8-flash` | Gemini model used by every script |
| `LANGCHAIN_API_KEY` | (empty, optional) | Turns on LangSmith tracing for the customer care bot |

## Architecture

- **LLM**: Google Gemini through `langchain-google-genai`.
- **Memory**: conversation history kept in Streamlit session state, or LangChain memory classes in the terminal scripts.
- **Voice**: `SpeechRecognition` (speech-to-text), `pyttsx3` (offline text-to-speech), `gTTS` (online text-to-speech in `chatbot.py`).

## Troubleshooting

| Problem | Fix |
|---|---|
| "GOOGLE_API_KEY is not set" | Make sure the file is named exactly `.env` (not `.env.txt`) and is in the project folder. |
| `streamlit: command not found` | Activate the virtual environment (step 2) first. |
| No microphone / `PyAudio` error | See the note under step 3, or use the text-only scripts. |
| `404 model not found` | Set `GEMINI_MODEL=gemini-3.6-flash` in `.env`. |
| LangChain deprecation warnings | They are only warnings. The scripts still work. |

## License
MIT. See [LICENSE](LICENSE).

## Contact
- *Amit Kumar Mohanty*
- *GitHub: @amitmohanty022*
- *Email: mohantyamit2003@gmail.com*
