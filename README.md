# 🤖 Customized AI Agent — INING Session Demo

A Streamlit app demonstrating a customizable AI agent built on the Gemini API (free).

## Features

- **Chat Agent** — conversational AI with session memory
- **Prompt Builder** — edit the system prompt live, see behaviour change instantly
- 4 built-in example personas to load and demo
- Chat history saved to file across sessions

## Quick Start

```bash
# 1. Clone / download this folder
# 2. Install dependencies
pip install -r requirements.txt

# 3. Set your API key in ai_client.py
# Get your FREE key at: https://aistudio.google.com/apikey
os.environ["GEMINI_API_KEY"] = "paste-your-key-here"

# 4. Run
streamlit run app.py
```

## The Key Idea

The entire agent personality lives in one variable:

```python
completion(
    model="gemini/gemini-1.5-flash",
    messages=[
        {"role": "system",    "content": system_prompt},  # ← change this = different agent
        *history,                                          # ← past conversation memory
        {"role": "user",      "content": user_message},   # ← latest input
    ]
)
```

## Structure

```
chatagent-default/
├── app.py                # Main Streamlit app
├── ai_client.py          # LiteLLM + Gemini API wrapper
├── default_prompt.txt    # Active system prompt (editable from UI)
├── sample_prompt.txt     # Original default prompt (used by Reset button)
├── chat_history.txt      # Conversation history (auto-created)
├── requirements.txt      # Dependencies
└── README.md
```

## Demo Script

1. Open the app → **Chat Agent** page
2. Type: *"Summarize what an AI agent is in 2 sentences"*
3. Note the response tone (default: Data Engineer persona)
4. Switch to **Prompt Builder** → load "Sarcastic Genius"
5. Hit **Update Agent** → go back to Chat Agent
6. Ask the same question → completely different agent!
