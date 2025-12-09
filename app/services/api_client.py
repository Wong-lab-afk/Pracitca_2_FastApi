import httpx
import os

#API_KEY = os.getenv("EXTERNAL_API_KEY")
BASE_URL = os.getenv("EXTERNAL_API_URL", "https://api.api-ninjas.com/v1/geocoding")

async def fetch_city_info(city: str):
    params = {"city": city}
    headers = {"X-Api-Key": "3ttG6iHCdnYityyM7UiqeQ==yjiouPULD60B4Scx"}
    
    #Manejo de errores básico requerido
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(BASE_URL, params=params, headers=headers, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error fetching external API: {e}")
            return {"error": "no_external_data"}
