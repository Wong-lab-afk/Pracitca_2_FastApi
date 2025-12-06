from pydantic import BaseModel, EmailStr

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
    
    class Config:
        from_attributes = True # Antes orm_mode = True