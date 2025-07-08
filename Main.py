# main.py
import os
import time
import datetime
from App_Directory.LLM.Gemini import init_chat, greet_user, handle_user_message
from App_Directory.Python.Functions import log_message

# Абсолютный путь к директории Bank_AI_Caller
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Путь к папке Logs внутри App_Directory
log_dir = os.path.join(project_root, "App_Directory", "Logs")
os.makedirs(log_dir, exist_ok=True)

# Время начала разговора
start_time = datetime.datetime.now()

# Имя и путь лог-файла
log_file_name = f"chat_log_{start_time.strftime('%Y-%m-%d_%H-%M-%S')}.txt"
log_file = os.path.join(log_dir, log_file_name)

# Запись времени начала в лог
with open(log_file, "a", encoding="utf-8") as f:
    f.write(f"[INFO] Начало разговора: {start_time.strftime('%Y-%m-%d %H:%M:%S')}\n")

def main():
    # Старт
    chat = init_chat()

    # Приветствие
    try:
        bot_reply = greet_user(chat)
        print("Бот:", bot_reply)
        log_message("Бот", bot_reply, log_file)
    except Exception as e:
        print("⚠️ Ошибка при приветствии:", e)

    # Основной цикл
    while True:
        user_input = input("Ты: ")
        log_message("Ты", user_input, log_file)

        cleaned_reply, log_type, log_value = handle_user_message(chat, user_input)
        print("Бот:", cleaned_reply)
        log_message("Бот", cleaned_reply, log_file)

        if log_type:
            if log_type == "fail":
                print("📋 Результат: клиент отказался")
            elif log_type == "success":
                print("📋 Результат: клиент заинтересован")
            elif log_type == "callback":
                print(f"📋 Результат: клиент просит перезвонить в {log_value}")

            with open(log_file, "a", encoding="utf-8") as f:
                f.write(f"[RESULT] {log_type.upper()}: {log_value if log_value else ''}\n")

            print("Система: Разговор завершён")
            end_time = datetime.datetime.now()
            duration = end_time - start_time
            duration_str = str(duration).split(".")[0]  # Удаляем микросекунды

            with open(log_file, "a", encoding="utf-8") as f:
                f.write(f"[INFO] Конец разговора: {end_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"[INFO] Длительность разговора: {duration_str}\n")
            break

        if cleaned_reply.startswith("⚠️ Ошибка"):
            time.sleep(60)

if __name__ == "__main__":
    main()