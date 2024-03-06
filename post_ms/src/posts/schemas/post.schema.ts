import { Prop, Schema, SchemaFactory } from '@nestjs/mongoose';
import { HydratedDocument } from 'mongoose';
import Ipost from '../interfaces/post.interface';

export type PostDocument = HydratedDocument<Post>;

@Schema({
  collection: 'posts',
  timestamps: true,
  validateBeforeSave: true,
})
export class Post implements Ipost {
  @Prop({ required: true, type: String })
  UserId: string;

  @Prop({ required: false, type: String })
  GroupId?: string;

  @Prop({ type: String, required: true, maxlength: 1000 })
  Content: string;

  @Prop({
    type: [{ type: String }],
    required: false,
    validate: {
      validator: function (value: string[]) {
        return value.length <= 4;
      },
      message: 'El campo media no puede tener más de 4 elementos',
    },
  })
  Media?: string[];
}
export const PostSchema = SchemaFactory.createForClass(Post);
