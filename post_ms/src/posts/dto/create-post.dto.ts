import { ApiProperty } from '@nestjs/swagger';
import { IsArray, IsNotEmpty, IsString } from 'class-validator';
export class CreatePostDto {
  @ApiProperty()
  @IsNotEmpty()
  @IsString()
  Content: string;

  @ApiProperty()
  @IsArray()
  Media?: string[];
}
