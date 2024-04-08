const express = require('express');
const friendsroutes = express.Router(); // Crea un enrutador para las rutas de amigos

// Importa los controladores para manejar las operaciones CRUD de amigos
const FriendController = require('../controllers/friendscontroller');

// Define las rutas para las operaciones relacionadas con amigos

// Ruta para enviar una solicitud de amistad
friendsroutes.post('/', FriendController.sendFriendRequest);

// Ruta para aceptar una solicitud de amistad
friendsroutes.put('/accept', FriendController.acceptRequest);

// Ruta para rechazar una solicitud de amistad
friendsroutes.put('/reject', FriendController.rejectRequest);

// Ruta para obtener la lista de amigos de un usuario
friendsroutes.get('/:userId', FriendController.getFriends);

friendsroutes.get('/userfriendships/:userId', FriendController.getUserFriendships);

// Ruta para obtener la lista de amigos de un usuario
friendsroutes.delete('/:friendshipId', FriendController.deleteFriend);

module.exports = friendsroutes; // Exporta las rutas de amigos para su uso en otros archivos
