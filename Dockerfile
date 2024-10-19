# Usa una imagen base de Python
FROM python:3.9-slim

# Establece el directorio de trabajo
WORKDIR /app

# Copia solo los archivos necesarios para instalar las dependencias primero
COPY requirements.txt requirements.txt

# Instala las dependencias
RUN pip install -r requirements.txt

# Copia todos los archivos del proyecto (esto se hará dinámicamente con volúmenes en docker-compose)
COPY . /app

# Expone el puerto en el que tu app correrá
EXPOSE 5000

# Comando predeterminado para el entorno de producción con Gunicorn
CMD ["gunicorn", "-c", "gunicorn_config.py", "run:app"]