import { Component, OnInit } from '@angular/core';
import { FormGroup, FormControl, Validators, FormBuilder } from '@angular/forms';
import { Router, ActivatedRoute } from '@angular/router';
import { ApiservicesService } from 'src/app/services/apiservices.service';
import Swal from 'sweetalert2';
import { HttpClient } from '@angular/common/http';
import { LocationStrategy } from '@angular/common';
import { saveAs } from 'file-saver';
import { DomSanitizer } from '@angular/platform-browser';
@Component({
    selector: 'app-offerletter',
    templateUrl: './offerletter.component.html',
    styleUrls: ['./offerletter.component.scss']
})
export class OfferLetterComponent implements OnInit {
    urlvalues;
    hrefLink:any;
    downloadURL: any
    offerLetter: FormGroup;
    data: string;
    message: any;
    constructor(private fb: FormBuilder, private routerNavigate: Router, private ar: ActivatedRoute,
        private as: ApiservicesService, private http: HttpClient, private location: LocationStrategy,    private sanitizer: DomSanitizer) {
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
        if (this.checkLogin() == false) {
            this.logout();
        }
        this.offerLetter = this.fb.group({
            name: ['', [Validators.minLength(6)]],
            designation: ['', [Validators.required, Validators.minLength(6)]],
            ctc: ['', [Validators.required, Validators.minLength(6)]],
            description: ['', [Validators.required, Validators.minLength(6)]],

        });
    }
    checkLogin() {
        if (localStorage.getItem('token')) {
            return true
        } else {
            return false
        }
    }
    logout() {
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
            this.downloadURL = res.path;
            console.log(this.downloadURL, "path")
            this.downloadURL = this.sanitizer.bypassSecurityTrustUrl(this.downloadURL);
        //     if (this.downloadURL.startsWith("file:///")) {
        //     this.downloadURL = this.downloadURL.substring("file:///".length);
        // }
            // window.location.href = this.downloadURL;
            // var link = document.createElement("a");
            // link.href = this.downloadURL;
            // console.log(link);
            // this.hrefLink=link.href.slice(8);
            // console.log(this.hrefLink,"link")
            // link.href = this.hrefLink;
            // console.log(link);
            // link.download = "sample.pdf"
            // document.body.appendChild(link);
            // console.log(this.hrefLink);
            // link.click();
            // document.body.removeChild(link);
            // this.downloadFile(this.downloadURL)
        });

    }
    // downloadFile(downloadUrl: string) {
    //     this.http.get(downloadUrl, { responseType: 'blob' }).subscribe((blob: Blob) => {
    //         saveAs(blob, 'offer_letter.pdf');
    //     }, error => {
    //         console.error("Download error:", error);
    //     });
    // }



}
