from pydantic import BaseModel

class WeatherResponse(BaseModel):
    weather: dict
    gist_url: str
