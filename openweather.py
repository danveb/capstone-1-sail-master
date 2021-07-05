# OpenweatherMap API 

import requests 

API_KEY = '8fc4d6f3f7c922e3476f07c266677ab7'

def current_weather(lat, lon):
    """OpenweatherMap API -> One Call API
    
    Provides the following weather data for any geographical coordinates: 
    - Current weather

    Parameters
    - lat, lon (required) -> Geographical coordinates (latitude, longitude)
    - appid	(required) -> Your unique API key (you can always find it on your account page under the "API key" tab)
    - exclude (optional) -> By using this parameter you can exclude some parts of the weather data from the API response. It should be a comma-delimited list (without spaces).
        
        Available values:
        - current
        - minutely
        - hourly
        - daily
        - alerts
    
    - units	(optional) -> Units of measurement. standard, metric and imperial units are available. If you do not use the units parameter, standard units will be applied by default. 
    - lang	(optional) -> You can use the lang parameter to get the output in your language. 
    """

    # Current Weather
    URL = f'https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude=alerts,minutely,hourly,daily&units=metric&appid={API_KEY}'

    response = requests.get(URL).json()

    temp = response['current']['temp']
    humidity = response['current']['humidity']
    clouds = response['current']['clouds']
    visibility = response['current']['visibility']
    wind_speed = response['current']['wind_speed']
    wind_deg = response['current']['wind_deg']

    return {
        'temp': temp, 
        'humidity': humidity,
        'clouds': clouds,
        'visibility': visibility,
        'wind_speed': wind_speed,
        'wind_deg': wind_deg,
    }

# chicago = current_weather('41.8813', '-87.6163')
# print(chicago) 
# # {'temp': 25.63, 'humidity': 47, 'clouds': 1, 'visibility': 10000, 'wind_speed': 3.58, 'wind_deg': 327}

# milwaukee = current_weather('43.3', '-87.5389')
# print(milwaukee)
# # {'temp': 26.75, 'humidity': 79, 'clouds': 2, 'visibility': 10000, 'wind_speed': 6.48, 'wind_deg': 281}

# pier_25_marina = current_weather('40.439', '-74.051')
# print(pier_25_marina)
# # {'temp': 17.72, 'humidity': 89, 'clouds': 100, 'visibility': 10000, 'wind_speed': 3.13, 'wind_deg': 48}

def daily_forecast(lat, lon):
    """OpenweatherMap API -> One Call API
    
    Provides the following weather data for any geographical coordinates: 
    - Daily forecast for 7 days

    Parameters
    - lat, lon (required) -> Geographical coordinates (latitude, longitude)
    - appid	(required) -> Your unique API key (you can always find it on your account page under the "API key" tab)
    - exclude (optional) -> By using this parameter you can exclude some parts of the weather data from the API response. It should be a comma-delimited list (without spaces).
        
        Available values:
        - current
        - minutely
        - hourly
        - daily
        - alerts
    
    - units	(optional) -> Units of measurement. standard, metric and imperial units are available. If you do not use the units parameter, standard units will be applied by default. 
    - lang	(optional) -> You can use the lang parameter to get the output in your language. 
    """

    # Hourly Forecast
    URL = f'https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude=alerts,minutely,current,hourly&units=metric&appid={API_KEY}'

    response = requests.get(URL).json()

    # need to loop over each day to 
    min_temp = [d['temp']['min'] for d in response['daily']]
    max_temp = [d['temp']['max'] for d in response['daily']]

    # humidity = response['daily']['humidity']
    # clouds = response['daily']['clouds']
    # visibility = response['daily']['visibility']
    # wind_speed = response['daily']['wind_speed']
    # wind_deg = response['daily']['wind_deg']

    return {
        'min_temp': min_temp, 
        'max_temp': max_temp,

        # 'humidity': humidity,
        # 'clouds': clouds,
        # 'visibility': visibility,
        # 'wind_speed': wind_speed,
        # 'wind_deg': wind_deg,
    }

chicago = daily_forecast('41.8813', '-87.6163')
print(chicago) 

# milwaukee = daily_forecast('43.3', '-87.5389')
# print(milwaukee)

# pier_25_marina = daily_forecast('40.439', '-74.051')
# print(pier_25_marina)