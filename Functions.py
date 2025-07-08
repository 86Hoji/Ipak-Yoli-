# core/utils.py
import datetime
import re

def log_message(sender, message, log_file):
    timestamp = datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"{timestamp} {sender}: {message}\n")
        f.flush()

def parse_log_and_clean(message):
    match = re.search(r"\[LOG:\s*(.*?)\]", message)
    if not match:
        return message, None, None

    log_content = match.group(1).strip().lower()
    cleaned_message = re.sub(r"\[LOG:\s*.*?\]", "", message).strip()

    if log_content == "fail":
        return cleaned_message, "fail", None
    elif log_content == "success":
        return cleaned_message, "success", None
    elif log_content.startswith("callback@"):
        callback_time = log_content.split("callback@")[1]
        return cleaned_message, "callback", callback_time

    return cleaned_message, None, None
