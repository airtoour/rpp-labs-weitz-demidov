import requests
# Запрос добавления информации о регионе /v1/add/region
url = 'http://localhost:5433/v1/add/region'
data = {'id': 54, 'region': 'Новосибирск'}
response = requests.post(url, json = data)
if response.status_code == 200:
    json_data = response.json()
    print(json_data)
else:
    print('Error:', response.status_code, response.content.decode('utf-8'))
    print(response.json())

# Запрос добавления объекта налогооблажения POST /v1/add/taxparam
url  = 'http://localhost:5433/v1/add/tax-param'
data = {'id':                       123,
        'city_code':                54,
        'from_hp_car':              180,
        'to_hp_car':                200,
        'from_production_year_car': 1990,
        'to_production_year_car':   1995,
        'rate':                     0.5}

response = requests.post(url, json = data)
if response.status_code == 200:
    json_data = response.json()
    print(json_data)
else:
    print('Error:', response.status_code, response.content.decode('utf-8'))
    print(response.json())

# Запрос добавления автомобиля POST /v1/add/auto
url = 'http://127.0.0.1:5433/v1/add/auto'
data = {'id':              5,
        'city_code':       54,
        'tax_id':          123,
        'name':           'BMW',
        'horse_power':     130,
        'production_year': 1988}

response = requests.post(url, json = data)
if response.status_code == 200:
    json_data = response.json()
    print(json_data)
else:
    print('Error:', response.status_code, response.content.decode('utf-8'))

# Создать запрос получения информации по всем автомобилям GET /v1/auto
9
url = 'http://127.0.0.1:5433/v1/auto'
data = {'id': 5}
response = requests.get(url, json = data)
if response.status_code == 200:
    json_data = response.json()
    print(json_data)
else:
    print('Error:', response.status_code, response.content.decode('utf-8'))
