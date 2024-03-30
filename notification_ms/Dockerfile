# Establece la imagen base
FROM golang:latest

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia el contenido del directorio actual al directorio /app en el contenedor
COPY . .

# Copia el archivo serviceAccountKey.json al directorio de trabajo del contenedor
COPY serviceAccountKey.json /app

# Descarga los módulos necesarios si estás utilizando Go Modules
RUN go mod download

# Compila la aplicación Go
RUN go build -o main .

# Expone el puerto en el que la aplicación se ejecutará dentro del contenedor
EXPOSE 8080

# Comando para ejecutar la aplicación cuando se inicie el contenedor
CMD ["./main"]