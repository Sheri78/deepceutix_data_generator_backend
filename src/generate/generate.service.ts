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

  // ----------------- DEEPSEEK ----------------- DeepSeek R1 Qwen3-8B (free)
  async callDeepSeek(prompt: string): Promise<string> {
    const apiKey = process.env.DEEPSEEK_R1_API_KEY;
    const siteUrl = process.env.OPENROUTER_SITE_URL || ''; 
    const siteTitle = process.env.OPENROUTER_SITE_TITLE || ''; 

    const response = await axios.post(
      'https://openrouter.ai/api/v1/chat/completions',
      {
        model: 'deepseek/deepseek-r1-0528-qwen3-8b:free',
        messages: [{ role: 'user', content: prompt }],
        extra_body: {},
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

  // ----------------- LLAMA (via OpenRouter) -----------------
  async callLlama(prompt: string): Promise<string> {
    const apiKey = process.env.Llama_API_KEY;
    const siteUrl = process.env.OPENROUTER_SITE_URL || ''; 
    const siteTitle = process.env.OPENROUTER_SITE_TITLE || ''; 

    const response = await axios.post(
      'https://openrouter.ai/api/v1/chat/completions',
      {
        model: 'meta-llama/llama-3.3-70b-instruct:free',
        messages: [{ role: 'user', content: prompt }],
        extra_body: {},
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

  // ----------------- QWEN2.5 CODER (via OpenRouter) -----------------
  async callQwen(prompt: string): Promise<string> {
    const apiKey = process.env.QWEN2_5_VL_72B_API_KEY;
    const siteUrl = process.env.OPENROUTER_SITE_URL || '';
    const siteTitle = process.env.OPENROUTER_SITE_TITLE || '';

    const response = await axios.post(
      'https://openrouter.ai/api/v1/chat/completions',
      {
        model: 'qwen/qwen2.5-vl-72b-instruct:free',
        messages: [{ role: 'user', content: prompt }],
        extra_body: {},
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

    // Defensive: check for choices and message
    if (
      !response.data ||
      !Array.isArray(response.data.choices) ||
      !response.data.choices[0]?.message?.content
    ) {
      throw new Error(
        `Qwen3-Coder API error: ${JSON.stringify(response.data)}`
      );
    }

    return response.data.choices[0].message.content;
  }

  // ----------------- GPT-OSS-20B (via OpenRouter) -----------------
  async callGptOss20b(prompt: string): Promise<string> {
    const apiKey = process.env.GPT_OSS_20B_API_KEY;
    const siteUrl = process.env.OPENROUTER_SITE_URL || ''; 
    const siteTitle = process.env.OPENROUTER_SITE_TITLE || ''; 

    const response = await axios.post(
      'https://openrouter.ai/api/v1/chat/completions',
      {
        model: 'openai/gpt-oss-20b:free',
        messages: [{ role: 'user', content: prompt }],
        extra_body: {},
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

  async create(dto: CreateGenerateDto): Promise<GenerateResponseDto> {
    const { prompt, model } = dto;

    let rawText: string;
    const modelKey = model?.toLowerCase();

    if (modelKey === 'gemini') {
      rawText = await this.callGemini(prompt);
    } else if (modelKey === 'llama') {
      rawText = await this.callLlama(prompt);
    } else if (modelKey === 'deepseek') {
      rawText = await this.callDeepSeek(prompt);
    } else if (modelKey === 'qwen2.5') {
      rawText = await this.callQwen(prompt);
    } else if (modelKey === 'gpt-oss-20b') {
      rawText = await this.callGptOss20b(prompt);
    } else {
      throw new Error('Unsupported model');
    }

    return this.smartParse(rawText, model);
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
                cleanText = cleanText.replace(match, '');
              }
            } catch {
            }
          });
        }
      }
    } catch (e) {
      console.warn('Chart JSON parse failed, skipping.', e);
    }

    const tableRegex = /\|(.+\|)+\s*\n\s*\|[-:\s|]+\|\s*\n((?:\|.+\|\s*\n?)*)/g;
    let match;
    while ((match = tableRegex.exec(text)) !== null) {
      try {
        const tableText = match[0];
        const lines = tableText.trim().split('\n');
        
        if (lines.length >= 3) {
          const headers = lines[0].split('|').map((h) => h.trim()).filter(Boolean);
          const rows = lines
            .slice(2) 
            .filter(line => line.trim()) 
            .map((line) =>
              line.split('|').map((c) => c.trim()).filter(Boolean),
            );
          
          if (headers.length && rows.length) {
            (result.tables ??= []).push({ headers, rows }); 
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
      const codeMatch = codeMatches.find(match => 
        match.includes('matplotlib') || 
        match.includes('plt.') || 
        match.includes('import') ||
        !match.includes('{') 
      );
      
      if (codeMatch) {
        const code = codeMatch.replace(/```(?:python|py)?\s*/, '').replace(/\s*```/, '').trim();
        result.code = code;
        
        cleanText = cleanText.replace(codeMatch, '');

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
      .replace(/```[\s\S]*?```/g, '') 
      .replace(/\|(.+\|)+\s*\n\s*\|[-:\s|]+\|\s*\n((?:\|.+\|\s*\n?)*)/g, '') 
      .replace(/\{[\s\S]*?\}/g, '') 
      .replace(/^\s*[\r\n]/gm, '')
      .replace(/\n{3,}/g, '\n\n') 
      .trim();

    
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
      const tempDir = path.join(__dirname, '../../temp', Date.now().toString());
      await fs.promises.mkdir(tempDir, { recursive: true });
      
      const cleanedCode = this.cleanCodeForWindows(code);
      
      const modifiedCode = this.modifyCodeForExecution(cleanedCode, tempDir);
      
      const scriptPath = path.join(tempDir, 'script.py');
      await fs.promises.writeFile(scriptPath, modifiedCode, 'utf8');
      
      const pythonCommands = ['python', 'python3', 'py'];
      let result: { stdout: string; stderr: string } | undefined;
      let lastError = '';
      
      for (const cmd of pythonCommands) {
        try {
          console.log(`Trying Python command: ${cmd}`);
          
          const env = {
            ...process.env,
            PYTHONIOENCODING: 'utf-8',
            PYTHONLEGACYWINDOWSSTDIO: '1'
          };
          
          result = await execAsync(`${cmd} "${scriptPath}"`, {
            timeout: 30000,
            cwd: tempDir,
            env: env,
            encoding: 'utf8'
          });
          console.log(`Success with command: ${cmd}`);
          break;
        } catch (error: any) {
          lastError = error.message;
          console.log(`Failed with ${cmd}: ${error.message}`);
          continue;
        }
      }
      
      if (!result) {
        throw new Error(`All Python commands failed. Last error: ${lastError}`);
      }
      
      const { stdout, stderr } = result;
      
      const plotPath = path.join(tempDir, 'plot.png');
      const plotExists = await fs.promises.access(plotPath).then(() => true).catch(() => false);
      
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
      console.error('Python execution error:', error);
      return {
        success: false,
        error: `Python execution failed: ${error.message}`
      };
    }
  }

  //i have added  this new method to clean Unicode characters
  private cleanCodeForWindows(code: string): string {
    return code
      .replace(/⁻¹/g, '^-1')           
      .replace(/⁻/g, '-')              
      .replace(/¹/g, '1')              
      .replace(/²/g, '2')              
      .replace(/³/g, '3')              
      .replace(/°/g, ' degrees')       
      .replace(/μ/g, 'micro')         
      .replace(/α/g, 'alpha')  
      .replace(/β/g, 'beta')  
      .replace(/γ/g, 'gamma')  
      .replace(/δ/g, 'delta')  
      .replace(/λ/g, 'lambda')        
      .replace(/π/g, 'pi')             
      .replace(/σ/g, 'sigma')         
      .replace(/Δ/g, 'Delta')         
      .replace(/Ω/g, 'Omega')         
      .replace(/±/g, '+/-')            
      .replace(/×/g, 'x')              
      .replace(/÷/g, '/')            
      .replace(/≤/g, '<=')             
      .replace(/≥/g, '>=')            
      .replace(/≠/g, '!=')       
      .replace(/≈/g, '~=')             
      .replace(/∞/g, 'infinity')
  }

  private modifyCodeForExecution(originalCode: string, tempDir: string): string {
    let modifiedCode = originalCode;
    
    // Add encoding declaration at the top
    modifiedCode = `# -*- coding: utf-8 -*-
import sys
import os
# Set UTF-8 encoding for output
if sys.platform.startswith('win'):
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.detach())

` + modifiedCode;
    
    if (!modifiedCode.includes('import matplotlib.pyplot as plt')) {
      modifiedCode = 'import matplotlib.pyplot as plt\n' + modifiedCode;
    }
    if (!modifiedCode.includes('import numpy as np')) {
      modifiedCode = 'import numpy as np\n' + modifiedCode;
    }
    
    modifiedCode = modifiedCode.replace(
      'import matplotlib.pyplot as plt',
      `import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt`
    );
    
    const plotPath = path.join(tempDir, 'plot.png').replace(/\\/g, '/');
    modifiedCode = modifiedCode.replace(
      /plt\.show\(\)/g, 
      `plt.savefig('${plotPath}', dpi=150, bbox_inches='tight')
plt.close()  # Close the figure to free memory`
    );
    
    const dataPath = path.join(tempDir, 'data.json').replace(/\\/g, '/');
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
        with open('${dataPath}', 'w', encoding='utf-8') as f:
            json.dump(data_to_extract, f)
            
    print("Script executed successfully!")
except Exception as e:
    print(f"Note: Could not extract data - {e}")
`;
    
    return modifiedCode;
  }
}
