// Importa el modelo de friend
const Friendship = require('../models/friendsmodel');

exports.sendFriendRequest = async (req, res, next) => {
    const { senderId, receiverId } = req.body;
  
    try {
      const friendship = await Friendship.create({ senderId, receiverId });
      res.status(201).json(friendship);
    } catch (error) {
      next(error);
    }
  };
  
exports.acceptRequest = async (req, res, next) => {
    const { senderId, receiverId } = req.body;
  
    try {
      // Verificar si existe una entrada en la tabla Friendship con los IDs proporcionados
      const friendship = await Friendship.findOne({
        where: {
          senderId,
          receiverId
        }
      });
  
      if (!friendship) {
        return res.status(404).json({ error: 'Friendship request not found' });
      }
  
      // Actualizar el estado de la solicitud a 'accepted'
      await friendship.update({ status: 'accepted' });
  
      // Enviar la respuesta
      res.status(200).json({ message: 'Friendship request accepted successfully' });
    } catch (error) {
      next(error);
    }
  };