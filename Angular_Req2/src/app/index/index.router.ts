
import { ForgotComponent } from './forgot/forgot.component';
import { LoginComponent } from './login/login.component';
import { Routes } from '@angular/router';
import { SignUpComponent } from './sign-up/sign-up.component';
import { IndexComponent } from './index.component';

import { SetpasswordComponent } from './setpassword/setpassword.component';
import { OfferLetterComponent } from './offerletter/offerletter.component';


export const Indexroutes: Routes = [
{path:'',redirectTo:'login',pathMatch:'full'},

    {path:'login',component:LoginComponent},
    {path:'offerLetter',component:OfferLetterComponent},
    
    {path:'sing-up',component:SignUpComponent},
   

   {path:'forgotpassword',component:ForgotComponent},
   {path:'setpassword',component:SetpasswordComponent}
]
