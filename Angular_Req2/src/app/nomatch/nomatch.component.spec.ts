import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { NomatchComponent } from './nomatch.component';

describe('NomatchComponent', () => {
  let component: NomatchComponent;
  let fixture: ComponentFixture<NomatchComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ NomatchComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(NomatchComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
