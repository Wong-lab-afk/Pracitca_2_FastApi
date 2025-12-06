# Usamos una imagen ligera de Python
FROM python:3.10-slim

# Evita que Python escriba archivos .pyc y habilita logs en tiempo real
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Instalamos dependencias del sistema necesarias para psycopg2 (postgres)
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiamos los requirements y los instalamos
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el resto del código
COPY . .

# Comando para correr la app
# Nota: --host 0.0.0.0 es obligatorio dentro de Docker para salir al exterior
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]