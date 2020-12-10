import { ComponentFixture, TestBed } from '@angular/core/testing';

import { BarCauseRuptureComponent } from './bar-cause-rupture.component';

describe('BarCauseRuptureComponent', () => {
  let component: BarCauseRuptureComponent;
  let fixture: ComponentFixture<BarCauseRuptureComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ BarCauseRuptureComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(BarCauseRuptureComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
