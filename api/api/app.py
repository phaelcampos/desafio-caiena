import owm.omw as owm
from fastapi import FastAPI, HTTPException
from github import Github

owm_sdk = owm.OpenWeatherMapSDK("")
github = Github("")
app = FastAPI()

@app.get("/weather",)
async def get_weather(city: str):
    if not city:
        raise HTTPException(status_code=400, detail="City parameter is required")
    
    weather_data = owm_sdk.get_weather("são José dos campos")
    
    return weather_data
