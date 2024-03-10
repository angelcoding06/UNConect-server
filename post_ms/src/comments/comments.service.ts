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
        'The post from which you wanted to get comments was not found',
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
        'There was an error creating the comment',
        HttpStatus.INTERNAL_SERVER_ERROR,
      );
    }
  }

  async getCommentsbyPost(page: Query, PostId: string) {
    const filter = { PostId: PostId };
    const postFound = await this.postsService.getOnePost(PostId);
    if (!postFound) {
      throw new HttpException(
        'The post from which you wanted to get comments was not found',
        HttpStatus.NOT_FOUND,
      );
    }

    try {
      const comments = await paginate(this.commentModel, page, filter);
      if (comments.items.length === 0) {
        throw new HttpException(
          'There were no comments found for this post',
          HttpStatus.NOT_FOUND,
        );
      }
      return comments;
    } catch (error) {
      if (error instanceof HttpException) {
        throw error;
      } else {
        throw new HttpException(
          'There was an error searching for the comments of this post',
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
    if (!postFound) {
      throw new HttpException(
        'The post from which you wanted to get comments was not found',
        HttpStatus.NOT_FOUND,
      );
    }
    const filter = { _id: CommentId };
    const commentFound = await this.commentModel.find(filter);
    if (!commentFound[0]) {
      throw new HttpException(
        'The comment to update was not found',
        HttpStatus.NOT_FOUND,
      );
    }
    try {
      const updatedComment = Object.assign(commentFound[0], updateCommentDto);
      await this.commentModel.updateOne(filter, updatedComment);
      return updatedComment;
    } catch (error) {
      throw new HttpException(
        'There was an error updating the comment',
        HttpStatus.INTERNAL_SERVER_ERROR,
      );
    }
  }

  async removeComment(CommentId: string, PostId: string) {
    const filter = { _id: CommentId };
    const postFound = await this.postsService.getOnePost(PostId);
    if (!postFound) {
      throw new HttpException(
        'The post from which you wanted to get comments was not found',
        HttpStatus.NOT_FOUND,
      );
    }
    const commentFound = await this.commentModel.find(filter);
    if (!commentFound[0]) {
      throw new HttpException(
        'The comment to delete was not found',
        HttpStatus.NOT_FOUND,
      );
    }
    try {
      await this.commentModel.deleteOne(filter);
      return `The comment with id ${CommentId} given by the user has been successfully deleted`;
    } catch (error) {
      if (error instanceof HttpException) {
        throw error;
      } else {
        throw new HttpException(
          'There was an error deleting the comment',
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
        'There was an error deleting the comments of the post',
        HttpStatus.INTERNAL_SERVER_ERROR,
      );
    }
  }
}
