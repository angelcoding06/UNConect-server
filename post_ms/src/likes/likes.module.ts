import { Module, forwardRef } from '@nestjs/common';
import { LikesService } from './likes.service';
import { LikesController } from './likes.controller';
import { MongooseModule } from '@nestjs/mongoose';
import { Like, LikeSchema } from './schemas/like.schema';
import { PostsModule } from 'src/posts/posts.module';

@Module({
  imports: [
    MongooseModule.forFeature([{ name: Like.name, schema: LikeSchema }]),
    forwardRef(() => PostsModule),
  ],
  controllers: [LikesController],
  providers: [LikesService],
  exports: [LikesService],
})
export class LikesModule {}
