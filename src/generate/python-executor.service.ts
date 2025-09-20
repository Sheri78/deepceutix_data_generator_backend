import { Injectable } from '@nestjs/common';
import { exec } from 'child_process';
import { promisify } from 'util';
import * as fs from 'fs';
import * as path from 'path';

const execAsync = promisify(exec);

@Injectable()
export class PythonExecutorService {
  
  async execute(code: string) {
    const tempDir = path.join(__dirname, '../../temp');
    if (!fs.existsSync(tempDir)) {
      fs.mkdirSync(tempDir, { recursive: true });
    }

    const fileName = `script_${Date.now()}.py`;
    const filePath = path.join(tempDir, fileName);

    fs.writeFileSync(filePath, code, 'utf-8');

    try {
      const { stdout, stderr } = await execAsync(`python "${filePath}"`, {
        timeout: 15000, 
      });

      return {
        success: true,
        stdout: stdout.trim(),
        stderr: stderr.trim() || null,
        filePath,
      };
    } catch (error) {
      return {
        success: false,
        error: error.message,
      };
    } finally {
    }
  }
}
