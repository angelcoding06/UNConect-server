const { Sequelize } = require('sequelize');
require('dotenv').config();

const sequelize = new Sequelize('postgres://user:password@127.0.0.1:5432/usersdb');

module.exports = { sequelize };

