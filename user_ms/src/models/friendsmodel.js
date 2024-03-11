const { DataTypes } = require('sequelize');
const sequelize = require('../database').sequelize;

const Friendship = sequelize.define('Friendship', {
  senderId: {
    type: DataTypes.INTEGER,
    allowNull: false
  },
  receiverId: {
    type: DataTypes.INTEGER,
    allowNull: false
  },
  status: {
    type: DataTypes.ENUM('pending', 'accepted'),
    allowNull: false,
    defaultValue: 'pending'
  }
});

module.exports = Friendship;