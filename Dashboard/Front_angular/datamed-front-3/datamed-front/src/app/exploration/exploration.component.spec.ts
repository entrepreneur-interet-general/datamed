import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ExplorationComponent } from './exploration.component';

describe('ExplorationComponent', () => {
  let component: ExplorationComponent;
  let fixture: ComponentFixture<ExplorationComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ExplorationComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ExplorationComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
