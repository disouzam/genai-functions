import requests

def get_current_weather(latitude, longitude):
    print(f"Fetching current weather for coordinates: {latitude}, {longitude}")
    response = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,wind_speed_10m&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m")
    data = response.json()
    return data['current']['temperature_2m']

def get_my_location():
    print("Fetching my current location.")
    dummy_location = {
        'latitude': -19.934016866168683,
        'longitude': -43.93634461364911
    }
    return dummy_location