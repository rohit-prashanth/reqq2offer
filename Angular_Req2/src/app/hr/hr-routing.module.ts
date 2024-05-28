import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { AuthGuard } from '../gaurds/auth.guard';
import { HrComponent } from './hr.component';
import { HrSelectedCandidateComponent } from './hr-selected-candidate/hr-selected-candidate.component';
import { HrExternalReqComponent } from './hr-external-req/hr-external-req.component';
import { HrInternalReqComponent } from './hr-internal-req/hr-internal-req.component';
import { TagselectedcandidateComponent } from './tagselectedcandidate/tagselectedcandidate.component';
import { DashboardComponent } from './dashboard/dashboard.component';
import { ProfileComponent } from './profile/profile.component';
import { ChangepasswordComponent } from './changepassword/changepassword.component';


const routes: Routes = [
  // { path: '', redirectTo: '/hrdashboard', pathMatch: 'full' },
  {path:'hr',component:HrComponent,canActivate:[AuthGuard],
  children:[ 
     {path:'hrdashboard', component:DashboardComponent},
     {path:'profile', component:ProfileComponent,canActivate:[AuthGuard]},
     {path:'changepassword', component:ChangepasswordComponent,canActivate:[AuthGuard]},
    {path:'hrinternalreqs', component:HrInternalReqComponent,canActivate:[AuthGuard]},
    {path:'hrexternalreq', component:HrExternalReqComponent,canActivate:[AuthGuard]},
    {path:'hr_selected_candidets', component:HrSelectedCandidateComponent,canActivate:[AuthGuard]},
      {path:'tag_selected_candidates',component:TagselectedcandidateComponent,canActivate:[AuthGuard]}
   
  
  ]
}
];



@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class HrRoutingModule { }
