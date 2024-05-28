import { AuthService } from "./../services/auth.service";
import { Injectable } from "@angular/core";
import { CanActivate, Router } from "@angular/router";
import { Location } from "@angular/common";

@Injectable({
providedIn: "root"
})
export class AuthGuard implements CanActivate {
constructor(private routerNavigate: Router,private loc:Location) {
 
   
}

canActivate(): boolean {

//   var u= window.confirm("enter user");
//   if(u){
// return true;
// }
// else{
//  this.routerNavigate.navigate(['/hr'])
// }
// }
    var role=localStorage.getItem('role');
    var tkn=localStorage.getItem('token');


if((role==='HR')&&(tkn))
{
   
return true;
}


// if(tkn&&role==='Tag')
// {
   
// return true;
// }
// if(tkn&&role==='Admin')
// {
   
// return true;
// }
// if(tkn&&role==='BDM')
// {
   
// return true;
// }
// if(tkn&&role==='Account')
// {
   
// return true;
// }
// if(tkn&&role==='Finance Head')
// {
   
// return true;
// }

// if(tkn&&role==='Bu Head')
// {
   
// return true;
// }

else
{
 this.loc.back();
  //this.routerNavigate.navigate([prevurl]);
return false;
}

}
}
