import { Injectable } from '@nestjs/common';
import axios from 'axios';

@Injectable()
export class QwenService {
  async callModel(prompt: string): Promise<string> {
    const apiKey = process.env.QWEN2_5_VL_72B_API_KEY;
    const siteUrl = process.env.OPENROUTER_SITE_URL || '';
    const siteTitle = process.env.OPENROUTER_SITE_TITLE || '';

    const response = await axios.post(
      'https://openrouter.ai/api/v1/chat/completions',
      {
        model: 'qwen/qwen2.5-vl-72b-instruct:free',
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

    if (!response.data.choices?.[0]?.message?.content) {
      throw new Error(`Qwen API error: ${JSON.stringify(response.data)}`);
    }

    return response.data.choices[0].message.content;
  }
}
