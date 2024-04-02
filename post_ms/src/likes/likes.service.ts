import {
  HttpException,
  HttpStatus,
  Inject,
  Injectable,
  forwardRef,
} from '@nestjs/common';
import { CreateLikeDto } from './dto/create-like.dto';
import { UpdateLikeDto } from './dto/update-like.dto';
import { Like } from './schemas/like.schema';
import { Model } from 'mongoose';
import { InjectModel } from '@nestjs/mongoose';
import { paginate } from 'src/utils/paginate.utils';
import { Query } from 'express-serve-static-core';
// eslint-disable-next-line @typescript-eslint/no-unused-vars
import { PostsService } from 'src/posts/posts.service';

@Injectable()
export class LikesService {
  constructor(
    @InjectModel(Like.name)
    private likeModel: Model<Like>,
    @Inject(forwardRef(() => PostsService))
    private readonly postsService: PostsService,
  ) {}

  async createLike(
    createLikeDto: CreateLikeDto,
    UserId: string,
    PostId: string,
  ) {
    const filter = { UserId: UserId, PostId: PostId };
    const postFound = await this.postsService.getOnePost(PostId);
    if (!postFound) {
      throw new HttpException('Post not found', HttpStatus.NOT_FOUND);
    }
    const existingLike = await this.likeModel.findOne(filter);
    if (existingLike) {
      throw new HttpException(
        'There is already a like from the user for this post',
        HttpStatus.NOT_FOUND,
      );
    }
    try {
      const createLike = new this.likeModel(createLikeDto);
      createLike.UserId = UserId;
      createLike.PostId = PostId;
      return await createLike.save();
    } catch (error) {
      throw new HttpException(
        'It was not possible to create the like',
        HttpStatus.INTERNAL_SERVER_ERROR,
      );
    }
  }

  async getLikesbyPost(page: Query, PostId: string) {
    const filter = { PostId: PostId };
    const postFound = await this.postsService.getOnePost(PostId);
    if (!postFound) {
      throw new HttpException('Post not found', HttpStatus.NOT_FOUND);
    }
    try {
      const likes = await paginate(this.likeModel, page, filter);
      if (page > likes.totalPages) {
        throw new HttpException(
          'The page number requested is greater than the total number of pages',
          HttpStatus.NOT_FOUND,
        );
      }
      if (likes.items.length === 0) {
        throw new HttpException(
          'There were no likes found for this post',
          HttpStatus.NOT_FOUND,
        );
      }
      return likes;
    } catch (error) {
      if (error instanceof HttpException) {
        throw error;
      } else {
        throw new HttpException(
          'There was an error searching for the likes of this post',
          HttpStatus.INTERNAL_SERVER_ERROR,
        );
      }
    }
  }

  async updateLike(
    UserId: string,
    PostId: string,
    updateLikeDto: UpdateLikeDto,
  ) {
    const filter = { UserId: UserId, PostId: PostId };
    const likeFound = await this.likeModel.find(filter);
    // We have to use [0] because the result is an array with one element
    // Meanwhile findbyId gives us an object, find gives us an array
    if (!likeFound[0]) {
      throw new HttpException('Like to update not found', HttpStatus.NOT_FOUND);
    }
    try {
      const updatedLike = Object.assign(likeFound[0], updateLikeDto);
      await this.likeModel.updateOne(filter, updatedLike);
      return updatedLike;
    } catch (error) {
      throw new HttpException(
        'There was an error modifying the like',
        HttpStatus.INTERNAL_SERVER_ERROR,
      );
    }
  }

  async removeLike(UserId: string, PostId: string) {
    const filter = { UserId: UserId, PostId: PostId };
    const likeFound = await this.likeModel.find(filter);
    if (!likeFound[0]) {
      throw new HttpException('Like to delete not found', HttpStatus.NOT_FOUND);
    }
    try {
      await this.likeModel.deleteOne(filter);
      return `The like on the post with id ${PostId} given by the user ${UserId} has been successfully deleted`;
    } catch (error) {
      if (error instanceof HttpException) {
        throw error;
      } else {
        throw new HttpException(
          'There was an error searching for the like',
          HttpStatus.INTERNAL_SERVER_ERROR,
        );
      }
    }
  }

  async deleteLikesByPostId(postId: string) {
    try {
      await this.likeModel.deleteMany({ PostId: postId });
    } catch (error) {
      throw new HttpException(
        'There was an error deleting the post likes',
        HttpStatus.INTERNAL_SERVER_ERROR,
      );
    }
  }
}
