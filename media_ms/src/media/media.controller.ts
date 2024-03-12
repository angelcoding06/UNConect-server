import {
  Controller,
  Get,
  Post,
  Param,
  Delete,
  UploadedFiles,
  UseInterceptors,
  Res,
  Headers,
  HttpException,
  HttpStatus,
} from '@nestjs/common';
import { MediaService } from './media.service';
import { FilesInterceptor } from '@nestjs/platform-express';
import { diskStorage } from 'multer';
import { createReadStream } from 'fs';
import type { Response } from 'express';
import { FileTypes } from './schemas/media.schema';
import { ApiBody, ApiConsumes, ApiTags } from '@nestjs/swagger';

@ApiTags('Media')
@Controller('media')
export class MediaController {
  constructor(private readonly mediaService: MediaService) {}

  @ApiConsumes('multipart/form-data')
  @ApiBody({
    schema: {
      type: 'object',
      properties: {
        media: {
          type: 'string',
          format: 'binary',
        },
      },
    },
  })
  @Post('file')
  @UseInterceptors(
    FilesInterceptor('files', 4, {
      storage: diskStorage({
        destination: './uploads',
        filename: (req, file, cb) => {
          const UserId = req.headers.userid;
          const timestamp = Date.now();
          const filename = `${UserId}_${timestamp}_${file.originalname}`;
          // Callback to determine the name of the uploaded file.
          cb(null, filename);
        },
      }),
    }),
  )
  uploadFile(
    @UploadedFiles() files: Express.Multer.File[],
    @Headers('UserId') UserId: string,
  ) {
    return this.mediaService.createMedia(files, UserId);
  }

  @Get(':id')
  async get(
    @Param('id') id: string,
    @Headers('Type') Type: string,
    @Res() res: Response,
  ) {
    const file = await this.mediaService.getFileById(id);
    if (!file) {
      throw new HttpException('File not found', HttpStatus.NOT_FOUND);
    }
    switch (file.Type) {
      case FileTypes.JPG:
        res.set({
          'Content-Type': 'image/jpeg',
        });
        break;
      case FileTypes.VIDEO:
        res.set({
          'Content-Type': 'video/mp4',
        });
        break;
      case FileTypes.PNG:
        res.set({
          'Content-Type': 'image/png',
        });
        break;
      default:
        throw new HttpException('Invalid file type', HttpStatus.BAD_REQUEST);
    }

    const stream = createReadStream(file.Path);
    stream.pipe(res);
  }

  @Delete(':id')
  async delete(@Param('id') id: string) {
    return this.mediaService.deleteMediaById(id);
  }
}
