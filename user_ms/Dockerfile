FROM node:latest

# Establece el directorio de trabajo en /app
WORKDIR /usr/src/user_ms

# Copia el package.json y el package-lock.json a /app
COPY package*.json ./

# Instala las dependencias
RUN npm install

# Copia el resto de los archivos de la aplicación a /app
COPY . .

# Expone el puerto en el que se ejecutará tu aplicación
EXPOSE 3003

# Ejecuta el comando para iniciar la aplicación
CMD ["npm", "start"]