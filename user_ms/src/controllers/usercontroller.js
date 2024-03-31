// Importa el modelo de usuario
const User = require('../models/usermodel');

// Controlador para obtener todos los usuarios
exports.getAllUsers = async (req, res, next) => {
  try {
    // Busca todos los usuarios en la base de datos
    const users = await User.findAll();
    // Devuelve todos los usuarios encontrados
    res.json(users);
  } catch (error) {
    console.error("Error en getAllUsers:", error);
    next(error); // Pasa cualquier error al siguiente middleware
  }
};

// Controlador para obtener un usuario por su ID
exports.getUserById = async (req, res, next) => {
  const { id } = req.params; // Obtiene el ID del usuario desde los parámetros de la solicitud
  try {
    // Busca un usuario por su ID en la base de datos
    const user = await User.findByPk(id);
    // Si no se encuentra el usuario, devuelve un error
    if (!user) {
      return res.status(404).json({ error: 'User not found' });
    }
    // Devuelve el usuario encontrado
    res.json(user);
  } catch (error) {
    console.error("Error en getUserById:", error);
    next(error); // Pasa cualquier error al siguiente middleware
  }
};

// Controlador para crear un nuevo usuario
exports.createUser = async (req, res, next) => {
  try {
    // Extrae los campos del cuerpo de la solicitud
    const { ID_Auth, Name, Last_Name, Birthday, Campus, Faculty, Career, MemberUN_Since, Phone_Number, Gender, Profile_Photo, myGroups } = req.body;
    console.log(req.body)
    console.log("ID_Auth: ", ID_Auth)
    console.log("Name: ", Name)
    console.log("Last_Name: ", Last_Name)
    console.log("Birthday: ", Birthday)
    console.log("Campus: ", Campus)
    console.log("Faculty: ", Faculty)
    console.log("Career: ", Career)
    console.log("MemberUN_Since: ", MemberUN_Since)
    console.log("Phone_Number: ", Phone_Number)
    console.log("GENDER: ", Gender )
    console.log("Profile_Photo: ", Profile_Photo)
    console.log("myGroups: ", myGroups)

    // Crea un nuevo usuario con los campos proporcionados
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

    // Envia la respuesta con el nuevo usuario creado
    res.status(201).json(newUser);
  } catch (error) {
    console.error("Error en createUser:", error);
    next(error); // Pasa cualquier error al siguiente middleware
  }
};

// Controlador para actualizar un usuario existente
exports.updateUser = async (req, res, next) => {
  const { id } = req.params; // Obtiene el ID del usuario desde los parámetros de la solicitud
  try {
    // Busca el usuario por su ID
    const user = await User.findByPk(id);
    
    // Si no se encuentra el usuario, devuelve un error
    if (!user) {
      return res.status(404).json({ error: 'User not found' });
    }

    // Actualiza el usuario con los datos proporcionados en el cuerpo de la solicitud
    await user.update(req.body);

    // Envia la respuesta con el usuario actualizado
    res.json(user);
  } catch (error) {
    console.error("Error en updateUser:", error);
    next(error); // Pasa cualquier error al siguiente middleware
  }
};

// Controlador para eliminar un usuario
exports.deleteUser = async (req, res, next) => {
  const { id } = req.params; // Obtiene el ID del usuario desde los parámetros de la solicitud
  try {
    // Busca el usuario por su ID
    const user = await User.findByPk(id);
    // Si no se encuentra el usuario, devuelve un error
    if (!user) {
      return res.status(404).json({ error: 'User not found' });
    }
    // Elimina el usuario de la base de datos
    await user.destroy();
    // Devuelve un mensaje de éxito
    res.json({ message: 'User deleted successfully' });
  } catch (error) {
    console.error("Error en deleteUser:", error);
    next(error); // Pasa cualquier error al siguiente middleware
  }
};
