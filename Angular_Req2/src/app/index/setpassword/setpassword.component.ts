import { Component, OnInit } from '@angular/core';
import { FormGroup, FormControl, Validators, FormBuilder } from '@angular/forms';
import { Router, ActivatedRoute } from '@angular/router';
import { PasswordValidation } from './validators1';
import { ApiservicesService } from 'src/app/services/apiservices.service';
import Swal from 'sweetalert2';
import { HttpClient } from '@angular/common/http';

@Component({
selector: 'app-setpassword',
templateUrl: './setpassword.component.html',
styleUrls: ['./setpassword.component.scss']
})
export class SetpasswordComponent implements OnInit {

urlvalues;
forgot: any;
sai: any;
offerLetter: FormGroup;
empid: number;
employee_id: string;
pas: string;
data: string;
message:any;
constructor( private fb: FormBuilder, private routerNavigate: Router, private ar: ActivatedRoute,
    private as: ApiservicesService, private http: HttpClient) {
        this.urlvalues = this.ar.snapshot.queryParams;
        this.empid = this.urlvalues.empid;
        console.log(this.urlvalues);
}

ngOnInit() {

this.offerLetter = this.fb.group({
    name: ['', [  Validators.minLength(6)]],
    designation: ['', [ Validators.required, Validators.minLength(6)]],
    ctc: ['', [ Validators.required, Validators.minLength(6)]],
    description: ['', [ Validators.required, Validators.minLength(6)]],
    
});
}
generate(){
    let payload:any={
        name:this.offerLetter.value.name,
        designation:this.offerLetter.value.designation,
        ctc:this.offerLetter.value.ctc,
        description:this.offerLetter.value.description
    }
    this.as.generateOffer(payload).subscribe((res:any)=>{
        console.log("res",res)
        this.message=res.status
    })
}
}
// send(register) {
    
   
// this.employee_id = JSON.parse(this.urlvalues.empid);
// this.pas = register.value['conformpassword'];
// const data = {'employee_id': this.employee_id, 'password': this.pas};
// console.log(data);
// this.as.set_password(data).subscribe(res => {
//     console.log(res);
//     const status_code = res['message'];
//     if (status_code === 'password update successfully') {
//         Swal.fire(
//         'Your Password Set successfully!',
//         res['message'],
//         'success'
//         );
//         this.routerNavigate.navigate(['/login']);
// }
// this.routerNavigate.navigate(['/login']);
// });
// }};
