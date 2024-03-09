import { registerAs } from '@nestjs/config';

export default registerAs('mongodb', () => {
  const {
    // MONGO_PORT,
    // MONGO_HOSTNAME,
    // MONGO_DATABASE,
    // MONGO_USERNAME,
    // MONGO_PASSWORD,
  } = process.env;
  // const uri = `mongodb://${MONGO_USERNAME}:${MONGO_PASSWORD}@${MONGO_HOSTNAME}:${MONGO_PORT}/${MONGO_DATABASE}?retryWrites=true&w=majority`;
  const uri = `mongodb://angel2:password@172.19.171.46/postsDB`;
  return { uri };
});
