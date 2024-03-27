import { Model } from 'mongoose';
import {
  HttpException,
  HttpStatus,
  Inject,
  Injectable,
  forwardRef,
} from '@nestjs/common';
import { InjectModel } from '@nestjs/mongoose';
import { CreatePostDto } from './dto/create-post.dto';
import { UpdatePostDto } from './dto/update-post.dto';
import { Post } from './schemas/post.schema';
import { Query } from 'express-serve-static-core';
import { paginate } from 'src/utils/paginate.utils';
import { LikesService } from 'src/likes/likes.service';
import { CommentsService } from 'src/comments/comments.service';
@Injectable()
export class PostsService {
  constructor(
    @InjectModel(Post.name) private postModel: Model<Post>,
    @Inject(forwardRef(() => LikesService)) private likesService: LikesService,
    @Inject(forwardRef(() => CommentsService))
    private commentsService: CommentsService,
  ) {}
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
        'It was not possible to create the post',
        HttpStatus.INTERNAL_SERVER_ERROR,
      );
    }
  }

  async getUserPosts(page: Query, UserId: string, GroupId?: string) {
    const filters = { UserId: UserId, GroupId: GroupId || null };
    try {
      const userPosts = await paginate(this.postModel, page, filters);
      if (page > userPosts.totalPages) {
        throw new HttpException(
          'The page number requested is greater than the total number of pages',
          HttpStatus.NOT_FOUND,
        );
      }
      if (userPosts.items.length === 0) {
        throw new HttpException(
          'No posts were found for this user',
          HttpStatus.NOT_FOUND,
        );
      }
      return userPosts;
    } catch (error) {
      if (error instanceof HttpException) {
        throw error;
      } else {
        throw new HttpException(
          `There was an error searching for the user's posts`,
          HttpStatus.INTERNAL_SERVER_ERROR,
        );
      }
    }
  }

  async getOnePost(PostId: string) {
    try {
      const postFound = await this.postModel.find({ _id: PostId });
      if (postFound.length === 0) {
        throw new HttpException(
          'This post was not found',
          HttpStatus.NOT_FOUND,
        );
      }
      return postFound;
    } catch (error) {
      if (error instanceof HttpException) {
        throw error;
      } else if (error.name == 'CastError') {
        throw new HttpException(
          'The post id is not valid',
          HttpStatus.NOT_FOUND,
        );
      } else {
        throw new HttpException(
          'There was an error searching for the post',
          HttpStatus.INTERNAL_SERVER_ERROR,
        );
      }
    }
  }

  async updatePost(PostId: string, updatePostDto: UpdatePostDto) {
    const postFound = await this.postModel.findById(PostId);
    if (!postFound) {
      throw new HttpException(
        'The post to modify was not found',
        HttpStatus.NOT_FOUND,
      );
    }
    try {
      const updatedPost = Object.assign(postFound, updatePostDto);
      await this.postModel.updateOne({ _id: PostId }, updatedPost);
      return updatedPost;
    } catch (error) {
      throw new HttpException(
        'There was an error modifying the post',
        HttpStatus.INTERNAL_SERVER_ERROR,
      );
    }
  }

  async getGroupPost(page: Query, GroupId: string) {
    const filter = { GroupId: GroupId };
    try {
      const groupPosts = await paginate(this.postModel, page, filter);
      if (page > groupPosts.totalPages && groupPosts.totalPages !== 0) {
        throw new HttpException(
          'The page number requested is greater than the total number of pages',
          HttpStatus.NOT_FOUND,
        );
      }
      if (groupPosts.items.length === 0) {
        throw new HttpException(
          'No posts found for this group',
          HttpStatus.NOT_FOUND,
        );
      }
      return groupPosts;
    } catch (error) {
      if (error instanceof HttpException) {
        throw error;
      } else {
        throw new HttpException(
          'An error occurred while searching for the group posts',
          HttpStatus.INTERNAL_SERVER_ERROR,
        );
      }
    }
  }

  async deletePost(PostId: string): Promise<string> {
    const postFound = await this.postModel.findById(PostId);
    if (!postFound) {
      throw new HttpException(
        'The post to delete was not found',
        HttpStatus.NOT_FOUND,
      );
    }
    try {
      // Delete all likes and comments related to the post
      await this.commentsService.deleteCommentsByPostId(PostId);
      await this.likesService.deleteLikesByPostId(PostId);
      await this.postModel.deleteOne({ _id: PostId });
      return `The post with id ${PostId} has been deleted successfully`;
    } catch (error) {
      throw new HttpException(
        'The post could not be deleted, an unknown error occurred',
        HttpStatus.INTERNAL_SERVER_ERROR,
      );
    }
  }
}
