from enum import Enum


class WeatherTranslation(Enum):
    CLEAR = 'Céu Limpo'
    CLOUDS = 'Nublado'
    RAIN = 'Chuva'
    DRIZZLE = 'Chuvisco'
    THUNDERSTORM = 'Tempestade'
    SNOW = 'Neve'
    MIST = 'Névoa'
    FOG = 'Neblina'
    HAZE = 'Neblina Seca'
    SMOKE = 'Fumaça'
    DUST = 'Poeira'
    SAND = 'Areia'
    ASH = 'Cinzas'
    SQUALL = 'Rajada'
    TORNADO = 'Tornado'

    @classmethod
    def translate(cls, english_weather):
        try:
            return cls[english_weather.upper()].value
        except KeyError:
            return english_weather
