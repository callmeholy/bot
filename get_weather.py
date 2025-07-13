import requests
import datetime
from tokens import open_weather_token
from translatepy.translators.google import GoogleTranslate
translate = GoogleTranslate()


def get_weather_all_day(city, token):
    my_req = requests.get(f'https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={token}&units=metric')
    data = my_req.json()
    result = {}
    for i in data['list']:
        if str(datetime.datetime.fromtimestamp(i['dt']))[:10] == str(datetime.datetime.today())[:10]:
            result[str(datetime.datetime.fromtimestamp(i['dt']))[11:]] = round(i['main']['temp'])
    return result


def get_weather_for_5_days(city, token):
    my_req = requests.get(f'https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={token}&units=metric')
    data = my_req.json()
    result = {}
    for i in data['list']:
        if (str(datetime.datetime.fromtimestamp(i['dt'])).endswith('15:00:00') or
                str(datetime.datetime.fromtimestamp(i['dt'])).endswith('12:00:00') or
                str(datetime.datetime.fromtimestamp(i['dt'])).endswith('18:00:00')):
            result[str(datetime.datetime.fromtimestamp(i['dt']))] = round(i['main']['temp'])
    return result


def get_weather(city, token):
    my_req = requests.get(
        f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={token}&units=metric'
    )
    data = my_req.json()
    result = {
        'cur_city': data['name'], 'cur_temp' : str(round(data['main']['temp'])) + 'C°',
        'feels_like': str(round(data['main']['feels_like'], 1)) + 'C°',
        'wind_speed': data['wind']['speed'],
        'description': translate.translate(data['weather'][0]['description'], 'ru')
    }
    return result


def main():
    city = input('Введите город: ')
    result = get_weather(city, open_weather_token)
    print(result)


if __name__ == '__main__':
    main()
