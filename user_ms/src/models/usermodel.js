const { Sequelize, DataTypes } = require('sequelize');
const sequelize = require('../database').sequelize;
const { v4: uuidv4 } = require('uuid');

const User = sequelize.define('User', {
  ID: {
    type: DataTypes.UUID,
    defaultValue: DataTypes.UUIDV4,
    allowNull: false,
    primaryKey: true
  },
  ID_Auth: {
    type: DataTypes.STRING,
    allowNull: false
  },
  Name: {
    type: DataTypes.STRING,
    allowNull: false
  },
  Last_Name: {
    type: DataTypes.STRING,
    allowNull: false
  },
  Birthday: {
    type: DataTypes.DATEONLY,
    allowNull: false
  },
  Campus: {
    type: DataTypes.STRING,
    allowNull: false
  },
  Faculty: {
    type: DataTypes.STRING,
    allowNull: false
  },
  Career: {
    type: DataTypes.STRING,
    allowNull: false
  },
  MemberUN_Since: {
    type: DataTypes.INTEGER,
    allowNull: false
  },
  Phone_Number: {
    type: DataTypes.INTEGER,
    allowNull: false
  },
  Gender: {
    type: DataTypes.STRING,
    allowNull: false
  },
  Profile_Photo: {
    type: DataTypes.STRING,
    allowNull: false
  },
  myGroups: {
    type: DataTypes.ARRAY(DataTypes.STRING) // Suponiendo que este atributo es una lista de grupos a los que el usuario pertenece
  }
});

module.exports = User;