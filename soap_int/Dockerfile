# Usa la imagen base de Python
FROM python:3.7

# Establece el directorio de trabajo en /app
WORKDIR /app

# Copia el archivo de requerimientos al contenedor
COPY ./requirements.txt /app/requirements.txt

# Instala las dependencias del proyecto
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copia todos los archivos al contenedor
COPY . .

# Expone el puerto 8082 para el servidor SOAP
EXPOSE 8082

# Ejecuta el servidor SOAP al iniciar el contenedor
CMD [ "python", "wsdlserver.py" ]