const express = require('express');
const userroutes = express.Router();

// Controladores para manejar las operaciones CRUD de usuarios
const UserController = require('../controllers/usercontroller');

// Ruta para obtener todos los usuarios
userroutes.get('/', UserController.getAllUsers);

// Ruta para obtener un usuario por su ID
userroutes.get('/:id', UserController.getUserById);

// Ruta para crear un nuevo usuario
userroutes.post('/', UserController.createUser);

// Ruta para actualizar un usuario existente
userroutes.put('/:id', UserController.updateUser);

// Ruta para eliminar un usuario
userroutes.delete('/:id', UserController.deleteUser);

module.exports = userroutes;
