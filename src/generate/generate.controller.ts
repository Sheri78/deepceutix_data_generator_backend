import { Body, Controller, Get, Param, Post, Res } from '@nestjs/common';
import { GenerateService } from './generate.service';
import { CreateGenerateDto } from './dto/create-generate.dto';
import path from 'path';
import type { Response } from 'express';

@Controller('generate')
export class GenerateController {
  constructor(private readonly generateService: GenerateService) {}

  @Post()
  async create(@Body() dto: CreateGenerateDto) {
    return this.generateService.create(dto);
  }

  @Post('execute-python')
  async executePython(@Body() dto: { code: string }) {
    return this.generateService.executePython(dto.code);
  }

  @Get('temp-image/:folder/:filename')
  async getTempImage(
    @Param('folder') folder: string,
    @Param('filename') filename: string,
    @Res() res: Response
  ) {
    const imagePath = path.join(__dirname, '../../temp', folder, filename);
    return res.sendFile(imagePath);
  }
}
