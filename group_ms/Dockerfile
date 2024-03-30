# Usa la imagen oficial de Python como base
FROM python:3.12

# Establece el directorio de trabajo en /app
WORKDIR /app

# Copia el archivo requirements.txt al contenedor
COPY requirements.txt .

# Instala las dependencias de la aplicación
RUN pip install -r requirements.txt

# Copia todo el contenido del directorio actual al contenedor en /app
COPY . .

# Exponer el puerto 8001 para que la aplicación Django pueda ser accesible desde el exterior
EXPOSE 8001

# Define las variables de entorno necesarias para Django
ENV DJANGO_SETTINGS_MODULE=group_ms.settings
ENV PYTHONUNBUFFERED=1

# Ejecuta las migraciones de Django
RUN python manage.py migrate

# Comando para arrancar el servidor de desarrollo de Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8001"]
