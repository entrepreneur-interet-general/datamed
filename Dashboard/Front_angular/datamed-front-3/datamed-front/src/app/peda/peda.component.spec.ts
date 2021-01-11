import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PedaComponent } from './peda.component';

describe('PedaComponent', () => {
  let component: PedaComponent;
  let fixture: ComponentFixture<PedaComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ PedaComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(PedaComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
