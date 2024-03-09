import { ApiProperty } from '@nestjs/swagger';
import { IsEnum, IsNotEmpty } from 'class-validator';
import { TypeLike } from '../interfaces/likes.interface';
export class CreateLikeDto {
  @ApiProperty({ enum: TypeLike, isArray: true, required: true })
  @IsNotEmpty()
  @IsEnum(TypeLike)
  type: TypeLike;
}
