# Usar una imagen base oficial de Python
FROM python:3.11-slim

# Establecer variables de entorno
# PYTHONDONTWRITEBYTECODE: Previene que Python escriba archivos .pyc
# PYTHONUNBUFFERED: Asegura que la salida de Python se envíe directamente al terminal
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Establecer el directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema necesarias para psycopg2 y otros
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar el archivo de requerimientos
COPY requirements.txt /app/

# Instalar dependencias de Python
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copiar el resto del código del proyecto
COPY . /app/

# Recolectar archivos estáticos (si se usa WhiteNoise)
# RUN python manage.py collectstatic --noinput

# Exponer el puerto 8000
EXPOSE 8000

# Comando por defecto (puede ser sobreescrito por docker-compose)
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi:application"]
