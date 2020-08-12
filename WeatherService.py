import requests


def find_by_city():
    city = input("Введи город: ")
    url = 'http://api.openweathermap.org/data/2.5/weather?q=' + city + '&appid=24b79c83f930a5580feb4c0ccc717fde&units=metric'
    res = requests.get(url)
    data = res.json()
    show_data(data)


def show_data(data):
    temp = data['main']['temp']
    wind_speed = data['wind']['speed']
    print('Температура : {} С°'.format(temp))
    print('Скорость ветра : {} м/с'.format(wind_speed))


if __name__ == '__main__':
    find_by_city()