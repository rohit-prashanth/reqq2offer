import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { LoginComponent } from './login/login.component';
import { SignUpComponent } from './sign-up/sign-up.component';
import { ForgotComponent } from './forgot/forgot.component';
import { ReactiveFormsModule, FormsModule} from '@angular/forms';
import { SetpasswordComponent } from './setpassword/setpassword.component';
import { OfferLetterComponent } from './offerletter/offerletter.component';





@NgModule({
  declarations: [LoginComponent,
     SignUpComponent,
     ForgotComponent,
      SetpasswordComponent,
    OfferLetterComponent  ],
  imports: [
    CommonModule,
    ReactiveFormsModule,
    FormsModule
   

  ]
})
export class IndexModule { }
