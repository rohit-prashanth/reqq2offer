import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { OfferLetterComponent } from './offerletter.component';

describe('OfferLetterComponent', () => {
  let component: OfferLetterComponent;
  let fixture: ComponentFixture<OfferLetterComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ OfferLetterComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(OfferLetterComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
