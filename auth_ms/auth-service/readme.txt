JAVA VERSION 17

//Si se realizan cambios usar el sigueinte comando para que el archivo .jar se actualice

./mvnw clean package -DskipTests

//cabe aclarar que el '-DskipTests' es porque la configuracion esta ya hecha para la conexion dockerizada con la DB

//builde docker 
docker-compose up --build -d 

//stop docker 
docker-compose down 