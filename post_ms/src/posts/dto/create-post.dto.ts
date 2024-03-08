import { ApiProperty } from '@nestjs/swagger';
import { IsArray, IsNotEmpty, IsOptional, IsString } from 'class-validator';
export class CreatePostDto {
  @ApiProperty()
  @IsNotEmpty()
  @IsString()
  Content: string;

  @ApiProperty()
  @IsArray()
  @IsOptional()
  Media?: string[];
}
