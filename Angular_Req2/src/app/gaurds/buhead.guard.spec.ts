import { TestBed, async, inject } from '@angular/core/testing';

import { BuheadGuard } from './buhead.guard';

describe('BuheadGuard', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [BuheadGuard]
    });
  });

  it('should ...', inject([BuheadGuard], (guard: BuheadGuard) => {
    expect(guard).toBeTruthy();
  }));
});
