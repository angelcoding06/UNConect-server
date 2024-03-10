import {
  Controller,
  Get,
  Post,
  Body,
  Patch,
  Delete,
  Headers,
  Query,
} from '@nestjs/common';
import { LikesService } from './likes.service';
import { CreateLikeDto } from './dto/create-like.dto';
import { UpdateLikeDto } from './dto/update-like.dto';
import { Query as QueryType } from 'express-serve-static-core';
import { ApiTags } from '@nestjs/swagger';
@ApiTags('Likes')
@Controller('likes')
export class LikesController {
  constructor(private readonly likesService: LikesService) {}

  @Post()
  async create(
    @Body() createLikeDto: CreateLikeDto,
    @Headers('UserId') UserId: string,
    @Headers('PostId') PostId: string,
  ) {
    return await this.likesService.createLike(createLikeDto, UserId, PostId);
  }

  @Get()
  async getLikesbyPost(
    @Query('page') page: QueryType,
    @Headers('PostId') PostId: string,
  ) {
    return await this.likesService.getLikesbyPost(page, PostId);
  }

  @Patch()
  async update(
    @Body() updateLikeDto: UpdateLikeDto,
    @Headers('UserId') UserId: string,
    @Headers('PostId') PostId: string,
  ) {
    return await this.likesService.updateLike(UserId, PostId, updateLikeDto);
  }

  @Delete()
  async remove(
    @Headers('UserId') UserId: string,
    @Headers('PostId') PostId: string,
  ) {
    return await this.likesService.removeLike(UserId, PostId);
  }
}
