import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { TestmanagerComponent } from './test-manager.component';

describe('TestmanagerComponent', () => {
  let component: TestmanagerComponent;
  let fixture: ComponentFixture<TestmanagerComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ TestmanagerComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(TestmanagerComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
