import { Injectable } from '@nestjs/common';
import axios from 'axios';

@Injectable()
export class GeminiService {
  async callModel(prompt: string): Promise<string> {
    const apiKey = process.env.GEMINI_API_KEY;
    const url = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=${apiKey}`;

    const response = await axios.post(url, {
      contents: [{ parts: [{ text: prompt }] }],
    });

    return response.data.candidates[0].content.parts[0].text;
  }
}
