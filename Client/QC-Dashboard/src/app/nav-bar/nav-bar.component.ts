import { Component, OnInit, Renderer } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';

@Component({
  selector: 'nav-bar',
  templateUrl: './nav-bar.component.html',
  styleUrls: ['./nav-bar.component.css']
})
export class NavBarComponent implements OnInit {

  constructor(private route:ActivatedRoute, private renderer:Renderer) { }

  ngOnInit() {
  }

  updateBar(event){
      this.clearActiveClass(event.target.parentNode.parentNode);
      this.renderer.setElementClass(event.target.parentNode,"active",true);
  }

  clearActiveClass(listHead){
    for(var li = 0; li < listHead.children.length; li++){
        listHead.children[li].classList.remove('active');
    }

  }

}
