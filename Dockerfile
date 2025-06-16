# Usa una imagen base oficial de Python
FROM python:3.9-slim

# Establece el directorio de trabajo en el contenedor
WORKDIR /app

# Copia el archivo de requisitos
COPY requirements.txt .

# Instala las dependencias del sistema necesarias para osmnx
RUN apt-get update && apt-get install -y \
    build-essential \
    libgeos-dev \
    libproj-dev \
    proj-data \
    proj-bin \
    libspatialindex-dev \
    libgdal-dev \
    && rm -rf /var/lib/apt/lists/*

# Instala las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto de la aplicación
COPY . .

# Expone el puerto en el que correrá la aplicación
EXPOSE 5000

# Variable de entorno para producción
ENV FLASK_ENV=production

# Comando para ejecutar Gunicorn (mejor para producción que `python app.py`)
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]



