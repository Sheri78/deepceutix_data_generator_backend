import { Injectable } from '@nestjs/common';
import axios from 'axios';

@Injectable()
export class ClaudeService {
  async callModel(prompt: string): Promise<string> {
    const apiKey = process.env.ANTHROPIC_API_KEY;
    const response = await axios.post(
      'https://api.anthropic.com/v1/messages',
      {
        model: 'claude-3-opus-20240229',
        max_tokens: 1000,
        messages: [{ role: 'user', content: prompt }],
      },
      {
        headers: {
          'x-api-key': apiKey,
          'content-type': 'application/json',
          'anthropic-version': '2023-06-01',
        },
      },
    );

    return response.data.content[0].text;
  }
}
