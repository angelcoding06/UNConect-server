import { PartialType } from '@nestjs/swagger';
import { CreateLikeDto } from './create-like.dto';
import { ApiProperty } from '@nestjs/swagger';
import { IsEnum, IsNotEmpty } from 'class-validator';
import { TypeLike } from '../interfaces/likes.interface';

export class UpdateLikeDto extends PartialType(CreateLikeDto) {
  @ApiProperty()
  @IsNotEmpty()
  @IsEnum(TypeLike)
  type: TypeLike;
}
