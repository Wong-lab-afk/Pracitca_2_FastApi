import requests
import os
from dotenv import load_dotenv

# Carga las variables de entorno (asegúrate de tener tu archivo .env listo)
load_dotenv()

API_KEY = os.getenv("NINJAS_API_KEY")  # Guárdala en tu .env como NINJAS_API_KEY=tu_clave_aqui
BASE_URL = "https://api.api-ninjas.com/v1/geocoding"

def obtener_coordenadas(ciudad: str, pais: str = ""):
    """
    Consulta la API de Ninjas para obtener latitud y longitud.
    Retorna un diccionario con 'lat' y 'lon' o None si falla.
    """
    if not API_KEY:
        raise ValueError("Error: No se ha configurado la API Key de Ninjas.")

    # Parámetros de la consulta
    params = {'city': ciudad}
    if pais:
        params['country'] = pais

    headers = {'X-Api-Key': API_KEY}

    try:
        response = requests.get(BASE_URL, params=params, headers=headers)
        
        if response.status_code == 200:
            datos = response.json()
            if datos:
                # La API devuelve una lista; tomamos el primer resultado (el más relevante)
                resultado = datos[0]
                return {
                    "latitud": resultado.get("latitude"),
                    "longitud": resultado.get("longitude"),
                    "nombre": resultado.get("name"),
                    "pais": resultado.get("country")
                }
            else:
                print(f" No se encontraron resultados para: {ciudad}")
                return None
        else:
            print(f" Error en la API externa: {response.status_code} - {response.text}")
            return None

    except Exception as e:
        print(f" Error de conexión: {e}")
        return None
