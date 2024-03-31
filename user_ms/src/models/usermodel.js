// Importa los módulos necesarios
const { Sequelize, DataTypes } = require('sequelize');
const sequelize = require('../database').sequelize; // Importa la instancia de Sequelize configurada
const { v4: uuidv4 } = require('uuid');

// Define el modelo User utilizando Sequelize
const User = sequelize.define('User', {
  ID: {
    type: DataTypes.UUID, // Tipo de datos UUID para el ID
    defaultValue: DataTypes.UUIDV4, // Valor predeterminado generado automáticamente con UUIDV4
    allowNull: false, // No permite valores nulos
    primaryKey: true // Define la clave primaria
  },
  ID_Auth: {
    type: DataTypes.STRING, // Tipo de datos STRING para el ID de autenticación
    allowNull: false // No permite valores nulos
  },
  Name: {
    type: DataTypes.STRING, // Tipo de datos STRING para el nombre
    allowNull: false // No permite valores nulos
  },
  Last_Name: {
    type: DataTypes.STRING, // Tipo de datos STRING para el apellido
    allowNull: false // No permite valores nulos
  },
  Birthday: {
    type: DataTypes.DATEONLY, // Tipo de datos DATEONLY para la fecha de nacimiento
    allowNull: false // No permite valores nulos
  },
  Campus: {
    type: DataTypes.STRING, // Tipo de datos STRING para el campus
    allowNull: false, // No permite valores nulos
    validate: {
      isIn: { // Validación para asegurar que el valor esté dentro de una lista específica
        args: [['Amazonía', 'Bogotá', 'Caribe', 'La Paz', 'Manizalez', 'Medellín', 'Orinoquia', 'Palmira', 'Tumaco']],
        msg: 'El campo Campus no admite ese valor' // Mensaje de error personalizado si la validación falla
      }
    }
  },
  Faculty: {
    type: DataTypes.STRING, // Tipo de datos STRING para la facultad
    allowNull: false, // No permite valores nulos
    validate: {
      isIn: { // Validación para asegurar que el valor esté dentro de una lista específica
        args: [['AGRONOMÍA', 'ARTES', 'CIENCIAS', 'CIENCIAS AGRARIAS', 'CIENCIAS ECONÓMICAS', 'CIENCIAS HUMANAS', 'DERECHO, CIENCIAS POLÍTICAS Y SOCIALES', 'ENFERMERÍA', 'INGENIERÍA', 'MEDICINA', 'MEDICINA VETERINARIA Y DE ZOOTECNIA', 'ODONTOLOGÍA']],
        msg: 'El campo Faculty no admite ese valor' // Mensaje de error personalizado si la validación falla
      }
    }
  },
  Career: {
    type: DataTypes.STRING, // Tipo de datos STRING para la carrera
    allowNull: false // No permite valores nulos
  },
  MemberUN_Since: {
    type: DataTypes.INTEGER, // Tipo de datos INTEGER para el año de ingreso
    allowNull: false, // No permite valores nulos
    validate: {
      len: [4, 4] // Validación para asegurar que la longitud sea de 4 dígitos
    }
  },
  Phone_Number: {
    type: DataTypes.INTEGER, // Tipo de datos INTEGER para el número de teléfono
    allowNull: false // No permite valores nulos
  },
  Gender: {
    type: DataTypes.STRING, // Tipo de datos STRING para el género
    allowNull: false // No permite valores nulos
  },
  Profile_Photo: {
    type: DataTypes.STRING, // Tipo de datos STRING para la URL de la foto de perfil
    allowNull: false // No permite valores nulos
  },
  myGroups: {
    type: DataTypes.ARRAY(DataTypes.STRING) // Tipo de datos ARRAY de STRING para los grupos a los que pertenece el usuario
  }
});

module.exports = User; // Exporta el modelo User para su uso en otros archivos
