// Importa los módulos necesarios
const { DataTypes } = require('sequelize');
const sequelize = require('../database').sequelize;
const { v4: uuidv4 } = require('uuid');
const User = require('./usermodel'); // Importa el modelo de usuario

// Define el modelo Friendship utilizando Sequelize
const Friendship = sequelize.define('Friendship', {
  ID: {
    type: DataTypes.UUID, // Tipo de datos UUID para el ID
    defaultValue: DataTypes.UUIDV4, // Valor predeterminado generado automáticamente con UUIDV4
    allowNull: false, // No permite valores nulos
    primaryKey: true // Define la clave primaria
  },
  senderId: {
    type: DataTypes.INTEGER, // Tipo de datos INTEGER para el ID del remitente
    allowNull: false, // No permite valores nulos
  },
  receiverId: {
    type: DataTypes.INTEGER, // Tipo de datos INTEGER para el ID del receptor
    allowNull: false, // No permite valores nulos
  },
  status: {
    type: DataTypes.ENUM('pending', 'accepted'), // Tipo de datos ENUM para el estado de la amistad
    allowNull: false, // No permite valores nulos
    defaultValue: 'pending' // Valor predeterminado para el estado: 'pending'
  }
});

module.exports = Friendship; // Exporta el modelo Friendship para su uso en otros archivos
