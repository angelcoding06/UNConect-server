import { Prop, Schema, SchemaFactory } from '@nestjs/mongoose';
import { HydratedDocument } from 'mongoose';
import Imedia from '../interfaces/media.interface';

export enum FileTypes {
  JPG = 'image/jpeg',
  VIDEO = 'video/mp4',
  PNG = 'image/png',
  OCTE = 'application/octet-stream',
}

export type MediaDocument = HydratedDocument<Media>;

@Schema({
  collection: 'media',
  timestamps: true,
  validateBeforeSave: true,
})
export class Media implements Imedia {
  @Prop({ required: true, type: String })
  UserId: string;

  @Prop({ required: false, type: String })
  GroupId?: string;

  @Prop({ required: false, type: 'ObjectId' })
  PostId?: string;

  @Prop({ type: String, required: true })
  Path: string;

  @Prop({ enum: FileTypes, required: true })
  Type: FileTypes;
}
export const MediaSchema = SchemaFactory.createForClass(Media);
