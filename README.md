# 🤖 TalentScout Hiring Assistant

An AI-powered chatbot for automated technical candidate screening, built with Streamlit and Groq LLM.

---

## 📌 Project Overview

TalentScout Hiring Assistant is a conversational AI chatbot designed to streamline the initial stages of technical recruitment. It collects candidate information through a guided conversation flow and automatically generates relevant technical interview questions based on the candidate's declared tech stack.

**Key Capabilities:**
- Guides candidates through a structured information-gathering process (name, email, phone, experience, position, location, tech stack)
- Validates inputs in real-time (e.g., email format validation)
- Generates 5 targeted technical questions per technology using a Groq-powered LLM (LLaMA 3.1)
- Persists candidate data locally in a JSON file for recruiter review
- Supports graceful session termination via exit keywords

---

## ⚙️ Installation Instructions

### Prerequisites
- Python 3.8 or higher
- A valid [Groq API key](https://console.groq.com/)

### Step-by-Step Setup

**1. Clone the repository**
```bash
git clone https://github.com/your-username/talentscout.git
cd talentscout
```

**2. Create a virtual environment**
```bash
# Mac/Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Create a `.env` file in the project root**
```
GROK_API_KEY=your_groq_api_key_here
```

**5. Run the application**
```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

---

## 🚀 Usage Guide

1. Launch the app using `streamlit run app.py`
2. The chatbot will greet you and begin collecting your details step by step:
   - Full Name
   - Email Address (validated for correct format)
   - Phone Number
   - Years of Experience
   - Desired Position
   - Current Location
   - Tech Stack (comma-separated, e.g., `Python, React, PostgreSQL`)
3. Once your tech stack is submitted, the LLM generates 5 technical questions per technology
4. Review the questions and type any of the exit keywords to end the session: `exit`, `quit`, `bye`, `goodbye`, or `end`

> **Note:** Your information is automatically saved to `candidates.json` after the tech stack step.

---

## 🛠️ Technical Details

### Libraries Used

| Library | Purpose |
|---|---|
| `streamlit` | Frontend chat UI |
| `groq` | API client for Groq LLM |
| `python-dotenv` | Loading environment variables from `.env` |
| `re` (built-in) | Email validation via regex |
| `json`, `os` (built-in) | Candidate data persistence |

### Model Details

- **Model:** `llama-3.1-8b-instant` via Groq API
- **Temperature:** `0.3` (low, for consistent and focused question generation)
- **Why Groq + LLaMA?** Groq offers extremely fast inference speeds, making the chatbot feel responsive. LLaMA 3.1 8B provides strong instruction-following capability at a lightweight size, ideal for structured prompts.

### Architecture Overview

```
app.py                  → Streamlit UI + session state management
conversation_manager.py → Stage-based conversation flow controller
llm_engine.py           → Groq API wrapper (call_llm)
prompts.py              → Prompt templates for question generation
data_store.py           → JSON-based candidate persistence
utils.py                → Email validation helper
config.py               → Environment variable loading + exit keywords
```

The application follows a **linear finite-state machine** pattern. The `ConversationManager` holds a `stage` variable that progresses through: `greeting → name → email → phone → experience → position → location → tech_stack → end`. Each stage processes the user's input and transitions to the next.

---

## 🧠 Prompt Design

### Information Gathering
The information gathering phase is handled entirely by the state machine in `conversation_manager.py` — no LLM is used here. This ensures deterministic, reliable data collection without hallucinations or off-topic responses.

### Technical Question Generation
When the candidate provides their tech stack, the following prompt strategy is applied in `prompts.py`:

**Key Design Decisions:**
- The system prompt establishes strict persona: *"You are a strict senior technical interviewer"* — this anchors the model to professional, relevant output.
- The user prompt explicitly lists the candidate's declared technologies and enforces hard rules:
  - Generate questions **only** for mentioned technologies (prevents the model from adding unrequested topics)
  - Exactly **5 questions per technology** (ensures consistency)
  - **No answers** provided (keeps it as a screening tool)
  - Clear **heading format** per technology for readability
- A low temperature of `0.3` is used to minimize creative drift and keep questions practical and on-topic.

**Example Prompt Structure:**
```
You are a strict technical interviewer.

Candidate Tech Stack: Python, Django

IMPORTANT RULES:
- Generate questions ONLY for the technologies explicitly mentioned above.
- Generate exactly 5 questions per technology.
- Do NOT provide answers.
- Clearly mention the technology name as a heading.
```

---

## 🧩 Challenges & Solutions

### Challenge 1: Email Validation Without Blocking Conversation Flow
**Problem:** If an invalid email was entered, the conversation needed to re-prompt without losing state or breaking the flow.

**Solution:** The `email` stage returns an error message and stays on the same stage (does not advance `self.stage`) until a valid email matching the regex pattern `^[\w\.-]+@[\w\.-]+\.\w+$` is provided. This creates a natural retry loop without resetting the entire session.

---

### Challenge 2: LLM Generating Questions for Unmentioned Technologies
**Problem:** LLMs tend to add related technologies (e.g., if user says "Python", the model might also generate NumPy or Django questions unprompted).

**Solution:** The prompt was made stricter with explicit capitalized rules like `"DO NOT add any extra technologies"` and `"If only one technology is mentioned, generate questions only for that."` Combined with a low temperature (0.3), this significantly reduced unwanted additions.

---

### Challenge 3: Streamlit Session State Management
**Problem:** Streamlit reruns the entire script on every interaction, which could reset the `ConversationManager` and lose conversation history.

**Solution:** The `ConversationManager` instance and message history are stored in `st.session_state`, which persists across reruns. The greeting is initialized only once using an `if "chat_manager" not in st.session_state` guard.

---

### Challenge 4: Graceful Session Termination
**Problem:** Users needed a natural way to end the session without the chatbot continuing to prompt them.

**Solution:** Exit keywords (`exit`, `quit`, `bye`, `goodbye`, `end`) are checked in `app.py` before any processing. If detected, a farewell message is shown and `st.stop()` halts further execution cleanly.

---

## 📁 Project Structure

```
talentscout/
├── app.py                  # Main Streamlit application
├── conversation_manager.py # Conversation state machine
├── llm_engine.py           # Groq LLM API interface
├── prompts.py              # Prompt templates
├── data_store.py           # Candidate data storage (JSON)
├── utils.py                # Utility functions
├── config.py               # Configuration and environment variables
├── candidates.json         # Stored candidate records (auto-generated)
├── requirements.txt        # Python dependencies
└── .env                    # API keys (not committed to git)
```

---

## 🔒 Security Notes

- Never commit your `.env` file to version control
- Add `.env` and `venv/` to your `.gitignore`
- The `candidates.json` file contains PII — handle it according to your data privacy policies

---

## 📄 License

This project is for educational and internal recruitment use.
