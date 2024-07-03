from flask import request
from datetime import datetime
import os

def save_error(content):
    file_path = os.path.join("app", "src", "logs", "error.log")

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    user_ip = request.remote_addr

    with open(file_path, "a", encoding="utf-8") as file:
        file.write(f"{current_time} - {user_ip} : '{content}'\n")


def save_http_request():
    file_path = os.path.join("app", "src", "logs", "http_requests.log")

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    user_ip = request.remote_addr

    with open(file_path, "a", encoding="utf-8") as file:
        file.write(f"{current_time} - {user_ip} : '{request.method}' - {request.url} \n")