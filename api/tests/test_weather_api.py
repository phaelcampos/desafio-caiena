import json
import os
from http import HTTPStatus
from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient

from api.app import app, get_weather
from api.utils.message_formater import format_weather_data

client = TestClient(app)


def load_mock_data(filename):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, 'resources', filename)
    with open(file_path, 'r') as file:
        return json.load(file)


@pytest.fixture
def mock_owm_sdk():
    with patch('api.app.owm_sdk') as mock:
        yield mock


@pytest.fixture
def mock_github():
    with patch('api.app.github') as mock:
        yield mock


def test_get_weather_city_not_provided(mock_owm_sdk):
    response = client.get('/weather/')
    assert response.status_code == 404


def test_get_weather_city_not_found(mock_owm_sdk):
    mock_owm_sdk.get_weather.return_value = {'status': HTTPStatus.NOT_FOUND}
    response = client.get('/weather/NonExistentCity')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'City NonExistentCity not found'}


def test_get_weather_successful(mock_owm_sdk, mock_github):
    mock_weather_data = load_mock_data('weather_response.json')

    mock_owm_sdk.get_weather.return_value = mock_weather_data

    mock_gist = MagicMock()
    mock_gist.html_url = 'https://gist.github.com/user/1234567890abcdef'
    mock_github.get_user.return_value.create_gist.return_value = mock_gist

    response = client.get('/weather/London')
    result = response.text.strip('"')
    assert response.status_code == HTTPStatus.OK
    assert result == 'https://gist.github.com/user/1234567890abcdef'


@pytest.mark.asyncio
async def test_get_weather_function(mock_owm_sdk, mock_github):
    mock_weather_data = load_mock_data('weather_response.json')
    mock_owm_sdk.get_weather.return_value = mock_weather_data

    mock_gist = MagicMock()
    mock_gist.html_url = 'https://gist.github.com/user/1234567890abcdef'
    mock_github.get_user.return_value.create_gist.return_value = mock_gist

    result = await get_weather('London')
    assert result == 'https://gist.github.com/user/1234567890abcdef'

    mock_github.get_user.return_value.create_gist.assert_called_once_with(
        public=False,
        files={'London_weather.md': pytest.approx(any(dict))},
        description='my description',
    )


def test_format_weather_data(mock_owm_sdk):
    mock_weather_data = load_mock_data('weather_response.json')

    formatted_data = format_weather_data(mock_weather_data['data'])
    assert 'São José dos Campos' in formatted_data
    assert '24°C' in formatted_data
    assert 'Clouds' in formatted_data
