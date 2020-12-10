import { ComponentFixture, TestBed } from '@angular/core/testing';

import { RadarClassificationComponent } from './radar-classification.component';

describe('RadarClassificationComponent', () => {
  let component: RadarClassificationComponent;
  let fixture: ComponentFixture<RadarClassificationComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ RadarClassificationComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(RadarClassificationComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
