import requests
from requests.exceptions import RequestException
from http import HTTPStatus


class OpenWeatherMapSDK:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "http://api.openweathermap.org/data/2.5/forecast"

    def get_weather(self, city, days=5):
        if days > 5:
            return {
                "status": HTTPStatus.BAD_REQUEST,
                "message": "Please use a max of five days",
            }
        params = {
            "q": city,
            "appid": self.api_key,
            "units": "metric",
            "cnt": min(days * 8, 40),
        }
        try:
            response = requests.get(self.base_url, params=params)
            data = response.json()

            if "cod" in data and data["cod"] == "404":
                return {
                    "status": HTTPStatus.NOT_FOUND,
                    "message": f"City {city} not found",
                }
            return data, days
        except RequestException as e:
            return {
                "status": HTTPStatus.BAD_REQUEST,
                "message": f"Request failed: {str(e)}",
            }
