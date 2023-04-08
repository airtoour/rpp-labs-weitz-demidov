import http.client
import json


# Определяем функцию operate, которая принимает два аргумента: строку в формате JSON data и целое число left
def operate(data: str, left: int):
    # Преобразуем данные в формате JSON из строки data в словарь Python с помощью функции json.loads()
    dict = json.loads(data)

    # Если операция равна 'mul' (умножение), то умножаем left на число из словаря и возвращаем результат
    if dict['operation'] == 'mul':
        return left * dict['number']

    # Если операция равна 'sub' (вычитание), то вычитаем число из словаря из left и возвращаем результат
    if dict['operation'] == 'sub':
        return left - dict['number']

    # Если операция равна 'div' (деление), то делим left на число из словаря и возвращаем результат
    if dict['operation'] == 'div':
        return left / dict['number']

    # Если операция равна 'sum' (сложение), то складываем left с числом из словаря и возвращаем результат
    if dict['operation'] == 'sum':
        return left + dict['number']


# Пункт 1:
conn = http.client.HTTPConnection("167.172.172.227:8000")
conn.request("GET", "/number/1")

# Получаем ответ от сервера и сохраняем его в переменной op
op1 = conn.getresponse()

# Выводим на экран статус ответа и его причину
print("           ", op1.status, op1.reason)

# Декодируем тело ответа из байтовой строки в строку типа str
decode_body = op1.read().decode()

# Преобразуем строку JSON в объект Python типа dict и извлекаем значение поля number
obj1 = json.loads(decode_body)['number']

conn.close()

# Выводим на экран значение переменной obj1
print("Вывод П.1: ", obj1)

# Пункт 2
connect = http.client.HTTPConnection("167.172.172.227:8000")
connect.request('GET', '/number/?option=1')

# Получение ответа от сервера
op2 = connect.getresponse()

# Вывод статуса ответа (код состояния HTTP) и причины (строковое описание кода состояния)
print("           ", op2.status, op2.reason)

# Декодирование тела ответа сервера в строку
decode_body2 = op2.read().decode()

# Вызов функции operate с параметрами decode_body2 и obj1, сохранение результата в переменной obj2
obj2 = operate(decode_body2, obj1)

conn.close()

# Вывод значения переменной left
print("Вывод П.2: ", obj2)

# Пункт 3
connect = http.client.HTTPConnection("167.172.172.227:8000")
headers = {'Content-type': 'application/x-www-form-urlencoded'}
connect.request('POST', '/number/', 'option=1', headers)

# Получение ответа от сервера
op3 = connect.getresponse()

# Вывод статус-кода и причины ответа сервера
print("           ", op3.status, op3.reason)

# Декодирование тела ответа сервера в строку
decode_body3 = op3.read().decode()

# Вызов функции operate с параметрами decode_body3 и obj2, сохранение результата в переменной obj3
obj3 = operate(decode_body3, obj2)

conn.close()

# Вывод значения переменной left
print("Вывод П.3: ", obj3)

# Пункт 4
connect = http.client.HTTPConnection("167.172.172.227:8000")
headers = {'Content-type': 'application/json'}
connect.request('PUT', '/number/', json.dumps({'option': 1}), headers)

# Получение ответа от сервера
op4 = connect.getresponse()

# Вывод статус-кода и причины ответа сервера
print("           ", op4.status, op4.reason)

# Декодирование тела ответа сервера в строку и передача этой строки в функцию "operate" вместе с переменной "obj3"
decode_body4 = op4.read().decode()

# Вызов функции operate с параметрами decode_body4 и obj3, сохранение результата в переменной obj4
obj4 = operate(decode_body4, obj3)

conn.close()

# Вывод результата работы функции operate()
print("Вывод П.4: ", round(obj4, 2))


# Пункт 5
connect = http.client.HTTPConnection("167.172.172.227:8000")
connect.request('DELETE', '/number/', json.dumps({'option': 1}))

# Получение ответа от сервера
op5 = connect.getresponse()

# Вывод статус-кода и причины ответа сервера
print("           ", op5.status, op5.reason)

# Декодирование тела ответа сервера в строку и передача этой строки в функцию "operate" вместе с переменной "obj4"
decoded_body5 = op5.read().decode()

# Вызов функции operate с параметрами decode_body5 и obj4, сохранение результата в переменной obj5
obj5 = operate(decoded_body5, obj4)

conn.close()

# Вывод результата работы функции operate()
print("Вывод П.5: ", round(obj5, 2))
