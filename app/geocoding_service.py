# geocoding_service.py
import httpx
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("NINJAS_API_KEY") # Recuerda poner esto en tu .env

async def obtener_coordenadas(city: str):
    url = "https://api.api-ninjas.com/v1/geocoding"
    headers = {'X-Api-Key': API_KEY}
    params = {'city': city}
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, params=params)
            if response.status_code == 200:
                data = response.json()
                if data:
                    return {
                        "latitude": data[0]['latitude'],
                        "longitude": data[0]['longitude']
                    }
            return None
        except Exception as e:
            print(f"Error conectando con API Ninjas: {e}")
            return None