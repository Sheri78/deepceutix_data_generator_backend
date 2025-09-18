import { Injectable } from '@nestjs/common';
import { CreateGenerateDto } from './dto/create-generate.dto';
import axios from 'axios';
import { GenerateResponseDto } from './dto/generate-response.dto';
import { exec } from 'child_process';
import { promisify } from 'util';
import * as fs from 'fs';
import * as path from 'path';

const execAsync = promisify(exec);

@Injectable()
export class GenerateService {
  async create(dto: CreateGenerateDto): Promise<GenerateResponseDto> {
    const { prompt, model } = dto;

    let rawText: string;

    if (model === 'Gemini') {
      rawText = await this.callGemini(prompt);
    } else if (model === 'Claude') {
      rawText = await this.callClaude(prompt);
    } else if (model === 'DeepSeek') {
      rawText = await this.callDeepSeek(prompt);
    } else {
      throw new Error('Unsupported model');
    }

    // Parse into structured response
    return this.smartParse(rawText, model);
  }

  // ----------------- GEMINI -----------------
  async callGemini(prompt: string): Promise<string> {
    const apiKey = process.env.GEMINI_API_KEY;
    const url = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=${apiKey}`;

    const response = await axios.post(url, {
      contents: [{ parts: [{ text: prompt }] }],
    });

    return response.data.candidates[0].content.parts[0].text;
  }

  // ----------------- CLAUDE -----------------
  async callClaude(prompt: string): Promise<string> {
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

  // ----------------- DEEPSEEK (via OpenAI-style fallback) -----------------
  async callDeepSeek(prompt: string): Promise<string> {
    const apiKey = process.env.OPENAI_API_KEY;
    const response = await axios.post(
      'https://api.openai.com/v1/chat/completions',
      {
        model: 'gpt-3.5-turbo',
        messages: [{ role: 'user', content: prompt }],
        max_tokens: 600,
      },
      {
        headers: {
          Authorization: `Bearer ${apiKey}`,
          'Content-Type': 'application/json',
        },
      },
    );

    return response.data.choices[0].message.content;
  }

  // ----------------- SMART PARSER -----------------
  smartParse(text: string, label: string): GenerateResponseDto {
    const result: GenerateResponseDto = {
      chart: null,
      tables: [],
      code: null,
      explanation: null,
    };

    let cleanText = text;

    // 1. Try to extract JSON chart(s)
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
              // Remove this JSON block from clean text
              cleanText = cleanText.replace(match, '');
            }
          } catch (e) {
            console.warn('Failed to parse JSON chart:', e);
          }
        });
      }

      // Fallback: try to find JSON without code blocks
      if (!result.chart) {
        const jsonMatches = text.match(/\{[\s\S]*?\}/g);
        if (jsonMatches) {
          jsonMatches.forEach((match) => {
            try {
              const parsed = JSON.parse(match);
              if (parsed.x && parsed.y) {
                result.chart = {
                  x: parsed.x.map(Number),
                  y: parsed.y.map(Number),
                  label: parsed.label || label,
                };
                // Remove this JSON from clean text
                cleanText = cleanText.replace(match, '');
              }
            } catch {
              // ignore if not valid JSON
            }
          });
        }
      }
    } catch (e) {
      console.warn('⚠️ Chart JSON parse failed, skipping.', e);
    }

    // 2. Try to extract tables (markdown-style)
    const tableRegex = /\|(.+\|)+\s*\n\s*\|[-:\s|]+\|\s*\n((?:\|.+\|\s*\n?)*)/g;
    let match;
    while ((match = tableRegex.exec(text)) !== null) {
      try {
        const tableText = match[0];
        const lines = tableText.trim().split('\n');
        
        if (lines.length >= 3) {
          const headers = lines[0].split('|').map((h) => h.trim()).filter(Boolean);
          const rows = lines
            .slice(2) // Skip header and separator
            .filter(line => line.trim()) // Remove empty lines
            .map((line) =>
              line.split('|').map((c) => c.trim()).filter(Boolean),
            );
          
          if (headers.length && rows.length) {
            (result.tables ??= []).push({ headers, rows }); // Ensure tables is always an array
            // Remove this table from clean text
            cleanText = cleanText.replace(tableText, '');
          }
        }
      } catch (e) {
        console.warn('Failed to parse table:', e);
      }
    }

    // 3. Extract code blocks
    const codeMatches = text.match(/```(?:python|py)?\s*([\s\S]*?)\s*```/g);
    if (codeMatches) {
      // Take the first Python code block
      const codeMatch = codeMatches.find(match => 
        match.includes('matplotlib') || 
        match.includes('plt.') || 
        match.includes('import') ||
        !match.includes('{') // Avoid JSON blocks
      );
      
      if (codeMatch) {
        const code = codeMatch.replace(/```(?:python|py)?\s*/, '').replace(/\s*```/, '').trim();
        result.code = code;
        
        // Remove code blocks from clean text
        cleanText = cleanText.replace(codeMatch, '');

        // Try to extract x and y arrays from code if no chart found yet
        if (!result.chart) {
          const xMatch = code.match(/x\s*=\s*```math\s*([^`]+)```/);
          const yMatch = code.match(/y\s*=\s*```math\s*([^`]+)```/);

          if (xMatch && yMatch) {
            try {
              const xVals = xMatch[1].split(',').map((n) => Number(n.trim()));
              const yVals = yMatch[1].split(',').map((n) => Number(n.trim()));
              if (xVals.length === yVals.length && xVals.length > 0) {
                result.chart = { x: xVals, y: yVals, label };
              }
            } catch (e) {
              console.warn('Failed to extract x,y from code:', e);
            }
          }
        }
      }
    }

    // 4. Clean explanation (remove extracted content)
    result.explanation = cleanText
      .replace(/```[\s\S]*?```/g, '') // Remove any remaining code blocks
      .replace(/\|(.+\|)+\s*\n\s*\|[-:\s|]+\|\s*\n((?:\|.+\|\s*\n?)*)/g, '') // Remove any remaining tables
      .replace(/\{[\s\S]*?\}/g, '') // Remove any remaining JSON
      .replace(/^\s*[\r\n]/gm, '') // Remove empty lines
      .replace(/\n{3,}/g, '\n\n') // Replace multiple newlines with double newlines
      .trim();

    // If explanation is too short or empty, use original text
    if (!result.explanation || result.explanation.length < 50) {
      result.explanation = text;
    }

    return result;
  }

  async executePythonCode(code: string): Promise<{
    success: boolean;
    output?: string;
    error?: string;
    imagePath?: string;
    data?: any;
  }> {
    try {
      // Create a temporary directory for this execution
      const tempDir = path.join(__dirname, '../../temp', Date.now().toString());
      await fs.promises.mkdir(tempDir, { recursive: true });
      
      // Modify the code to save plots and capture data
      const modifiedCode = this.modifyCodeForExecution(code, tempDir);
      
      // Write the code to a temporary file
      const scriptPath = path.join(tempDir, 'script.py');
      await fs.promises.writeFile(scriptPath, modifiedCode);
      
      // Execute the Python script
      const { stdout, stderr } = await execAsync(`python ${scriptPath}`, {
        timeout: 30000, // 30 second timeout
        cwd: tempDir
      });
      
      // Check for generated plot
      const plotPath = path.join(tempDir, 'plot.png');
      const plotExists = await fs.promises.access(plotPath).then(() => true).catch(() => false);
      
      // Check for generated data
      const dataPath = path.join(tempDir, 'data.json');
      let extractedData = null;
      try {
        if (await fs.promises.access(dataPath).then(() => true).catch(() => false)) {
          const dataContent = await fs.promises.readFile(dataPath, 'utf-8');
          extractedData = JSON.parse(dataContent);
        }
      } catch (e) {
        console.warn('Could not read extracted data:', e);
      }
      
      return {
        success: true,
        output: stdout,
        error: stderr || undefined,
        imagePath: plotExists ? `/api/temp-image/${path.basename(tempDir)}/plot.png` : undefined,
        data: extractedData
      };
      
    } catch (error: any) {
      return {
        success: false,
        error: error.message
      };
    }
  }

  private modifyCodeForExecution(originalCode: string, tempDir: string): string {
    let modifiedCode = originalCode;
    
    // Add necessary imports if not present
    if (!modifiedCode.includes('import matplotlib.pyplot as plt')) {
      modifiedCode = 'import matplotlib.pyplot as plt\n' + modifiedCode;
    }
    if (!modifiedCode.includes('import numpy as np')) {
      modifiedCode = 'import numpy as np\n' + modifiedCode;
    }
    
    // Replace plt.show() with plt.savefig()
    modifiedCode = modifiedCode.replace(
      /plt\.show\(\)/g, 
      `plt.savefig('${path.join(tempDir, 'plot.png').replace(/\\/g, '/')}', dpi=150, bbox_inches='tight')`
    );
    
    // Add code to extract data if possible
    modifiedCode += `

# Try to extract data for frontend
import json
try:
    # Look for common variable names that might contain plot data
    data_to_extract = {}
    
    # Check for common variable names
    if 'wavenumber' in locals() and 'absorbance_formulation' in locals():
        data_to_extract = {
            'x': wavenumber.tolist() if hasattr(wavenumber, 'tolist') else list(wavenumber),
            'y': absorbance_formulation.tolist() if hasattr(absorbance_formulation, 'tolist') else list(absorbance_formulation)
        }
    elif 'x' in locals() and 'y' in locals():
        data_to_extract = {
            'x': x.tolist() if hasattr(x, 'tolist') else list(x),
            'y': y.tolist() if hasattr(y, 'tolist') else list(y)
        }
    
    if data_to_extract:
        with open('${path.join(tempDir, 'data.json').replace(/\\/g, '/')}', 'w') as f:
            json.dump(data_to_extract, f)
except Exception as e:
    print(f"Could not extract data: {e}")
`;
  
    return modifiedCode;
  }
}
