import { Module } from '@nestjs/common';
import { AppController } from './app.controller';
import { AppService } from './app.service';
import { PostsModule } from './posts/posts.module';
import { DatabaseModule } from './database/database.module';

import { ConfigModule } from '@nestjs/config';
import { LikesModule } from './likes/likes.module';
import mongodbConfig from './shared/config/mongodb.config';
@Module({
  imports: [
    ConfigModule.forRoot({
      isGlobal: true,
      load: [mongodbConfig],
    }),
    DatabaseModule,
    PostsModule,
    LikesModule,
  ],
  controllers: [AppController],
  providers: [AppService],
})
export class AppModule {}
