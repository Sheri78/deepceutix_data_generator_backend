import { Test, TestingModule } from '@nestjs/testing';
import { GenerateService } from './GenerateService';

describe('GenerateService', () => {
  let service: GenerateService;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [GenerateService],
    }).compile();

    service = module.get<GenerateService>(GenerateService);
  });

  it('should be defined', () => {
    expect(service).toBeDefined();
  });
});
