

from litellm import completion
import os
#from dotenv import load_dotenv
#load_dotenv()  # Load environment variables from .env file

#os.environ["GEMINI_API_KEY"] = os.getenv("GEMINI_API_KEY")

import os
os.environ["GEMINI_API_KEY"] = "your secret"


MODELS = [
    "gemini/gemini-3.5-flash"
]

def update_history(user_message):
    with open("chat_history.txt", "a", encoding="utf-8") as f:
        f.write(f"user:{user_message}\n")

def ask_llm(messages, system_prompt,user_message):
    update_history(user_message)  # Save the latest prompt and messages to history
    full_messages = [
        {"role": "user", "content": system_prompt+user_message},
        *messages  # full chat history including latest user message
    ]
    for model in MODELS:
        try:
            return completion(
                model=model,
                messages=full_messages
            ).choices[0].message.content
        except Exception as e:
            print(f"{model} failed: {e}")
    raise RuntimeError("All models failed")
