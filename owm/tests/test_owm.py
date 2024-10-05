from owm.owm import OpenWeatherMapSDK
import pytest
from unittest.mock import patch, Mock
from http import HTTPStatus

@pytest.fixture
def sdk():
    return OpenWeatherMapSDK(api_key="test_api_key")


def test_init():
    sdk = OpenWeatherMapSDK(api_key="test_api_key")
    assert sdk.api_key == "test_api_key"
    assert sdk.base_url == "http://api.openweathermap.org/data/2.5/forecast"


def test_get_weather_days_exceed_limit(sdk):
    result = sdk.get_weather("London", days=6)
    assert result["status"] == HTTPStatus.BAD_REQUEST
    assert result["message"] == "Please use a max of five days"


@patch('requests.get')
def test_get_weather_success(mock_get, sdk):
    mock_response = Mock()
    mock_response.json.return_value = {"city": "London", "list": []}
    mock_get.return_value = mock_response

    data, days = sdk.get_weather("London", days=3)

    assert data == {"city": "London", "list": []}
    assert days == 3
    mock_get.assert_called_once_with(
        sdk.base_url,
        params={
            "q": "London",
            "appid": "test_api_key",
            "units": "metric",
            "cnt": 24  # 3 days * 8 forecasts per day
        }
    )


@patch('requests.get')
def test_get_weather_city_not_found(mock_get, sdk):
    mock_response = Mock()
    mock_response.json.return_value = {"cod": "404"}
    mock_get.return_value = mock_response

    result = sdk.get_weather("NonexistentCity")

    assert result["status"] == HTTPStatus.NOT_FOUND
    assert result["message"] == "City NonexistentCity not found"
