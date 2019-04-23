import { Component, OnInit } from '@angular/core';
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
  currentUser: User;
  currentUserSubscription: Subscription;

  constructor(public apiService: ApiService,
    public authenticationService: AuthenticationService) {
    this.currentUserSubscription = this.authenticationService.currentUser.subscribe(user => {
      this.currentUser = user;
      this.apiService.getContents(this.currentUser.id).subscribe((contents) => {
        this.rows = contents;
      });
    }); 
  }

  ngOnInit() {

  }
}
