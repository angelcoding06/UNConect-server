import {
  HttpException,
  HttpStatus,
  Inject,
  Injectable,
  forwardRef,
} from '@nestjs/common';
import { CreateCommentDto } from './dto/create-comment.dto';
import { UpdateCommentDto } from './dto/update-comment.dto';
import { InjectModel } from '@nestjs/mongoose';
import { Model } from 'mongoose';
// eslint-disable-next-line @typescript-eslint/no-unused-vars
import { PostsService } from 'src/posts/posts.service';
import { Comment } from './schemas/comment.schema';
import { Query } from 'express-serve-static-core';
import { paginate } from 'src/utils/paginate.utils';

@Injectable()
export class CommentsService {
  constructor(
    @InjectModel(Comment.name) private commentModel: Model<Comment>,
    @Inject(forwardRef(() => PostsService))
    private readonly postsService: PostsService,
  ) {}

  async createComment(
    createCommentDto: CreateCommentDto,
    UserId: string,
    PostId: string,
  ) {
    const postFound = await this.postsService.getOnePost(PostId);
    if (!postFound) {
      throw new HttpException(
        'No se encuentra el post al que quiere comentar',
        HttpStatus.NOT_FOUND,
      );
    }
    try {
      const createdComment = new this.commentModel(createCommentDto);
      createdComment.UserId = UserId;
      createdComment.PostId = PostId;
      return await createdComment.save();
    } catch (error) {
      throw new HttpException(
        'Hubo un error al crear el comentario',
        HttpStatus.INTERNAL_SERVER_ERROR,
      );
    }
  }

  async getCommentsbyPost(page: Query, PostId: string) {
    const filter = { PostId: PostId };
    const postFound = await this.postsService.getOnePost(PostId);
    console.log(postFound);
    if (!postFound) {
      throw new HttpException(
        'No se encontró el post del que quería obtener comentarios',
        HttpStatus.NOT_FOUND,
      );
    }

    try {
      const comments = await paginate(this.commentModel, page, filter);
      if (comments.items.length === 0) {
        throw new HttpException(
          'No se encontraron comments de está publicación',
          HttpStatus.NOT_FOUND,
        );
      }
      return comments;
    } catch (error) {
      if (error instanceof HttpException) {
        throw error;
      } else {
        throw new HttpException(
          'Hubo un error al buscar los comments de esta publicación',
          HttpStatus.INTERNAL_SERVER_ERROR,
        );
      }
    }
  }

  async updateComment(
    CommentId: string,
    PostId: string,
    updateCommentDto: UpdateCommentDto,
  ) {
    const postFound = await this.postsService.getOnePost(PostId);
    console.log(postFound, 'postfound');
    if (!postFound) {
      throw new HttpException(
        'No se encontró el post del que quería obtener comentarios',
        HttpStatus.NOT_FOUND,
      );
    }
    const filter = { _id: CommentId };
    const commentFound = await this.commentModel.find(filter);
    if (!commentFound[0]) {
      throw new HttpException(
        'No se ha encontrado el comentario',
        HttpStatus.NOT_FOUND,
      );
    }
    try {
      const updatedComment = Object.assign(commentFound[0], updateCommentDto);
      await this.commentModel.updateOne(filter, updatedComment);
      return updatedComment;
    } catch (error) {
      throw new HttpException(
        'Ha ocurrido un error al actualizar el comentario',
        HttpStatus.INTERNAL_SERVER_ERROR,
      );
    }
  }

  async removeComment(CommentId: string, PostId: string) {
    const filter = { _id: CommentId };
    const postFound = await this.postsService.getOnePost(PostId);
    console.log(postFound, 'postfound');
    if (!postFound) {
      throw new HttpException(
        'No se encontró el post del que quería obtener comentarios',
        HttpStatus.NOT_FOUND,
      );
    }
    const commentFound = await this.commentModel.find(filter);
    console.log(commentFound, 'commentFound');
    if (!commentFound[0]) {
      throw new HttpException(
        'No se ha encontrado el comentario a eliminar',
        HttpStatus.NOT_FOUND,
      );
    }
    try {
      await this.commentModel.deleteOne(filter);
      return `El comentario el con id ${CommentId} dado por el usuario  ha sido eliminado con éxito`;
    } catch (error) {
      if (error instanceof HttpException) {
        throw error;
      } else {
        throw new HttpException(
          'Hubo un error al eliminar el comentario',
          HttpStatus.INTERNAL_SERVER_ERROR,
        );
      }
    }
  }

  async deleteCommentsByPostId(postId: string) {
    try {
      await this.commentModel.deleteMany({ PostId: postId });
    } catch (error) {
      throw new HttpException(
        'No se han podido eliminar los comentarios del post',
        HttpStatus.INTERNAL_SERVER_ERROR,
      );
    }
  }
}
