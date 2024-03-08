import {
  Controller,
  Get,
  Post,
  Body,
  Patch,
  Delete,
  Query,
  Headers,
} from '@nestjs/common';
import { PostsService } from './posts.service';
import { CreatePostDto } from './dto/create-post.dto';
import { UpdatePostDto } from './dto/update-post.dto';
import { Query as QueryType } from 'express-serve-static-core';
@Controller('posts')
export class PostsController {
  constructor(private readonly postsService: PostsService) {}

  @Post()
  create(
    @Body() createPostDto: CreatePostDto,
    @Headers('UserId') UserId: string,
    @Headers('GroupId') GroupId: string,
  ) {
    return this.postsService.createPost(createPostDto, UserId, GroupId);
  }

  @Get('userPost')
  getuserPosts(
    @Query('page') page: QueryType,
    @Headers('UserId') UserId: string,
  ) {
    return this.postsService.getUserPosts(page, UserId);
  }

  @Get('groupPost')
  getGroupPost(
    @Query('page') page: QueryType,
    @Headers('GroupId') GroupId: string,
  ) {
    return this.postsService.getGroupPost(page, GroupId);
  }

  @Get()
  getOnePost(@Headers('PostId') PostId: string) {
    return this.postsService.getOnePost(PostId);
  }

  @Patch()
  update(@Headers('PostId') id: string, @Body() updatePostDto: UpdatePostDto) {
    return this.postsService.updatePost(id, updatePostDto);
  }

  @Delete()
  remove(@Headers('PostId') id: string) {
    return this.postsService.deletePost(id);
  }
}
