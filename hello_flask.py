import requests
from flask import Flask, render_template

app = Flask(__name__)
app.config['DEBUG'] = True


@app.route('/')
def index():
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid=24b79c83f930a5580feb4c0ccc717fde&units=metric'
    city = 'Новосибирск'

    r = requests.get(url.format(city)).json()
    # t = translator.translate(r['weather'][0]['description'])
    # print(t)

    weather = {
        'city': city,
        'temperature': r['main']['temp'],
        'description': r['weather'][0]['description'],
        'icon': r['weather'][0]['icon'],
    }

    return render_template('weather.html', weather=weather)


if __name__ == '__main__':
    app.run(host='10.24.64.39')
