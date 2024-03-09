import { Injectable } from '@nestjs/common';
import { CreateLikeDto } from './dto/create-like.dto';
import { UpdateLikeDto } from './dto/update-like.dto';
import { Like } from './schemas/like.schema';
import { Model } from 'mongoose';
import { InjectModel } from '@nestjs/mongoose';

@Injectable()
export class LikesService {
  constructor(@InjectModel(Like.name) private postModel: Model<Like>) {}
  create(createLikeDto: CreateLikeDto) {
    return 'This action adds a new like';
  }

  findAll() {
    return `This action returns all likes`;
  }

  findOne(id: number) {
    return `This action returns a #${id} like`;
  }

  update(id: number, updateLikeDto: UpdateLikeDto) {
    return `This action updates a #${id} like`;
  }

  remove(id: number) {
    return `This action removes a #${id} like`;
  }
}
