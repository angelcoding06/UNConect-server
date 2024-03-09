import { ApiProperty } from '@nestjs/swagger';
import { IsEnum, IsNotEmpty } from 'class-validator';
import { TypeLike } from '../interfaces/likes.interface';
export class CreateLikeDto {
  @ApiProperty()
  @IsNotEmpty()
  @IsEnum(TypeLike)
  type: TypeLike;
}
