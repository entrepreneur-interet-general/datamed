import { ComponentFixture, TestBed } from '@angular/core/testing';

import { BarClasseTherapeutiqueComponent } from './bar-classe-therapeutique.component';

describe('BarClasseTherapeutiqueComponent', () => {
  let component: BarClasseTherapeutiqueComponent;
  let fixture: ComponentFixture<BarClasseTherapeutiqueComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ BarClasseTherapeutiqueComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(BarClasseTherapeutiqueComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
