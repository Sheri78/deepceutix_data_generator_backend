export class GenerateResponseDto {
  chart?: {
    x: number[];
    y: number[];
    label: string;
  } | null;

  tables?: {
    headers: string[];  // Changed from 'columns' to 'headers'
    rows: string[][];
  }[];

  code?: string | null;

  explanation?: string | null;
}