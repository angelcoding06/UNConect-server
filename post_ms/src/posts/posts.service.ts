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
      console.log('createPost', createPost);
      return await createPost.save();
    } catch (error) {
      throw new HttpException(
        'No fue posible crear el post',
        HttpStatus.NOT_FOUND,
      );
    }
  }

  async getUserPosts(page: Query, UserId: string, GroupId?: string) {
    console.log('Group', GroupId);
    const filters = { UserId: UserId, GroupId: GroupId || null };
    console.log('filters', filters);
    try {
      const userPosts = await paginate(this.postModel, page, filters);
      if (userPosts.items.length === 0) {
        throw new HttpException(
          'No se encontraron post de este usuario',
          HttpStatus.NOT_FOUND,
        );
      }
      return userPosts;
    } catch (error) {
      throw new HttpException(
        'No se encontraron post de este usuario',
        HttpStatus.NOT_FOUND,
      );
    }
  }

  async getOnePost(PostId: string) {
    try {
      const post = await this.postModel.findById(PostId);
      if (!post) {
        throw new HttpException(
          //!take a look, it doesnt work
          'No se ha encontrado este post1',
          HttpStatus.NOT_FOUND,
        );
      }
      return post;
    } catch (error) {
      throw new HttpException(
        'No se ha encontrado este post',
        HttpStatus.NOT_FOUND,
      );
    }
  }

  async updatePost(PostId: string, updatePostDto: UpdatePostDto) {
    try {
      const postFound = await this.postModel.findById(PostId);
      const updatedPost = Object.assign(postFound, updatePostDto);
      await this.postModel.updateOne({ _id: PostId }, updatedPost);
      return updatedPost;
    } catch (error) {
      throw new HttpException(
        'No se ha podido modificar el post',
        HttpStatus.NOT_FOUND,
      );
    }
  }

  async getGroupPost(page: Query, GroupId: string) {
    const filter = { GroupId: GroupId };
    try {
      const groupPosts = await paginate(this.postModel, page, filter);

      return groupPosts;
    } catch (error) {
      throw new HttpException(
        'No se han encontrado post de este grupo',
        HttpStatus.NOT_FOUND,
      );
    }
  }

  async deletePost(PostId: string) {
    try {
      const postFound = await this.postModel.findById(PostId);
      if (!postFound) {
        //!take a look, it doesnt work
        throw new HttpException(
          'No se ha encontrado el post a eliminar',
          HttpStatus.NOT_FOUND,
        );
      }
      console.log('entro al try');
      await this.postModel.deleteOne({ _id: PostId });
      return `El post con id ${PostId} ha sido eliminado con éxito`;
    } catch (error) {
      throw new HttpException(
        'No se ha podido elimnar el post',
        HttpStatus.NOT_FOUND,
      );
    }
  }
}
