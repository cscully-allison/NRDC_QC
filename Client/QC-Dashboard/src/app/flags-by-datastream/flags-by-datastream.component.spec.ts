import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { FlagsByDatastreamComponent } from './flags-by-datastream.component';

describe('FlagsByDatastreamComponent', () => {
  let component: FlagsByDatastreamComponent;
  let fixture: ComponentFixture<FlagsByDatastreamComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ FlagsByDatastreamComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(FlagsByDatastreamComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
