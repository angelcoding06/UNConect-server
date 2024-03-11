const express = require('express');
const friendsroutes = express.Router();

// Controladores para manejar las operaciones CRUD de usuarios
const FriendController = require('../controllers/friendscontroller');

// Ruta para obtener un usuario por su ID
friendsroutes.post('/friend-request', FriendController.sendFriendRequest);

// Ruta para obtener todos los usuarios 
friendsroutes.put('/friend/accept', FriendController.acceptRequest);

module.exports = friendsroutes

