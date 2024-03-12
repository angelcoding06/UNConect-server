// Importa el modelo de friend
const Friendship = require('../models/friendsmodel');
const { sequelize } = require('sequelize'); // Importa el operador de Sequelize

// Función para enviar una solicitud de amistad
exports.sendFriendRequest = async (req, res, next) => {
  const { senderId, receiverId } = req.body; // Obtiene los IDs del remitente y el receptor

  try {
    // Crea una nueva solicitud de amistad en la base de datos
    const friendship = await Friendship.create({ senderId, receiverId });
    // Devuelve la solicitud creada como respuesta
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
    next(error); // Pasa cualquier error al siguiente middleware
  }
};

// Función para obtener los amigos de un usuario
exports.getFriends = async (req, res, next) => {
  const { userId } = req.params; // Obtiene el ID del usuario

  try {
    // Busca todas las solicitudes de amistad aceptadas donde el usuario es el remitente o el receptor
    const friends = await Friendship.findAll({
      where: {
        [sequelize.or]: [
          { senderId: userId, status: 'accepted' },
          { receiverId: userId, status: 'accepted' }
        ]
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
