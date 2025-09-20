import { Injectable } from '@nestjs/common';
import { GenerateResponseDto } from './dto/generate-response.dto';

@Injectable()
export class ParserService {
  parse(text: string, label: string): GenerateResponseDto {
    const result: GenerateResponseDto = {
      chart: null,
      tables: [],
      code: null,
      explanation: null,
    };

    let cleanText = text;

    // --- JSON CHART ---
    try {
      const jsonMatches = text.match(/```json\s*([\s\S]*?)\s*```/g);
      if (jsonMatches) {
        jsonMatches.forEach((match) => {
          try {
            const jsonContent = match.replace(/```json\s*/, '').replace(/\s*```/, '');
            const parsed = JSON.parse(jsonContent);
            if (parsed.x && parsed.y) {
              result.chart = {
                x: parsed.x.map(Number),
                y: parsed.y.map(Number),
                label: parsed.label || label,
              };
              cleanText = cleanText.replace(match, '');
            }
          } catch {}
        });
      }
    } catch {}

    // --- TABLES ---
    const tableRegex = /\|(.+\|)+\s*\n\s*\|[-:\s|]+\|\s*\n((?:\|.+\|\s*\n?)*)/g;
    let match;
    while ((match = tableRegex.exec(text)) !== null) {
      const tableText = match[0];
      const lines = tableText.trim().split('\n');
      if (lines.length >= 3) {
        const headers = lines[0].split('|').map((h) => h.trim()).filter(Boolean);
        const rows = lines.slice(2).map((line) =>
          line.split('|').map((c) => c.trim()).filter(Boolean),
        );
        (result.tables ??= []).push({ headers, rows });
        cleanText = cleanText.replace(tableText, '');
      }
    }

    // --- CODE BLOCK ---
    const codeMatches = text.match(/```(?:python|py)?\s*([\s\S]*?)\s*```/g);
    if (codeMatches) {
      const code = codeMatches[0]
        .replace(/```(?:python|py)?\s*/, '')
        .replace(/\s*```/, '')
        .trim();
      result.code = code;
      cleanText = cleanText.replace(codeMatches[0], '');
    }

    // --- EXPLANATION ---
    result.explanation = cleanText
      .replace(/```[\s\S]*?```/g, '')
      .replace(/\|(.+\|)+\s*\n\s*\|[-:\s|]+\|\s*\n((?:\|.+\|\s*\n?)*)/g, '')
      .replace(/\{[\s\S]*?\}/g, '')
      .trim();

    return result;
  }
}
