import { Injectable } from '@angular/core';
import { CanDeactivate, ActivatedRouteSnapshot, RouterStateSnapshot, UrlTree, Router } from '@angular/router';
import { Observable } from 'rxjs';
import { StdashboardComponent } from '../staffing/stdashboard/stdashboard.component';
import { DashboardComponent } from '../home/dashboard/dashboard.component';
import { HrComponent } from '../hr/hr.component';

@Injectable({
  providedIn: 'root'
})
export class StGuard implements CanDeactivate<HrComponent> {
  constructor(private r:Router)
  {

  }
  canDeactivate(
    component: HrComponent,
    currentRoute: ActivatedRouteSnapshot,
    currentState: RouterStateSnapshot,
    nextState: RouterStateSnapshot
  ): Observable<boolean|UrlTree>|Promise<boolean|UrlTree>|boolean|UrlTree  {

var u=window.confirm("u exit?")
if(u)
{
  return true;
}
var role=localStorage.getItem('role');
debugger;
    // if(role==='HR')
    // {
    // this.r.navigate(['/hr/hrdashboard']);
    // return true;
    // }
  
  
    }

 
}
