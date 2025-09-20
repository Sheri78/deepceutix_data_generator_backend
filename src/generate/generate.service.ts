import { Injectable } from '@nestjs/common';
import { CreateGenerateDto } from './dto/create-generate.dto';
import { GenerateResponseDto } from './dto/generate-response.dto';

// Model providers
import { GeminiService } from './llm-providers/gemini.service';
import { ClaudeService } from './llm-providers/claude.service';
import { LlamaService } from './llm-providers/llama.service';
import { DeepSeekService } from './llm-providers/deepseek.service';
import { QwenService } from './llm-providers/qwen.service';
import { GptOss20bService } from './llm-providers/gpt-oss-20b.service';

// Utilities
import { ParserService } from './parser.service';
import { PythonExecutorService } from './python-executor.service';

@Injectable()
export class GenerateService {
  constructor(
    private readonly gemini: GeminiService,
    private readonly claude: ClaudeService,
    private readonly llama: LlamaService,
    private readonly deepseek: DeepSeekService,
    private readonly qwen: QwenService,
    private readonly gptOss20b: GptOss20bService,
    private readonly parser: ParserService,
    private readonly pythonExecutor: PythonExecutorService,
  ) {}

  /**
   * Main entrypoint — generates response using selected LLM
   */
  async create(dto: CreateGenerateDto): Promise<GenerateResponseDto> {
    const { prompt, model } = dto;

    if (!model) {
      throw new Error('Model name must be provided');
    }

    let rawText: string;

    switch (model.toLowerCase()) {
      case 'gemini':
        rawText = await this.gemini.callModel(prompt);
        break;
      case 'claude':
        rawText = await this.claude.callModel(prompt);
        break;
      case 'llama':
        rawText = await this.llama.callModel(prompt);
        break;
      case 'deepseek':
        rawText = await this.deepseek.callModel(prompt);
        break;
      case 'qwen':
        rawText = await this.qwen.callModel(prompt);
        break;
      case 'gpt-oss-20b':
        rawText = await this.gptOss20b.callModel(prompt);
        break;
      default:
        throw new Error(`Unsupported model: ${model}`);
    }

    // Parse response into structured format
    return this.parser.parse(rawText, model);
  }

  /**
   * Expose Python execution (for charts, code, etc.)
   */
  async executePython(code: string) {
    return this.pythonExecutor.execute(code);
  }
}
