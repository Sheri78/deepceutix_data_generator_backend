import { Module } from '@nestjs/common';
import { GenerateController } from './generate.controller';
import { GenerateService } from './generate.service';
import { GeminiService } from './llm-providers/gemini.service';
import { ClaudeService } from './llm-providers/claude.service';
import { DeepSeekService } from './llm-providers/deepseek.service';
import { LlamaService } from './llm-providers/llama.service';
import { QwenService } from './llm-providers/qwen.service';
import { GptOss20bService } from './llm-providers/gpt-oss-20b.service';
import { ParserService } from './parser.service';
import { PythonExecutorService } from './python-executor.service';

@Module({
  controllers: [GenerateController],  
  providers: [
    GenerateService,
    GeminiService,
    ClaudeService,
    DeepSeekService,
    LlamaService,
    QwenService,
    GptOss20bService,
    ParserService,
    PythonExecutorService,
  ],
  exports: [GenerateService],
})
export class GenerateModule {}
