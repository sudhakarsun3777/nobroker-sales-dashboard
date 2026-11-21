import { ComponentFixture, TestBed } from '@angular/core/testing';

import { RmPerformanceComponent } from './rm-performance.component';

describe('RmPerformanceComponent', () => {
  let component: RmPerformanceComponent;
  let fixture: ComponentFixture<RmPerformanceComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [RmPerformanceComponent]
    });
    fixture = TestBed.createComponent(RmPerformanceComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
