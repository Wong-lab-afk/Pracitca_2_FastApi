from sqlalchemy import Column, Integer, String, Float
from app.db import Base

class Lead(Base):
    __tablename__ = "leads" # [cite: 61]

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    restaurant_type = Column(String, nullable=False)
    city = Column(String, nullable=False)
    #Columnas que se agregaron c:
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    # Puedes agregar una columna para guardar la respuesta de la API externa si deseas
