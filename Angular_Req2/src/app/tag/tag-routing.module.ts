import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { TagComponent } from './tag.component';
import { SelectedcandidateComponent } from './selectedcandidate/selectedcandidate.component';
import { DashboardComponent } from '../tag/dashboard/dashboard.component';
import { TaginternalreqsComponent } from './taginternalreqs/taginternalreqs.component';
import { TagexternalreqsComponent } from './tagexternalreqs/tagexternalreqs.component';
import { ProfileComponent } from './profile/profile.component';
import { ChangepasswordComponent } from './changepassword/changepassword.component';
import { TagGuard } from '../gaurds/tag.guard';

const routes: Routes = [
  {path:'tag',component:TagComponent,canActivate:[TagGuard],
  children:[ 
    {path:'dashboard',component:DashboardComponent},
    {path: 'profile', component:ProfileComponent},
  {path:'selectedcandidate',component:SelectedcandidateComponent},
  {path:'taginternalreqs', component:TaginternalreqsComponent},
   {path:'tagexternalreq', component:TagexternalreqsComponent},
   {path:'changepassword', component:ChangepasswordComponent}
  ]
 }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class TagRoutingModule { }
