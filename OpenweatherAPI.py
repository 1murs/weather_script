from credentials import API_KEY
import requests


class OpenweatherAPI:
    """
    With the help of the class, we connect to the api of the site and take information with it
    temperature, latitude, longitude, etc.
    """
    URL = 'https://api.openweathermap.org'

    def __init__(self, city_name: str, code_city: str, number_days: int = 2, lang: str = 'en',
             units_measurement: str = 'metric') -> None:
        self.city_name = city_name
        self.code_city = code_city
        self.number_days = number_days
        self.lang = lang
        self.units_measurement = units_measurement
        self.__API_KEY = API_KEY

    @property
    def get_geocoding(self) -> tuple:
        src = '/geo/1.0/direct'
        params = {'q': f'{self.city_name},{self.code_city}', 'appid': self.__API_KEY, 'limit': 1}
        response = requests.get(self.URL + src, params=params).json()
        return response[0]['lat'], response[0]['lon']

    def get_forecast(self) -> tuple:
        src = '/data/2.5/weather'
        lat, lon = self.get_geocoding
        # params = {'lat': lat, 'lon': lon, 'appid': self.__API_KEY, 'units': self.units_measurement}
        params = {'q': f'{self.city_name},{self.code_city}', 'appid': self.__API_KEY, 'units': self.units_measurement}
        response = requests.get(url=self.URL + src, params=params).json()
        coord = response['coord']['lon'], response['coord']['lon']
        temp, feels_like = response['main']['temp'], response['main']['feels_like']
        return temp, feels_like, lat, lon


