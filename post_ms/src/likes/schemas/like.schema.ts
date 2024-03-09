import { Prop, Schema, SchemaFactory } from '@nestjs/mongoose';
import { HydratedDocument } from 'mongoose';
import { TypeLike } from '../interfaces/likes.interface';
import Ilike from '../interfaces/likes.interface';

export type LikesDocument = HydratedDocument<Like>;

@Schema({
  collection: 'likes',
  timestamps: true,
  validateBeforeSave: true,
})
export class Like implements Ilike {
  @Prop({ required: true, type: String })
  UserId: string;

  @Prop({ required: true, type: String, unique: true })
  PostId: string;

  @Prop({ type: TypeLike, required: true })
  type: TypeLike;
}
export const LikeSchema = SchemaFactory.createForClass(Like);
