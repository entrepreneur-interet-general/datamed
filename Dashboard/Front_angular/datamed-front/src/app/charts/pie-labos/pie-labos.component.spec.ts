import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PieLabosComponent } from './pie-labos.component';

describe('PieLabosComponent', () => {
  let component: PieLabosComponent;
  let fixture: ComponentFixture<PieLabosComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ PieLabosComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(PieLabosComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
