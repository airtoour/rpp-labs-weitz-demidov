import requests
import time

url = 'http://127.0.0.1:5000/login'


users_list = [
    {"email": "artur_3@bk.ru",       "password": "1234568"},
    {"email": "artur_4@bk.ru",       "password": "1234569"},
    {"email": "artur_5@bk.ru",       "password": "1234565"},
    {"email": "artur_6@bk.ru",       "password": "1234564"},
    {"email": "artur_7@bk.ru",       "password": "1234563"},
    {"email": "artur_8@bk.ru",       "password": "1234562"},
    {"email": "artur_9@bk.ru",       "password": "1234561"},
    {"email": "artur_10@bk.ru",      "password": "1234566"},
    {"email": "artur_11@bk.ru",      "password": "12345612"},
    {"email": "artur_12@bk.ru",      "password": "12345613"},
    {"email": "artur_13@bk.ru",      "password": "12345614"},
    {"email": "artur_7@bk.ru",       "password": "1234563"},
    {"email": "artur_8@bk.ru",       "password": "1234562"},
    {"email": "artur_9@bk.ru",       "password": "1234561"},
    {"email": "artur_10@bk.ru",      "password": "1234566"},
    {"email": "artur_11@bk.ru",      "password": "12345612"},
    {"email": "artur_12@bk.ru",      "password": "12345613"},
    {"email": "artur_13@bk.ru",      "password": "12345614"},
    {"email": "artur_7@bk.ru",       "password": "1234563"},
    {"email": "artur_8@bk.ru",       "password": "1234562"},
    {"email": "artur_9@bk.ru",       "password": "1234561"},
    {"email": "artur_10@bk.ru",      "password": "1234566"},
    {"email": "artur_11@bk.ru",      "password": "12345612"},
    {"email": "artur_12@bk.ru",      "password": "12345613"},
    {"email": "artur_13@bk.ru",      "password": "12345614"},
    {"email": "shiva123121@mail.ru", "password": "123456"}
]

for user in users_list:
    payload = {
        'email':    user['email'],
        'password': user['password']}
    response = requests.post(url, data=payload)

    if response.status_code == 429:
        print(f'Слишком много запросов. Пауза на 1 минуту...,  {response.status_code}')
        time.sleep(60)
    elif response.status_code == 200:
        print(f'Логин: {user["email"]}, Пароль: {user["password"]}, {response.status_code}')
        break
    else:
        print(f'Неверно введены данные, {response.status_code}')
        continue
