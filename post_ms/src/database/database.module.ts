import { Module } from '@nestjs/common';
import { ConfigModule, ConfigService } from '@nestjs/config';
import { MongooseModule } from '@nestjs/mongoose';

@Module({
  imports: [
    MongooseModule.forRootAsync({
      imports: [ConfigModule],
      useFactory: (configService: ConfigService) => {
        const uri = configService.get<string>('mongodb.uri');
        return {
          retryAttempts: 1,
          authSource: 'admin',
          uri: uri,
        };
      },
      inject: [ConfigService],
    }),
  ],
})
export class DatabaseModule {}
