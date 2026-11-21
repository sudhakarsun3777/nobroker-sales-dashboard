import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SchedulesComponent } from './schedules.component';

describe('SchedulesComponent', () => {
  let component: SchedulesComponent;
  let fixture: ComponentFixture<SchedulesComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [SchedulesComponent]
    });
    fixture = TestBed.createComponent(SchedulesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
