import requests

# Задание 1
# Запрос добавления информации о регионе /v1/add/region
url  = 'http://localhost:5000/v1/add/tax'
data = {'region_code': '1',
        'tax_rate':     0.5}

response = requests.post(url, json = data)
if response.status_code == 200:
    json_data = response.json()
    print(json_data)
else:
    print('Error: ', response.status_code, response.content.decode('utf-8'))
    print(response.json())

# Задание 2
# Запрос обновление объекта налогооблажения POST /v1/update/tax
url  = 'http://localhost:5000/v1/update/tax'
data = {'region_code':   '1',
        'tax_rate':      0.76}

response = requests.post(url, json = data)
if response.status_code == 200:
    json_data = response.json()
    print(json_data)
else:
    print('Error: ', response.status_code, response.content.decode('utf-8'))
    print(response.json())

#Задание 3
#Запрос добавления автомобиля POST /v1/add/auto
url = 'http://127.0.0.1:5000/v1/add/auto'
data = {'id':              1,
        'city_id':         54,
        'tax_id':          2,
        'name':           'Mercedes',
        'horse_power':     220,
        'production_year': 1992}

response = requests.post(url, json = data)
if response.status_code == 200:
    json_data = response.json()
    print(json_data)
else:
    print('Error: ', response.status_code, response.content.decode('utf-8'))
    print(response.json())

# Создать запрос получения информации по всем автомобилям GET /v1/auto
url = 'http://127.0.0.1:5000/v1/auto/1'
response = requests.get(url)
if response.status_code == 200:
    json_data = response.json()
    print(json_data)
else:
    print('Error:', response.status_code, response.content.decode('utf-8'))
    print(response.json())
