import requests

def get_weather(city):
    """Get weather information for a city using a free weather API"""
    try:
        # Using OpenWeatherMap with a free API key (you'll need to sign up)
        # Replace 'YOUR_API_KEY' with your actual API key from openweathermap.org
        api_key = '5586add59abe22c9bca9a8d8f9782a3c'  
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        
        response = requests.get(url)
        data = response.json()
        
        if response.status_code == 200:
            weather = {
                "success": True,
                "city": data['name'],
                "country": data['sys']['country'],
                "temperature": data['main']['temp'],
                "feels_like": data['main']['feels_like'],
                "description": data['weather'][0]['description'],
                "humidity": data['main']['humidity'],
                "wind_speed": data['wind']['speed']
            }
            return weather
        else:
            return {
                "success": False,
                "error": f"Error: {data['message']}"
            }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }