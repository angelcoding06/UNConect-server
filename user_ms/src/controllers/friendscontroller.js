// Importa el modelo de friend
const Friendship = require('../models/friendsmodel');
const sequelize = require('../database').sequelize;// Importa el operador de Sequelize
const { Sequelize } = require('sequelize');

// Función para enviar una solicitud de amistad
exports.sendFriendRequest = async (req, res, next) => {
  const { senderId, receiverId } = req.body; // Obtiene los IDs del remitente y el receptor

  try {
    // Crea una nueva solicitud de amistad en la base de datos
    const friendship = await Friendship.create({ senderId, receiverId });
    // Devuelve la solicitud creada como respuesta
    console.log(friendship);
    res.status(201).json(friendship);
  } catch (error) {
    console.error("Error en sendFriendRequest:", error);
    next(error); // Pasa cualquier error al siguiente middleware
  }
};

// Función para aceptar una solicitud de amistad
exports.acceptRequest = async (req, res, next) => {
  const { senderId, receiverId } = req.body; // Obtiene los IDs del remitente y el receptor

  try {
    // Busca la solicitud de amistad en la base de datos
    const friendship = await Friendship.findOne({
      where: {
        senderId,
        receiverId
      }
    });

    // Si no se encuentra la solicitud, devuelve un error
    if (!friendship) {
      return res.status(404).json({ error: 'Friendship request not found' });
    }

    // Actualiza el estado de la solicitud a 'accepted'
    await friendship.update({ status: 'accepted' });

    // Devuelve un mensaje de éxito
    res.status(200).json({ message: 'Friendship request accepted successfully' });
  } catch (error) {
    console.error("Error en acceptRequest:", error);
    next(error); // Pasa cualquier error al siguiente middleware
  }
};

// Función para rechazar una solicitud de amistad
exports.rejectRequest = async (req, res, next) => {
  const { senderId, receiverId } = req.body; // Obtiene los IDs del remitente y el receptor

  try {
    // Busca la solicitud de amistad en la base de datos
    const friendship = await Friendship.findOne({
      where: {
        senderId,
        receiverId
      }
    });

    // Si no se encuentra la solicitud, devuelve un error
    if (!friendship) {
      return res.status(404).json({ error: 'Friendship request not found' });
    }

    // Elimina la solicitud de amistad de la base de datos
    await friendship.destroy();

    // Devuelve un mensaje de éxito
    res.status(200).json({ message: 'Friendship request rejected and deleted successfully' });
  } catch (error) {
    console.error("Error en rejectRequest:", error);
    next(error); // Pasa cualquier error al sfiguiente middleware
  }
};

// Función para obtener los amigos de un usuario
exports.getFriends = async (req, res, next) => {
  const { userId } = req.params; // Obtiene el ID del usuario
  console.log(userId);
  

  try{
    // Busca todas las solicitudes de amistad aceptadas donde el usuario es el remitente o el receptor
    const friends = await Friendship.findAll({
      where: {
        [Sequelize.Op.or]: [
          { senderId: userId },
          { receiverId: userId }
        ],
        status: 'accepted',
      }
    });

    // Obtiene los IDs de los amigos
    const friendIds = friends.map(friendship => {
      return friendship.senderId === userId ? friendship.receiverId : friendship.senderId;
    });

    // Devuelve los IDs de los amigos como respuesta
    res.status(200).json({ friendIds });
  } catch (error) {
    console.error("Error en getFriends:", error);
    next(error); // Pasa cualquier error al siguiente middleware
  }
};

exports.deleteFriend = async (req, res, next) => {
  const { friendshipId } = req.params; // Obtener el ID de la amistad a eliminar
  
  try {
    // Buscar la amistad por su ID
    const friendship = await Friendship.findByPk(friendshipId);
    
    // Verificar si la amistad existe
    if (!friendship) {
      return res.status(404).json({ message: 'La amistad no existe' });
    }
    
    // Eliminar la amistad
    await friendship.destroy();
    
    // Respuesta exitosa
    res.status(200).json({ message: 'Amistad eliminada exitosamente' });
  } catch (error) {
    console.error("Error al eliminar la amistad:", error);
    next(error); // Pasa cualquier error al siguiente middleware
  }
};

exports.getUserFriendships = async (req, res, next) => {
  const { userId } = req.params; 
  
  try {
    // Buscar todas las amistades del usuario
    const friendships = await Friendship.findAll({
      where: {
        [Sequelize.Op.or]: [
          { senderId: userId },
          { receiverId: userId }
        ]
      }
    });
    
    // Respuesta exitosa
    res.status(200).json({ friendships });
  } catch (error) {
    console.error("Error al obtener las amistades del usuario:", error);
    next(error); // Pasa cualquier error al siguiente middleware
  }
}
