import { Model } from 'mongoose';
import { HttpException, HttpStatus, Injectable } from '@nestjs/common';
import { InjectModel } from '@nestjs/mongoose';
import { CreatePostDto } from './dto/create-post.dto';
import { UpdatePostDto } from './dto/update-post.dto';
import { Post } from './schemas/post.schema';
import { Query } from 'express-serve-static-core';
import { paginate } from 'src/utils/paginate.utils';
@Injectable()
export class PostsService {
  constructor(@InjectModel(Post.name) private postModel: Model<Post>) {}
  // TODO
  // Ver las publicaciones de mis amigos
  // Buscar las publicaciones por una query o por texto
  // Buscar las publicaciones que tengan foto / video

  async createPost(
    createPostDto: CreatePostDto,
    UserId: string,
    GroupId: string,
  ): Promise<Post> {
    try {
      const createPost = new this.postModel(createPostDto);
      createPost.UserId = UserId;
      if (GroupId) {
        createPost.GroupId = GroupId;
      }
      return await createPost.save();
    } catch (error) {
      throw new HttpException(
        'No fue posible crear el post',
        HttpStatus.INTERNAL_SERVER_ERROR,
      );
    }
  }

  async getUserPosts(page: Query, UserId: string, GroupId?: string) {
    const filters = { UserId: UserId, GroupId: GroupId || null };
    try {
      const userPosts = await paginate(this.postModel, page, filters);
      if (userPosts.items.length === 0) {
        throw new HttpException(
          'No se encontraron posts de este usuario',
          HttpStatus.NOT_FOUND,
        );
      }
      return userPosts;
    } catch (error) {
      if (error instanceof HttpException) {
        throw error;
      } else {
        throw new HttpException(
          'Hubo un error al buscar los post del usuario',
          HttpStatus.INTERNAL_SERVER_ERROR,
        );
      }
    }
  }

  async getOnePost(PostId: string) {
    // const postFound = await this.postModel.find({ _id: PostId });
    // console.log('Post found desde getonepost ', postFound);
    try {
      const postFound = await this.postModel.find({ _id: PostId });
      console.log('Post found desde getonepost ', postFound);
      if (postFound.length === 0) {
        throw new HttpException(
          'No se ha encontrado este post',
          HttpStatus.NOT_FOUND,
        );
      }
      return postFound;
    } catch (error) {
      console.log('Error desde getonepost ', error);
      if (error instanceof HttpException) {
        throw error;
      } else if (error.name == 'CastError') {
        throw new HttpException(
          'El id del post no es válido',
          HttpStatus.NOT_FOUND,
        );
      } else {
        throw new HttpException(
          'Hubo un error al buscar el post',
          HttpStatus.INTERNAL_SERVER_ERROR,
        );
      }
    }
  }

  async updatePost(PostId: string, updatePostDto: UpdatePostDto) {
    const postFound = await this.postModel.findById(PostId);
    if (!postFound) {
      throw new HttpException(
        'No se ha encontrado el Post a modificar',
        HttpStatus.NOT_FOUND,
      );
    }
    try {
      const updatedPost = Object.assign(postFound, updatePostDto);
      await this.postModel.updateOne({ _id: PostId }, updatedPost);
      return updatedPost;
    } catch (error) {
      throw new HttpException(
        'Hubo un error modificando el post',
        HttpStatus.INTERNAL_SERVER_ERROR,
      );
    }
  }

  async getGroupPost(page: Query, GroupId: string) {
    const filter = { GroupId: GroupId };
    try {
      const groupPosts = await paginate(this.postModel, page, filter);
      if (groupPosts.items.length === 0) {
        throw new HttpException(
          'No se encontraron posts de este grupo',
          HttpStatus.NOT_FOUND,
        );
      }
      return groupPosts;
    } catch (error) {
      if (error instanceof HttpException) {
        throw error;
      } else {
        throw new HttpException(
          'Hubo un error al buscar los posts del grupo',
          HttpStatus.INTERNAL_SERVER_ERROR,
        );
      }
    }
  }

  async deletePost(PostId: string) {
    const postFound = await this.postModel.findById(PostId);
    if (!postFound) {
      throw new HttpException(
        'No se ha encontrado el post a eliminar',
        HttpStatus.NOT_FOUND,
      );
    }
    try {
      //todo Eliminar comentarios y likes asociados antes de eliminar el post
      // await this.commentService.deleteCommentsByPostId(PostId);
      // await this.likesService.deleteLikesByPostId(PostId);
      await this.postModel.deleteOne({ _id: PostId });
      return `El post con id ${PostId} ha sido eliminado con éxito`;
    } catch (error) {
      throw new HttpException(
        'No se ha podido elimnar el post',
        HttpStatus.INTERNAL_SERVER_ERROR,
      );
    }
  }
}
