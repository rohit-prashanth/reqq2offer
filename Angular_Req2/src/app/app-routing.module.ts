import { NgModule } from "@angular/core";
import { RouterModule,Routes } from "@angular/router";
import { DashboardComponent } from './home/dashboard/dashboard.component';
import { BuComponent } from './bu/bu.component';
import { LoginComponent } from './index/login/login.component';
import { IndexComponent } from './index/index.component';
import { NomatchComponent } from './nomatch/nomatch.component';


const routes = [
  {path:"",redirectTo:"/login", pathMatch:"full"},
  {path:"login",component:LoginComponent},
  {
    path:'nomatch',
    component:NomatchComponent
  }
 
 
 
];


@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule {}
