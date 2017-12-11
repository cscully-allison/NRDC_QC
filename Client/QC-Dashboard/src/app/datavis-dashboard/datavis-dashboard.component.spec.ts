import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { DatavisDashboardComponent } from './datavis-dashboard.component';

describe('DatavisDashboardComponent', () => {
  let component: DatavisDashboardComponent;
  let fixture: ComponentFixture<DatavisDashboardComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ DatavisDashboardComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(DatavisDashboardComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
