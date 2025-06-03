import requests

def get_location_from_ipapi(ip_address):
    try:
        response = requests.get(f"http://ip-api.com/json/{ip_address}?lang=ru")
        data = response.json()
        if data and data['status'] == 'success':
            city = data.get('city')
            country = data.get('country')
            return city, country
        else:
            print(f"Ошибка IP-API: {data.get('message', 'Неизвестная ошибка')}")
            return None, None
    except requests.exceptions.RequestException as e:
        print(f"Сетевая ошибка при запросе к IP-API: {e}")
        return None, None
city, country = get_location_from_ipapi("184.22.181.233")
if city and country:
    print(city, country)
# В вашем Flask-роуте или любом другом месте на сервере:
# from flask import request as flask_request # Избегаем конфликта имен

# def my_web_page_route():
#     user_ip = flask_request.remote_addr # Получить IP пользователя
#     city, country = get_location_from_ipapi(user_ip)
#     if city and country:
#         return f"Ваш город: {city}, Ваша страна: {country}"
#     else:
#         return "Не удалось определить ваше местоположение по IP."