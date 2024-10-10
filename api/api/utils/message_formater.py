from datetime import datetime, timedelta

from api.enums.weather_translation_enum import WeatherTranslation


def format_weather_data(data, days=5):
    city = data['city']['name']
    forecast = []
    current_date = datetime.now().date()
    for i in range(days):
        date = current_date + timedelta(days=i)
        day_data = [
            item
            for item in data['list']
            if datetime.fromtimestamp(item['dt']).date() == date
        ]
        if day_data:
            avg_temp = sum(item['main']['temp'] for item in day_data) / len(
                day_data
            )
            weather = day_data[0]['weather'][0]['main']
            translated_weather = WeatherTranslation.translate(weather)
            forecast.append(
                f"- {avg_temp:.0f}°C e {translated_weather} em {city}"
                f" em {date.strftime('%d/%m')}.\n"
            )
    return ''.join(forecast)
