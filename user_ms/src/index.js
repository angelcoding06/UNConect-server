const express = require('express'); // Importa Express
const app = express(); // Crea una instancia de la aplicación Express
const port = 3003; // Puerto en el que la aplicación escuchará las solicitudes
const { sequelize } = require('./database'); // Importa la instancia de Sequelize para la conexión a la base de datos
const userRoutes = require('./routes/user.js'); // Importa las rutas relacionadas con los usuarios
const friendsRoutes = require('./routes/friends.js'); // Importa las rutas relacionadas con los amigos
const User = require('./models/usermodel'); // Importa el modelo de usuario
const Friends = require('./models/friendsmodel'); // Importa el modelo de amigos

// Función asincrónica para autenticar la conexión a la base de datos y sincronizar los modelos
async function authenticateDatabase() {
  try {
    await sequelize.authenticate(); // Autentica la conexión a la base de datos
    await User.sync({ force: true }); // Sincroniza el modelo de usuario con la base de datos
    await Friends.sync({ force: true }); // Sincroniza el modelo de amigos con la base de datos
    console.log('Database connection established and models synced successfully'); // Muestra un mensaje de éxito en la consola
  } catch (error) {
    console.error('Error connecting to database and syncing models:', error); // Muestra un mensaje de error si falla la conexión o sincronización
  }
}

authenticateDatabase(); // Llama a la función para autenticar la conexión a la base de datos y sincronizar los modelos

app.get('/', (req, res) => {
  res.send('UNConnect users'); // Ruta de inicio que muestra un mensaje simple
});

// Usa las rutas de usuarios en la ruta /users y las rutas de amigos en la ruta /friends
app.use(express.json()); // Habilita el middleware para analizar el cuerpo de las solicitudes en formato JSON
app.use('/users', userRoutes); // Usa las rutas de usuarios
app.use('/friends', friendsRoutes); // Usa las rutas de amigos

// Inicia el servidor Express y lo hace escuchar en el puerto especificado
app.listen(port, () => {
  console.log(`App listening on port ${port} 🔥`); // Muestra un mensaje en la consola cuando la aplicación se inicia correctamente
});
