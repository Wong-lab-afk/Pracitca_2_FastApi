from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
# Importamos la nueva función asíncrona
from app.geocoding_service import obtener_coordenadas
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db import engine, Base, get_db
from app import models, schemas
from app.services.vector_service import get_vector, calculate_similarity

# --- IMPORTANTE: ALERTA DE MIGRACIÓN ---
# Si ya tienes una base de datos creada, 'create_all' no actualizará la tabla
# para agregar las columnas lat/long. 
# Para desarrollo rápido: Borra tu archivo .db o la tabla en Postgres, 
# o usa Alembic para migrar.
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Lead Service")

# 1. Health Check 
@app.get("/health")
def health_check():
    return {"status": "ok"}

# 2. Crear Lead (CON API NINJAS IMPLEMENTADA)
@app.post("/api/leads", response_model=models.LeadResponse)
async def create_lead(lead: models.LeadCreate, db: Session = Depends(get_db)):
    
    # A. Llamada a API externa (API Ninjas)
    print(f" Buscando coordenadas para: {lead.city}...")
    coords = await obtener_coordenadas(lead.city)
    
    lat = None
    lon = None

    if coords:
        print(f" Coordenadas encontradas: {coords}")
        lat = coords['latitude']
        lon = coords['longitude']
    else:
        print(" No se encontraron coordenadas o falló la API.")

    # B. Guardar en Postgres con los nuevos datos
    db_lead = schemas.Lead(
        name=lead.name,
        email=lead.email,
        phone=lead.phone,
        restaurant_type=lead.restaurant_type,
        city=lead.city,
        latitude=lat,   # Guardamos latitud
        longitude=lon   # Guardamos longitud
    )
    
    db.add(db_lead)
    db.commit()
    db.refresh(db_lead)
    
    return db_lead

# 3. Listar Leads 
@app.get("/api/leads", response_model=List[models.LeadResponse])
def read_leads(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    leads = db.query(schemas.Lead).offset(skip).limit(limit).all()
    return leads

# 4. Buscar Similitud 
class SearchQuery(BaseModel):
    query: str

@app.post("/api/leads/search")
def search_leads(search: SearchQuery, db: Session = Depends(get_db)):
    # ... (Tu código de búsqueda vectorial se mantiene igual) ...
    leads = db.query(schemas.Lead).all()
    query_vector = get_vector(search.query)
    results = []
    
    for lead in leads:
        lead_text = f"{lead.restaurant_type} en {lead.city}"
        lead_vector = get_vector(lead_text)
        score = calculate_similarity(query_vector, lead_vector)
        results.append({
            "lead": lead,
            "similarity_score": score
        })
    
    results.sort(key=lambda x: x["similarity_score"], reverse=True)
    return results
