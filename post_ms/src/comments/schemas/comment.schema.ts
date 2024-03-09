import { Prop, Schema, SchemaFactory } from '@nestjs/mongoose';
import { HydratedDocument } from 'mongoose';

import Icomment from '../interfaces/comments.interface';

export type LikesDocument = HydratedDocument<Comment>;

@Schema({
  collection: 'comments',
  timestamps: true,
  validateBeforeSave: true,
})
export class Comment implements Icomment {
  @Prop({ required: true, type: String })
  UserId: string;

  @Prop({ required: true, type: 'ObjectId', ref: 'Post' })
  PostId: string;

  @Prop({ required: true, type: String, maxlength: 1000 })
  Content: string;
}
export const CommentSchema = SchemaFactory.createForClass(Comment);
