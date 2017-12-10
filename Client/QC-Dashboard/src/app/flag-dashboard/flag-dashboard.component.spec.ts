import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { FlagDashboardComponent } from './flag-dashboard.component';

describe('FlagDashboardComponent', () => {
  let component: FlagDashboardComponent;
  let fixture: ComponentFixture<FlagDashboardComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ FlagDashboardComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(FlagDashboardComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
