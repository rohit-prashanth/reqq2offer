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
    remoteAddress="127.0.0.1:8000";
    finalURL:any;
    constructor(private fb: FormBuilder, private routerNavigate: Router, private ar: ActivatedRoute,
        private as: ApiservicesService, private http: HttpClient, private location: LocationStrategy,    private sanitizer: DomSanitizer) {
        this.urlvalues = this.ar.snapshot.queryParams;
        console.log(this.urlvalues);
        history.pushState(null, null, window.location.href);
        this.location.onPopState(() => {
            history.pushState(null, null, window.location.href);
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
   

    generate() {
        const offerlettertitleName=`${this.offerLetter.value.name}_${this.offerLetter.value.designation}`;
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
            this.finalURL = `http://${this.remoteAddress}${this.downloadURL}`;
            console.log(this.finalURL, "final URL");
        
            this.downloadPDF(this.finalURL,offerlettertitleName);
            
        });

    }
    downloadPDF(url: string, filename: string) {
        fetch(url)
            .then(response => response.blob())
            .then(blob => {
                const downloadUrl = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.style.display = 'none';
                a.href = downloadUrl;
                a.download = `${filename}.pdf`;
                document.body.appendChild(a);
                a.click();
                window.URL.revokeObjectURL(downloadUrl);
                document.body.removeChild(a);
            })
            .catch(err => console.error('Error downloading the PDF:', err));
    }
}
