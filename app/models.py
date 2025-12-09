from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional # <------------ se agrego esto por error en el docker
# Modelo para crear un lead (Input)
class LeadCreate(BaseModel):
    name: str
    email: EmailStr
    phone: str
    restaurant_type: str
    city: str

# Modelo de respuesta (Output) - hereda de Create y agrega ID
class LeadResponse(LeadCreate):
    id: int
    # --- NUEVOS CAMPOS ---
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    # En V2, "orm_mode" ahora se llama "from_attributes"
    model_config = ConfigDict(from_attributes=True)

class Config:
        orm_mode = True
