from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel 
from sqlalchemy.orm import Session
from typing import List
from app.db import engine, Base, get_db
from app import models, schemas
from app.services.api_client import fetch_city_info
from app.services.vector_service import get_vector, calculate_similarity

# Crear tablas en BD al inicio (para desarrollo)
Base.metadata.create_all(bind=engine)
app = FastAPI(title="Lead Service")

# 1. Health Check 
@app.get("/health")
def health_check():
    return {"status": "ok"}

# 2. Crear Lead
@app.post("/api/leads", response_model=models.LeadResponse)
async def create_lead(lead: models.LeadCreate, db: Session = Depends(get_db)):
    # A. Llamada a API externa (asíncrona) 
    city_info = await fetch_city_info(lead.city)
    print(f"Información externa para {lead.city}: {city_info}")
    
    # B. Guardar en Postgres 
    db_lead = schemas.Lead(
        name=lead.name,
        email=lead.email,
        phone=lead.phone,
        restaurant_type=lead.restaurant_type,
        city=lead.city
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
    # Obtener todos los leads (en producción esto se haría con vectores en BD)
    leads = db.query(schemas.Lead).all()
    
    query_vector = get_vector(search.query)
    results = []
    
    for lead in leads:
        # Creamos un "texto" del lead para comparar. Ej: combinando nombre y tipo
        lead_text = f"{lead.restaurant_type} en {lead.city}"
        lead_vector = get_vector(lead_text)
        
        score = calculate_similarity(query_vector, lead_vector)
        results.append({
            "lead": lead,
            "similarity_score": score
        })
    
    # Ordenar por similitud descendente
    results.sort(key=lambda x: x["similarity_score"], reverse=True)
    
    return results
