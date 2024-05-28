import { Component, OnInit } from '@angular/core';
import { AuthService } from '../services/auth.service';
import { Router } from '@angular/router';
declare var $: any;

@Component({
  selector: 'app-bu',
  templateUrl: './bu.component.html',
  styleUrls: ['./bu.component.scss']
})
export class BuComponent implements OnInit {
  username: string;
  role: string;
  constructor(private authService: AuthService, private routerNavigate: Router) {
    this.username = localStorage.getItem('username'),
    this.role = localStorage.getItem('role');
  }

  ngOnInit() {
    $(document).ready(function () {
      $('.push_menu').click(function () {
        $('.wrapper').toggleClass('active');
      });


      (function () {
        'use strict';

        const treeviewMenu = $('.app-menu');

        // Toggle Sidebar
        $('[data-toggle="sidebar"]').click(function (event) {
          event.preventDefault();
          $('.app').toggleClass('sidenav-toggled');
        });

        // Activate sidebar treeview toggle
        $('[data-toggle = "treeview" ]').click(function (event) {
          event.preventDefault();
          if (!$(this).parent().hasClass('is-expanded')) {
            treeviewMenu.find('[data-toggle = "treeview"]').parent().removeClass('is-expanded');
          }
          $(this).parent().toggleClass('is-expanded');
        });

        // Set initial active toggle
        $('[data-toggle="treeview."].is-expanded').parent().toggleClass('is-expanded');

        // Activate bootstrip tooltips
        $('[data-toggle="tooltip"]').tooltip();

      })();

    });
  }

logoutAction() {
    if (this.authService.logOutAction()) {
      this.routerNavigate.navigate(['login']);
    }
  }

}
