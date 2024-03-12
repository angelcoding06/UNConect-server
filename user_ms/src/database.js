const { Sequelize } = require('sequelize'); // Importa Sequelize para la conexión a la base de datos
require('dotenv').config(); // Importa dotenv para cargar las variables de entorno desde el archivo .env

// Crea una instancia de Sequelize para la conexión a la base de datos
const sequelize = new Sequelize(process.env.DB_NAME, process.env.DB_USER, process.env.DB_PASSWORD, {
    host: process.env.DB_HOST, // Host de la base de datos obtenido de las variables de entorno
    port: process.env.DB_PORT, // Puerto de la base de datos obtenido de las variables de entorno
    dialect: 'postgres', // Especifica el dialecto de la base de datos como PostgreSQL
});

module.exports = { sequelize }; // Exporta la instancia de Sequelize para su uso en otros archivos
