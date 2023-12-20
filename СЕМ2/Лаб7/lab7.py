# ЭТОТ ФАЙЛ ЗАПУСКАТЬ ТОЛЬКО ПОСЛЕ ТОГО, КАК ЗАПУСТИЛИ main

import requests
import time

url = 'http://127.0.0.1:5000/zadaniye'

users_list = [
    {"email": "gleb_roma_3@bk.ru",  "password": "1234568"},
    {"email": "gleb_roma_4@bk.ru",  "password": "1234569"},
    {"email": "gleb_roma_5@bk.ru",  "password": "1234565"},
    {"email": "gleb_roma_6@bk.ru",  "password": "1234564"},
    {"email": "gleb_roma_7@bk.ru",  "password": "1234563"},
    {"email": "gleb_roma_8@bk.ru",  "password": "1234562"},
    {"email": "gleb_roma_9@bk.ru",  "password": "1234561"},
    {"email": "gleb_roma_10@bk.ru", "password": "1234566"},
    {"email": "gleb_roma_11@bk.ru", "password": "12345612"},
    {"email": "gleb_roma_12@bk.ru", "password": "12345613"},
    {"email": "gleb_roma_13@bk.ru", "password": "12345614"},
    {"email": "gleb_roma_7@bk.ru",  "password": "1234563"},
    {"email": "gleb_roma_8@bk.ru",  "password": "1234562"},
    {"email": "gleb_roma_9@bk.ru",  "password": "1234561"},
    {"email": "gleb_roma_10@bk.ru", "password": "1234566"},
    {"email": "gleb_roma_11@bk.ru", "password": "12345612"},
    {"email": "gleb_roma_12@bk.ru", "password": "12345613"},
    {"email": "gleb_roma_13@bk.ru", "password": "12345614"},
    {"email": "gleb_roma_7@bk.ru",  "password": "1234563"},
    {"email": "gleb_roma_8@bk.ru",  "password": "1234562"},
    {"email": "gleb_roma_9@bk.ru",  "password": "1234561"},
    {"email": "gleb_roma_10@bk.ru", "password": "1234566"},
    {"email": "gleb_roma_11@bk.ru", "password": "12345612"},
    {"email": "gleb_roma_12@bk.ru", "password": "12345613"},
    {"email": "gleb_roma_13@bk.ru", "password": "12345614"}
]

for user in users_list:
    payload = {
        'email':    user['email'],
        'password': user['password']
    }
    # В ответ (response) записываем данные которые мы взяли из списка выше
    response = requests.post(url, data=payload)

    if response.status_code == 429: # Если код ответа 429, значит блокируем маршрут. Он означает Слишком много запросов (Too Many Requests)
        print(f'Слишком много запросов. Пауза на час...,  {response.status_code}')
        time.sleep(86400)
    elif response.status_code == 200:
        print(f'Логин: {user["email"]}, Пароль: {user["password"]}, {response.status_code}')
        break
    else:
        print(f'Неверно введены данные, {response.status_code}')
        continue