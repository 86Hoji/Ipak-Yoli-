# core/bot.py
import datetime
import google.generativeai as genai
from App_Directory.Python.Functions import parse_log_and_clean
from App_Directory.Prompts.Instruction import system_prompt

# Настройка API
genai.configure(api_key="AIzaSyB7fdZkYKLuX8EnfzEgQMSUcHU1TzyAOmw")

generation_config = {
    "temperature": 0.4,
    "top_p": 0.9,
    "top_k": 20,
    "max_output_tokens": 1024,
}

def init_chat():
    model = genai.GenerativeModel(
        "gemini-1.5-flash",
        generation_config=generation_config
    )

    now = datetime.datetime.now()
    current_time = now.strftime("%Y-%m-%d %H:%M")

    chat = model.start_chat(history=[{
        "role": "user",
        "parts": [system_prompt.format(current_time=current_time)]
    }])
    return chat

def greet_user(chat):
    try:
        response = chat.send_message("Поздоровайся как голосовой помощник банка")
        return response.text.strip()
    except Exception as e:
        return f"⚠️ Ошибка при приветствии: {e}"

def handle_user_message(chat, user_input):
    try:
        response = chat.send_message(user_input)
        bot_reply_raw = response.text.strip()
        return parse_log_and_clean(bot_reply_raw)
    except Exception as e:
        return f"⚠️ Ошибка: {e}", None, None
