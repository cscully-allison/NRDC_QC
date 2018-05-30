import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { HistoryTrackerComponent } from './history-tracker.component';

describe('HistoryTrackerComponent', () => {
  let component: HistoryTrackerComponent;
  let fixture: ComponentFixture<HistoryTrackerComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ HistoryTrackerComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(HistoryTrackerComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
