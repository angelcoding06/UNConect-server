import { ApiProperty } from '@nestjs/swagger';
import { IsNotEmpty, IsString, MaxLength } from 'class-validator';
export class CreateCommentDto {
  @ApiProperty({ required: true, maxLength: 1000, type: String })
  @IsNotEmpty()
  @IsString()
  @MaxLength(1000)
  Content: string;
}
