// Importa el modelo de usuario
const User = require('../models/usermodel');

// Controlador para obtener todos los usuarios
exports.getAllUsers = async (req, res, next) => {
  try {
    const users = await User.findAll();
    res.json(users);
  } catch (error) {
    next(error);
  }
};

// Controlador para obtener un usuario por su ID
exports.getUserById = async (req, res, next) => {
  const { id } = req.params;
  try {
    const user = await User.findByPk(id);
    if (!user) {
      return res.status(404).json({ error: 'User not found' });
    }
    res.json(user);
  } catch (error) {
    next(error);
  }
};

// Controlador para crear un nuevo usuario
exports.createUser = async (req, res, next) => {
    try {
        // Extraer los campos del cuerpo de la solicitud
        const { ID_Auth, Name, Last_Name, Birthday, Campus, Faculty, Career, MemberUN_Since, Phone_Number, Gender, Profile_Photo, myGroups } = req.body;

        console.log('Datos recibidos para crear usuario:', {
            ID_Auth,
            Name,
            Last_Name,
            Birthday,
            Campus,
            Faculty,
            Career,
            MemberUN_Since,
            Phone_Number,
            Gender,
            Profile_Photo,
            myGroups
          });
        
        // Crear un nuevo usuario con los campos proporcionados
        const newUser = await User.create({ 
          ID_Auth, 
          Name, 
          Last_Name, 
          Birthday, 
          Campus, 
          Faculty, 
          Career, 
          MemberUN_Since, 
          Phone_Number, 
          Gender, 
          Profile_Photo, 
          myGroups 
        });
    
        // Enviar la respuesta con el nuevo usuario creado
        res.status(201).json(newUser);
      } catch (error) {
        // Pasar el error al siguiente middleware de manejo de errores
        next(error);
      }
    };

// Controlador para actualizar un usuario existente
exports.updateUser = async (req, res, next) => {
    const { id } = req.params;
    try {
      // Buscar el usuario por su ID
      const user = await User.findByPk(id);
      
      // Verificar si el usuario existe
      if (!user) {
        return res.status(404).json({ error: 'User not found' });
      }
  
      // Actualizar el usuario con los datos proporcionados en el cuerpo de la solicitud
      await user.update(req.body);
  
      // Enviar la respuesta con el usuario actualizado
      res.json(user);
    } catch (error) {
      // Pasar el error al siguiente middleware de manejo de errores
      next(error);
    }
  };

// Controlador para eliminar un usuario
exports.deleteUser = async (req, res, next) => {
  const { id } = req.params;
  try {
    const user = await User.findByPk(id);
    if (!user) {
      return res.status(404).json({ error: 'User not found' });
    }
    await user.destroy();
    res.json({ message: 'User deleted successfully' });
  } catch (error) {
    next(error);
  }
};
