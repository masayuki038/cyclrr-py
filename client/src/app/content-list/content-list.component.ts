import { Component, OnInit } from '@angular/core';
import { Router } from "@angular/router";
import { Subscription } from 'rxjs';
import { ApiService } from '../api.service';
import { Content } from '../content';
import { User } from '../_models/user';
import { AuthenticationService } from 'src/app/_services/authentication.service';

@Component({
  selector: 'app-content-list',
  templateUrl: './content-list.component.html',
  styleUrls: ['./content-list.component.css']
})
export class ContentListComponent implements OnInit {

  public columns = ['id', 'name'];
  public rows: Content[];
  currentUser: any;
  currentUserSubscription: Subscription;

  constructor(public apiService: ApiService,
    public authenticationService: AuthenticationService,
    private router: Router) { }

  ngOnInit() {
    const userJson = localStorage.getItem('currentUser');
    if (userJson) {
      this.currentUser = JSON.parse(userJson);
      this.apiService.getContents(this.currentUser.id).subscribe((contents) => {
        this.rows = contents;
      });
    }
  }

  addUser() {
    this.router.navigate(['add']);
  }
}
