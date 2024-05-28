import { Component, OnInit } from '@angular/core';
import { FormGroup, FormControl, Validators, FormBuilder } from '@angular/forms';
import { Router, ActivatedRoute } from '@angular/router';
import { ApiservicesService } from 'src/app/services/apiservices.service';
import Swal from 'sweetalert2';
import { HttpClient } from '@angular/common/http';
import { LocationStrategy } from '@angular/common';
import { saveAs } from 'file-saver';
@Component({
selector: 'app-offerletter',
templateUrl: './offerletter.component.html',
styleUrls: ['./offerletter.component.scss']
})
export class OfferLetterComponent implements OnInit {
urlvalues;
offerLetter: FormGroup;
data: string;
message:any;
constructor( private fb: FormBuilder, private routerNavigate: Router, private ar: ActivatedRoute,
    private as: ApiservicesService, private http: HttpClient,private location: LocationStrategy) {
        this.urlvalues = this.ar.snapshot.queryParams;
        console.log(this.urlvalues);
        history.pushState(null, null, window.location.href);
        // check if back or forward button is pressed.
        this.location.onPopState(() => {
            history.pushState(null, null, window.location.href);
            // this.stepper.previous();
        });
}

ngOnInit() {
if(this.checkLogin()==false){
    this.logout();
}
this.offerLetter = this.fb.group({
    name: ['', [  Validators.minLength(6)]],
    designation: ['', [ Validators.required, Validators.minLength(6)]],
    ctc: ['', [ Validators.required, Validators.minLength(6)]],
    description: ['', [ Validators.required, Validators.minLength(6)]],
    
});
}
checkLogin(){
    if(localStorage.getItem('token')){
        return true
    }else{
        return false
    }
}
logout(){
    this.routerNavigate.navigate(['/login'])
    localStorage.removeItem('token')    
}
// generate(){
//     let payload:any={
//         name:this.offerLetter.value.name,
//         designation:this.offerLetter.value.designation,
//         ctc:this.offerLetter.value.ctc,
//         description:this.offerLetter.value.description
//     }
//     this.as.generateOffer(payload).subscribe((res:any)=>{
//         console.log("res",res)
//         this.message=res.status
//         console.log( this.message,"status")
//         const downloadUrl = res.path; 
//         this.downloadFile(downloadUrl);
//     })
// }

generate() {
    let payload: any = {
      name: this.offerLetter.value.name,
      designation: this.offerLetter.value.designation,
      ctc: this.offerLetter.value.ctc,
      description: this.offerLetter.value.description
    };
    this.as.generateOffer(payload).subscribe((res: any) => {
        console.log("res", res);
        this.message = res.status;
        console.log(this.message, "status");
       // Construct file URL
    const downloadURL = `file:///${res.path.replace(/\\/g, "/")}`;

    // Trigger download
    this.downloadFile(downloadURL);
  });
}

downloadFile(downloadURL: string) {
  const link = document.createElement('a');
  link.setAttribute('href', downloadURL);
  link.setAttribute('download', 'filename.pdf'); // You can specify the filename here
  document.body.appendChild(link);
  link.click();
  link.remove();
}
 

}
