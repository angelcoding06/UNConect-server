import { HttpException, HttpStatus, Injectable } from '@nestjs/common';
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
    @InjectModel(Like.name) private likeModel: Model<Like>,
    private readonly PostsService: PostsService,
  ) {}

  async createLike(
    createLikeDto: CreateLikeDto,
    UserId: string,
    PostId: string,
  ) {
    const filter = { UserId: UserId, PostId: PostId };
    const postFound = await this.PostsService.getOnePost(PostId);
    if (!postFound) {
      throw new HttpException('Post not found', HttpStatus.NOT_FOUND);
    }
    const existingLike = await this.likeModel.findOne(filter);
    if (existingLike) {
      throw new HttpException(
        'Ya existe un like del usuario para este post',
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
        'No fue posible crear el like',
        HttpStatus.NOT_FOUND,
      );
    }
  }

  async getLikesbyPost(page: Query, PostId: string) {
    const filter = { PostId: PostId };
    const postFound = await this.PostsService.getOnePost(PostId);
    if (!postFound) {
      throw new HttpException('Post not found', HttpStatus.NOT_FOUND);
    }
    try {
      const likes = await paginate(this.likeModel, page, filter);
      if (likes.items.length === 0) {
        throw new HttpException(
          'No se encontraron likes de está publicación',
          HttpStatus.NOT_FOUND,
        );
      }
      return likes;
    } catch (error) {
      if (error instanceof HttpException) {
        throw error;
      } else {
        throw new HttpException(
          'Hubo un error al buscar los likes de esta publicación',
          HttpStatus.NOT_FOUND,
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
      throw new HttpException(
        'No se ha encontrado el Like',
        HttpStatus.NOT_FOUND,
      );
    }
    try {
      const updatedLike = Object.assign(likeFound[0], updateLikeDto);
      await this.likeModel.updateOne(filter, updatedLike);
      return updatedLike;
    } catch (error) {
      throw new HttpException(
        'No se ha podido modificar el Like',
        HttpStatus.NOT_FOUND,
      );
    }
  }

  async removeLike(UserId: string, PostId: string) {
    const filter = { UserId: UserId, PostId: PostId };
    const likeFound = await this.likeModel.find(filter);
    if (!likeFound[0]) {
      throw new HttpException(
        'No se ha encontrado el Like a eliminar',
        HttpStatus.NOT_FOUND,
      );
    }
    try {
      await this.likeModel.deleteOne(filter);
      return `El like el post con id ${PostId} dado por el usuario ${UserId} ha sido eliminado con éxito`;
    } catch (error) {
      if (error instanceof HttpException) {
        throw error;
      } else {
        throw new HttpException(
          'Hubo un error al buscar el like',
          HttpStatus.NOT_FOUND,
        );
      }
    }
  }
}
