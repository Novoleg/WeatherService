import requests
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'thisisasecret'
db = SQLAlchemy(app)


class City(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)


def get_weather_data(city):
    """
    Обращение к сервису OpenWeather по API
    """
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid=24b79c83f930a5580feb4c0ccc717fde&units=metric&lang=ru'
    r = requests.get(url).json()
    print(r)
    return r


@app.route('/')
def index_get():
    cities = City.query.all()
    weather_data = []

    for city in cities:
        r = get_weather_data(city.name)

        weather = {
            'city': city.name,
            'temperature': r['main']['temp'],
            'description': r['weather'][0]['description'],
            'icon': r['weather'][0]['icon'],
            'recommendation': '',

        }

        if 20 < weather['temperature'] < 25:
            weather['recommendation'] = 'На улице приятная погода, одевайся легко'
        elif weather['temperature'] > 25:
            weather['recommendation'] = '''На улице очень жарко, надень головной убор'''
        else:
            weather['recommendation'] = 'На улице прохладно, надень ветровку'

        weather_data.append(weather)

    return render_template('weather.html', weather_data=weather_data)


@app.route('/', methods=['POST'])
def index_post():
    error_message = ''
    new_city = request.form.get('city')

    if new_city:
        existing_city = City.query.filter_by(name=new_city).first()

        if not existing_city:
            new_city_data = get_weather_data(new_city)

            if new_city_data['cod'] == 200:
                new_city_obj = City(name=new_city)
                db.session.add(new_city_obj)
                db.session.commit()
            else:
                error_message = 'Такого города не сущетсвует!'
        else:
            error_message = 'Город уже есть!'

    if error_message:
        flash(error_message, 'error')
    else:
        flash('Город добавлен')

    return redirect(url_for('index_get'))


if __name__ == '__main__':
    app.run(host='10.24.64.39')
