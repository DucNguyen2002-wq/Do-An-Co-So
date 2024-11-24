import json
import os
import google.generativeai as genai
from queue import Queue

genai.configure(api_key="AIzaSyBqIgwm7sSweenTFLwfEkqGnQ1T8P7JUsQ")

# Create the model
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro-002",
    generation_config=generation_config,
    system_instruction=(
        "You're named Fairy, a male AI assistant who is knowledgeable and loves chatting with people. "
        "You have a knack for breaking down complex topics into simple terms, often adding a bit of humor. "
        "You're always looking to keep the conversation flowing, whether it's with a friendly greeting or an intriguing question. "
        "You're efficient and direct in your responses, ensuring interactions are both informative and enjoyable."
    ),
)

def save_history(history, filename="chat_history.json"):
    """Save chat history to a file."""
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=4)


def load_history(filename="chat_history.json"):
    """Load chat history from a file."""
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        return []

# Initialize history
if os.path.exists("chat_history.json"):
    history = load_history()
else:
    history = []

# Function to process a user message
def process_message(user_input, response_queue):
    """Process user input and generate a response."""
    try:
        if not user_input.strip():
            response_queue.put("Fairy: Bạn có thể nói gì đó không?")
            return

        chat_session = model.start_chat(history=history)
        response = chat_session.send_message(user_input)
        model_response = response.text

        history.append({"role": "user", "parts": [user_input]})
        history.append({"role": "model", "parts": [model_response]})
        save_history(history)

        response_queue.put(f"Fairy: {model_response}")
    except Exception as e:
        response_queue.put(f"Có lỗi xảy ra: {str(e)}")
