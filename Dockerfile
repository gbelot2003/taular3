# Usa una imagen base de Python
FROM python:3.9-slim

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos de tu proyecto al contenedor
COPY . /app

# Instala las dependencias
# RUN pip install --no-cache-dir -r requirements.txt
RUN pip install -r requirements.txt

# Expone el puerto en el que tu app correrá
EXPOSE 5000

# Comando para iniciar la app con Gunicorn
#CMD ["gunicorn", "--bind", "0.0.0.0:5000", "run:app"]
CMD ["gunicorn", "-c", "gunicorn_config.py", "run:app"]