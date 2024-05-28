import { TestBed, async, inject } from '@angular/core/testing';

import { StGuard } from './st.guard';

describe('StGuard', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [StGuard]
    });
  });

  it('should ...', inject([StGuard], (guard: StGuard) => {
    expect(guard).toBeTruthy();
  }));
});
