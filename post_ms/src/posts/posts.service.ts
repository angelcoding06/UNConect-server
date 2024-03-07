import { Model } from 'mongoose';
import { Injectable } from '@nestjs/common';
import { InjectModel } from '@nestjs/mongoose';
import { CreatePostDto } from './dto/create-post.dto';
import { UpdatePostDto } from './dto/update-post.dto';
import { Post } from './schemas/post.schema';
import { Query } from 'express-serve-static-core';
@Injectable()
export class PostsService {
  constructor(@InjectModel(Post.name) private postModel: Model<Post>) {}

  async createPost(createPostDto: CreatePostDto): Promise<Post> {
    const createPost = new this.postModel(createPostDto);
    return createPost.save();
  }

  async getUserPosts(query: Query): Promise<Post[]> {
    //todo implement ID search
    const responsePerPage = 9;
    const currentPage = Number(query.page) || 1;
    const skip = responsePerPage * (currentPage - 1);

    const posts = await this.postModel.find().limit(responsePerPage).skip(skip);

    return posts;
  }

  getOnePost(id: number) {
    return `This action returns a #${id} post`;
  }

  updatePost(id: number, updatePostDto: UpdatePostDto) {
    return `This action updates a #${id} post`;
  }

  getGroupPost(id: number) {
    return `This action returns a #${id} post`;
  }

  deletePost(id: number) {
    return `This action removes a #${id} post`;
  }
}
