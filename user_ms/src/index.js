const express = require('express')
const app = express()
const port = 3000
const { sequelize } = require('./database');
const userRoutes = require('./routes/user.js');
const friendsRoutes = require('./routes/friends.js');
const User = require('./models/usermodel');
const Friends = require('./models/friendsmodel');

async function authenticateDatabase() {
  try {
    await sequelize.authenticate();
    await User.sync({ force: false }); // Opciones de sincronización según tu necesidad
    await Friends.sync({ force: false });
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
app.use('/friends', friendsRoutes);



app.listen(port, () => {
  console.log(`App listening on port ${port} 🔥`)
})