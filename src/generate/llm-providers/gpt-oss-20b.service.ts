import { Injectable } from '@nestjs/common';
import axios from 'axios';

@Injectable()
export class GptOss20bService {
  async callModel(prompt: string): Promise<string> {
    const apiKey = process.env.GPT_OSS_20B_API_KEY;
    const siteUrl = process.env.OPENROUTER_SITE_URL || '';
    const siteTitle = process.env.OPENROUTER_SITE_TITLE || '';

    const response = await axios.post(
      'https://openrouter.ai/api/v1/chat/completions',
      {
        model: 'openai/gpt-oss-20b:free',
        messages: [{ role: 'user', content: prompt }],
      },
      {
        headers: {
          Authorization: `Bearer ${apiKey}`,
          'Content-Type': 'application/json',
          ...(siteUrl && { 'HTTP-Referer': siteUrl }),
          ...(siteTitle && { 'X-Title': siteTitle }),
        },
      },
    );

    return response.data.choices[0].message.content;
  }
}
