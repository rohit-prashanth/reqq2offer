import { Injectable } from '@angular/core';
import { CanActivate, ActivatedRouteSnapshot, RouterStateSnapshot, Router } from '@angular/router';
import { Observable } from 'rxjs';
import { Location } from "@angular/common";

@Injectable({
  providedIn: 'root'
})
export class AdminGuard implements CanActivate {
  constructor(private router:Router,private loc:Location)
  {

  }
  canActivate(
    next: ActivatedRouteSnapshot,
    state: RouterStateSnapshot): Observable<boolean> | Promise<boolean> | boolean {

      var tkn=localStorage.getItem('token');
      var role=localStorage.getItem('role');
      //console.log(role);
    
      if((role==='Admin')&&(tkn))
      {
         
      return true;
      }
        else
        {
          this.loc.back();
        return false;
        }
        }
  }



