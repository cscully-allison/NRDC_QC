import { Component, OnInit, EventEmitter, Input, Output } from '@angular/core';
import { HierarchyNavigator } from '../safe-navigator';

@Component({
  selector: 'history-tracker',
  templateUrl: './history-tracker.component.html',
  styleUrls: ['./history-tracker.component.css']
})

export class HistoryTrackerComponent implements OnInit {

  @Input() navHist:HierarchyNavigator;
  @Output() notify: EventEmitter<any> = new EventEmitter();

  constructor() {

  }

  ngOnInit() {

  }

  notifyOfViewChange(histItem){
     this.notify.emit(histItem);
  }



}
