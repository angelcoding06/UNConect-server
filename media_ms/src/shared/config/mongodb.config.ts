import { registerAs } from '@nestjs/config';

export default registerAs('mongodb', () => {
  const {
    MONGO_PORT_MEDIA,
    MONGO_HOSTNAME_MEDIA,
    MONGO_DATABASE_MEDIA,
    MONGO_USERNAME_MEDIA,
    MONGO_PASSWORD_MEDIA,
  } = process.env;
  const uri = `mongodb://${MONGO_USERNAME_MEDIA}:${MONGO_PASSWORD_MEDIA}@${MONGO_HOSTNAME_MEDIA}:${MONGO_PORT_MEDIA}/${MONGO_DATABASE_MEDIA}?retryWrites=true&w=majority`;
  // const uri = 'mongodb://mediauser:password@localhost:27018/mediaDB';
  return { uri };
});
