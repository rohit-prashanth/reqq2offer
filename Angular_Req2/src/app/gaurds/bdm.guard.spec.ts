import { TestBed, async, inject } from '@angular/core/testing';

import { BdmGuard } from './bdm.guard';

describe('BdmGuard', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [BdmGuard]
    });
  });

  it('should ...', inject([BdmGuard], (guard: BdmGuard) => {
    expect(guard).toBeTruthy();
  }));
});
