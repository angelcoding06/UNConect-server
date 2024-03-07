import {
  Controller,
  Get,
  Post,
  Body,
  Patch,
  Param,
  Delete,
  Query,
} from '@nestjs/common';
import { PostsService } from './posts.service';
import { CreatePostDto } from './dto/create-post.dto';
import { UpdatePostDto } from './dto/update-post.dto';
import { Query as QueryType } from 'express-serve-static-core';

@Controller('posts')
export class PostsController {
  constructor(private readonly postsService: PostsService) {}

  @Post()
  create(@Body() createPostDto: CreatePostDto) {
    return this.postsService.createPost(createPostDto);
  }

  @Get(':id/userPosts')
  getuserPosts(@Query('page') page: QueryType) {
    return this.postsService.getUserPosts(page);
  }
  @Get()
  getGroupPost(@Query('page') page: QueryType, @Param('id') id: string) {
    return this.postsService.getGroupPost(page);
  }

  @Get(':id')
  getOnePost(@Param('id') id: string) {
    return this.postsService.getOnePost(+id);
  }

  @Patch(':id')
  update(@Param('id') id: string, @Body() updatePostDto: UpdatePostDto) {
    return this.postsService.updatePost(+id, updatePostDto);
  }

  @Delete(':id')
  remove(@Param('id') id: string) {
    return this.postsService.deletePost(+id);
  }
}
