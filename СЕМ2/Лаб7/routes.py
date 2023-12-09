from flask import Blueprint, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from db_data import users_credentials
import requests
import time

login = Blueprint('login', __name__)
limiter = Limiter(login, key_func=get_remote_address)

def make_login_request(username, password):
    login_url = "http://your-api-url/login"  # Замените "your-api-url" на фактический URL вашего API
    data = {'email': username, 'password': password}
    response = requests.post(login_url, data=data)
    return response

@limiter.request_filter
def ip_whitelist():
    return False  # Отключение ограничения по IP, чтобы использовать ограничение запросов на уровне эндпоинта

@login.route('/login', methods=['POST'])
@limiter.limit("10 per minute")  # Ограничение 10 запросов в минуту
def login_route():
    username = request.form.get('email')
    password = request.form.get('password')

    for _ in range(3):  # Попробовать три раза перед приостановкой
        response = make_login_request(username, password)

        if response.status_code == 429:  # Too Many Requests
            time.sleep(60)
        elif response.status_code == 200:  # OK
            return f"Successful login. Username: {username}, Password: {password}", 200
        else:
            return f"Login failed for Username: {username}, Password: {password}", 401

    return "Login failed after multiple attempts", 401
