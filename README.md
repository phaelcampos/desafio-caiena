# Weather API Project

This project is a FastAPI-based web service that provides weather information for a given city using the OpenWeatherMap API. It also creates a GitHub gist with the formatted weather data.

## Features

- Fetch weather data for a specified city
- Create a private GitHub gist with the weather information
- Use of custom OWM (OpenWeatherMap) SDK

## Requirements

- Python 3.12
- Poetry for dependency management
- Docker (optional)

## Clone the repository

   ```
   git clone https://github.com/phaelcampos/desafio-caiena.git
   cd desafio-caiena
   ```
   
## Generating OWM Wheel File

To generate a .whl file for the OWM library and move it to the root directory of the app:

1. Navigate to the OWM library directory:
   ```
   cd desafio-caiena/owm
   ```

2. Use Poetry to build the wheel file:
   ```
   poetry build
   ```

3. Move the generated .whl file to the root directory of the api:
   ```
   mv /owm/dist/owm-0.1.0-py3-none-any.whl desafio-caiena/api
   ```
****
## Installation

2. Enter on the api folder and install dependencies using Poetry:
   ```
   poetry install
   ```

3. Set up environment variables:
   Create a `.env` file in the project root and add the following:
   ```
   OWM_KEY=your_openweathermap_api_key
   GITHUB_KEY=your_github_api_key
   ```

## Usage

To run the FastAPI server:

```
poetry run task run
```

The API will be available at `http://localhost:8000`.

### Endpoints

- GET `/weather/{city}`: Get weather information for a specific city

Example:
```
curl http://localhost:8000/weather/London
```

## Running with Docker

To run the project using Docker:

1. Build the Docker image:
   ```
   docker build -t weather-api .
   ```

2. Run the Docker container:
   ```
   docker run -p 8000:8000 -e OWM_KEY=your_openweathermap_api_key -e GITHUB_KEY=your_github_api_key weather-api
   ```

   Replace `your_openweathermap_api_key` and `your_github_api_key` with your actual API keys.

The API will be available at `http://localhost:8000`.

## Development

- Lint the code: `poetry run task lint`
- Format the code: `poetry run task format`
- Run tests: `poetry run task test`


## Contributors

- raphael <raphaelcamachado@gmail.com>
