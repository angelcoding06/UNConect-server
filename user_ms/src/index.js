const express = require('express')
const app = express()
const port = 3000
const { sequelize } = require('./database');
const userRoutes = require('./routes/user.js');
const User = require('./models/usermodel');

async function authenticateDatabase() {
  try {
    await sequelize.authenticate();
    await User.sync({ force: true }); // Opciones de sincronización según tu necesidad
    console.log('Database connection established and models synced successfully');
  } catch (error) {
    console.error('Error connecting to database and syncing models:', error);
  }
}

authenticateDatabase();

app.get('/', (req, res) => {
  res.send('UNConnect users')
})

// Usa las rutas de usuarios en la ruta /users
app.use(express.json());
app.use('/users', userRoutes);

app.listen(port, () => {
  console.log(`App listening on port ${port} 🔥`)
})