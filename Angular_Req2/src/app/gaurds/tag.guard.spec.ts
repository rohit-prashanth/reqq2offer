import { TestBed, async, inject } from '@angular/core/testing';

import { TagGuard } from './tag.guard';

describe('TagGuard', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [TagGuard]
    });
  });

  it('should ...', inject([TagGuard], (guard: TagGuard) => {
    expect(guard).toBeTruthy();
  }));
});
