# Helper Functions 
from secretkey import API_SECRETIVE_KEY
from flask import Flask
# from models import Voyage 
import requests

app = Flask(__name__) 

def get_weather(lat, lon):
    """Get Today's Weather""" 
    URL = f'https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude=alerts,minutely,current,hourly&units=metric&appid={API_SECRETIVE_KEY}'

    response = requests.get(URL)

    # import pdb 
    # pdb.set_trace() 
    # response # Response[200]
    # data = response.json() 
    # max_temp = data['daily'][0]['temp']['max'] 

    data = response.json() 

    max_temp = data['daily'][0]['temp']['max']
    max_temp_round = round(max_temp)
    min_temp = data['daily'][0]['temp']['min']
    min_temp_round = round(min_temp) 
    humidity = data['daily'][0]['humidity']
    wind_speed = data['daily'][0]['wind_speed']
    wind_speed_knots = round(wind_speed * 1.944, 3) 
    wind_deg = data['daily'][0]['wind_deg'] 
    wind_gust = data['daily'][0]['wind_gust'] 
    condition = data['daily'][0]['weather'][0]['main']

    return {
        'max_temp': max_temp_round, 
        'min_temp': min_temp_round, 
        'humidity': humidity,
        'wind_speed': wind_speed_knots,
        'wind_deg': wind_deg,
        'wind_gust': wind_gust,
        'condition': condition,
    }