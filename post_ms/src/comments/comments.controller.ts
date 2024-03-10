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
import { CommentsService } from './comments.service';
import { CreateCommentDto } from './dto/create-comment.dto';
import { UpdateCommentDto } from './dto/update-comment.dto';
import { ApiTags } from '@nestjs/swagger';
import { Query as QueryType } from 'express-serve-static-core';

@ApiTags('Comments')
@Controller('comments')
export class CommentsController {
  constructor(private readonly commentsService: CommentsService) {}

  @Post()
  createComment(
    @Body() createCommentDto: CreateCommentDto,
    @Headers('UserId') UserId: string,
    @Headers('PostId') PostId: string,
  ) {
    return this.commentsService.createComment(createCommentDto, UserId, PostId);
  }

  @Get()
  findAll(@Headers('PostId') PostId: string, @Query('page') page: QueryType) {
    return this.commentsService.getCommentsbyPost(page, PostId);
  }

  @Patch()
  update(
    @Headers('CommentId') CommentId: string,
    @Headers('PostId') PostId: string,
    @Body() updateCommentDto: UpdateCommentDto,
  ) {
    return this.commentsService.updateComment(
      CommentId,
      PostId,
      updateCommentDto,
    );
  }

  @Delete()
  async remove(
    @Headers('CommentId') CommentId: string,
    @Headers('PostId') PostId: string,
  ) {
    return await this.commentsService.removeComment(CommentId, PostId);
  }
}
