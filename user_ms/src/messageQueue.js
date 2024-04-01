// messageQueue.js
const amqp = require('amqplib');
const { createUser } = require('./controllers/usercontroller');
let user_const = {
	"ID_Auth": "",
	"Name": "",
	"Last_Name": "",
	"Birthday": "1995-03-08",
	"Campus": "Bogotá",
	"Faculty": "INGENIERÍA",
	"Career": "Ingeniería Civil",
	"MemberUN_Since": 2000,
	"Phone_Number": "+573000000000",
	"Gender": "Masculino",
	"Profile_Photo": "",
	"myGroups": []
}

async function consumeQueue() {
	
	console.log("antes de la conexion");
	const connection = await amqp.connect('amqp://rabbitmq:5672');
	console.log('Connected to RabbitMQ', connection);
	const channel = await connection.createChannel();
	const queue = 'user-queue';

	await channel.assertQueue(queue, { durable: true });
	console.log('Waiting for messages in queue...');

	channel.consume(queue, async (message) => {
		
		console.log(`Received message: ${message.content.toString()}`);

		// Parsear el mensaje JSON
		const data = JSON.parse(message.content.toString());
		const id = data.ID_Auth;
		// Llamar a la función createUser con los datos del mensaje
		try {
			await createUser({
				"ID_Auth": id,
				"Name": "",
				"Last_Name": "",
				"Birthday": "1995-03-08",
				"Campus": "Bogotá",
				"Faculty": "INGENIERÍA",
				"Career": "Ingeniería Civil",
				"MemberUN_Since": 2000,
				"Phone_Number": "+573000000000",
				"Gender": "Masculino",
				"Profile_Photo": "",
				"myGroups": []
			});
		} catch (error) {
			console.error("Error al crear usuario:", error);
		}

	}, { noAck: true });
}

module.exports = { consumeQueue };
