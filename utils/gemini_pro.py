from langchain_google_genai import ChatGoogleGenerativeAI
import google.generativeai as genai
import os

generation_config = {
    "temperature": 0,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
}

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
]

genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))


def load_gemini_pro_model():
    chat_model = ChatGoogleGenerativeAI(
        model="gemini-pro",
        generation_config=generation_config,
        convert_system_message_to_human=True,
        safety_settings=safety_settings
    )
    return chat_model
