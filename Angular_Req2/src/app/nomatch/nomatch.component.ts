import { Component, OnInit } from '@angular/core';
import { Router, NavigationEnd } from '@angular/router';
import { filter } from 'rxjs/operators';
@Component({
  selector: 'app-nomatch',
  templateUrl: './nomatch.component.html',
  styleUrls: ['./nomatch.component.scss']
})
export class NomatchComponent implements OnInit {
  role: string;
  history: any[];

  previousUrl: string;
  currentUrl: string;
  constructor(private routerNavigate:Router) { }

  ngOnInit() {
  this.role=localStorage.getItem('role');
  }
go()
{


}
}
