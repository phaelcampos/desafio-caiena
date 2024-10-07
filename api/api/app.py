import os
from http import HTTPStatus

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from github import Github, InputFileContent
from owm import owm

from api.utils.message_formater import format_weather_data

load_dotenv()

owm_sdk = owm.OpenWeatherMapSDK(os.getenv('OWM_KEY'))
github = Github(os.getenv('GITHUB_KEY'))
app = FastAPI()


@app.get('/weather/{city}')
async def get_weather(city: str) -> str:
    if not city:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='City parameter is required',
        )
    weather_data = owm_sdk.get_weather(city)
    if (
        weather_data['status']
        and weather_data['status'] == HTTPStatus.NOT_FOUND
    ):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail=f'City {city} not found'
        )
    message = format_weather_data(weather_data['data'])
    gist = github.get_user().create_gist(
        public=False,
        files={f'{city}_weather.md': InputFileContent(message)},
    )

    return gist.html_url
