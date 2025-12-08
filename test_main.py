from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    # CAMBIO IMPORTANTE: Apuntamos a "/health" que sí existe en tu código
    response = client.get("/health")
    
    # Verificamos que sea exitoso (200)
    assert response.status_code == 200
    
    # Verificamos que la respuesta sea la esperada
    assert response.json() == {"status": "ok"}