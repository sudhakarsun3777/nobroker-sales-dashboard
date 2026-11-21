import { ComponentFixture, TestBed } from '@angular/core/testing';

import { VisitTrackingComponent } from './visit-tracking.component';

describe('VisitTrackingComponent', () => {
  let component: VisitTrackingComponent;
  let fixture: ComponentFixture<VisitTrackingComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [VisitTrackingComponent]
    });
    fixture = TestBed.createComponent(VisitTrackingComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
