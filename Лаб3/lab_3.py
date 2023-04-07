# Пункт 1
import http.client
import json

# Создаем переменную, которой присваиваем подключение к данному ip
conn = http.client.HTTPConnection("167.172.172.227:8000")
# Отправляем GET-запрос с конечным значением /number/1
conn.request('GET', '/number/1')
# Получение ответа от сервера, чтение и декодирование в строку.
op = conn.getresponse().read().decode()
# Преобразование строки JSON в объект Python.
op_json = json.loads(op)
# Извлечение значения поля number из полученного объекта и присвоение его переменной op1_json
op_json = op_json['number']
# Вывод на экран значения поля 'number' полученного объекта.
print("Ответ на п.1: ", op_json)

# Пункт 2
conn.request('GET', '/number/?option=1')
op1 = conn.getresponse().read().decode()
op1_json = json.loads(op1)
op1_json = op1_json['number']

# Вывод на экран значения.
print("Ответ на п.2: ", op1, ",", op_json, ",", op1_json, ",", round(op_json * op1_json, 2))

# Пункт 3
# Создание переменной head, которой присваем значение заголовок "Content-Type" и тип содержимого 'application/x-www-form-urlencoded'
head = {'Content-Type': 'application/x-www-form-urlencoded'}
# Отправляем GET-запрос с конечным значением /number/1 и словарь headers
conn.request("POST", "/number/", "option=1", headers=head)
op = conn.getresponse().read().decode()
op2_json = json.loads(op)
op2_json = op2_json['number']
print("Ответ на п.3: ", op, ",", op2_json, ",", round(op1_json / op2_json, 2))
conn.close()

# Пункт 4
# Создается переменная head, в которой присваивается значение заголовка "Content-Type" и тип содержимого 'application/json'
head = {'Content-Type': 'application/json'}
body = {"option": 1}
conn.request("PUT", "/number/", body=json.dumps(body), headers=head)
op = conn.getresponse().read().decode()
op2_json = json.loads(op)
op2_json = op2_json["number"]
print("Ответ на п.4: ", op, ",", op2_json, ",", op1_json - op2_json)
conn.close()

# Пункт 5
body = {"option": 1}
conn.request("DELETE", "/number/", body=json.dumps(body))
op = conn.getresponse().read().decode()
op3_json = json.loads(op)
op3_json = op3_json["number"]
print("Ответ на п.5: ", op, ",", op3_json, ",", op2_json * op3_json)
conn.close()
