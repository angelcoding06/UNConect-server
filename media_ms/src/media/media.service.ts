import { HttpException, HttpStatus, Injectable } from '@nestjs/common';
import { join } from 'path';
import { InjectModel } from '@nestjs/mongoose';
import { Media } from './schemas/media.schema';
import { Model } from 'mongoose';
import { unlink } from 'fs';

@Injectable()
export class MediaService {
  constructor(
    @InjectModel(Media.name)
    private mediaModel: Model<Media>,
  ) {}

  async createMedia(files: Express.Multer.File[], UserId: string) {
    const createdMediaIds = [];
    if (!files || files.length === 0) {
      throw new HttpException('No files received', HttpStatus.BAD_REQUEST);
    }
    const paths = files.map(
      (file) => join(process.cwd(), 'uploads', file.filename), // The path to the uploaded file.
    );
    for (let i = 0; i < files.length; i++) {
      const file = files[i];
      const fileType = file.mimetype;
      console.log('file:', file.mimetype);

      const media = new this.mediaModel({
        UserId: UserId,
        Path: paths[i],
        Type: fileType,
      });
      const savedMedia = await media.save();
      createdMediaIds.push(savedMedia._id);
    }

    return createdMediaIds;
  }

  async getFileById(id: string) {
    try {
      const file = await this.mediaModel.findById(id);
      if (!file) {
        throw new HttpException('File not found', HttpStatus.NOT_FOUND);
      }
      return file;
    } catch (error) {
      if (error instanceof HttpException) {
        throw error;
      }
      throw new HttpException('File not found', HttpStatus.NOT_FOUND);
    }
  }

  async deleteMediaById(id: string) {
    try {
      const fileFound = await this.mediaModel.find({ _id: id });
      const filepath = fileFound[0].Path;
      console.log('fileFound:', fileFound);
      if (!fileFound) {
        throw new HttpException('File not found', HttpStatus.NOT_FOUND);
      }
      try {
        unlink(filepath, (err) => {
          if (err) throw err;
          console.log('path/file.txt was deleted');
        });
        await this.mediaModel.findByIdAndDelete(id);
        return 'File deleted';
      } catch (error) {
        console.error('Error al eliminar el archivo:', error);
        throw error;
      }
    } catch (error) {}
  }
}
