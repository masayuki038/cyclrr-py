import { Component, OnInit } from '@angular/core';
import { Router } from "@angular/router";
import { MatTableDataSource, MatSlideToggleChange, MatDialog } from '@angular/material';
import { Subscription } from 'rxjs';
import { ApiService } from '../api.service';
import { Content } from '../content';
import { User } from '../_models/user';
import { AuthenticationService } from 'src/app/_services/authentication.service';
import { AlertService } from 'src/app/_services/alert.service';
import { ConfirmationDialogComponent } from '../confirmation-dialog/confirmation-dialog.component'

@Component({
  selector: 'app-content-list',
  templateUrl: './content-list.component.html',
  styleUrls: ['./content-list.component.css']
})
export class ContentListComponent implements OnInit {

  public displayedColumns = ['id', 'title', 'display', 'detail', 'delete'];
  public dataSource = new MatTableDataSource<Content>();
  currentUser: any;
  currentUserSubscription: Subscription;

  constructor(public apiService: ApiService,
    public authenticationService: AuthenticationService,
    private alertService: AlertService,
    private router: Router,
    public dialog: MatDialog) { }

  ngOnInit() {
    const userJson = localStorage.getItem('currentUser');
    if (userJson) {
      this.currentUser = JSON.parse(userJson);
      this.apiService.getContents(this.currentUser.id).subscribe((contents) => {
        this.dataSource.data = contents;
      });
    }
  }

  addContent() {
    this.router.navigate(['add']);
  }

  deleteContent = (id: number) => {
    const dialogRef = this.dialog.open(ConfirmationDialogComponent, {
      width: '350px',
      data: "Do you confirm the deletion of this data?"
    });
    dialogRef.afterClosed().subscribe(result => {
      if(result) {
        this.apiService.deleteContent(id).subscribe(() => {
          window.location.reload();
        });
      }
    });
  }

  toggleDisplay = (e: MatSlideToggleChange, content: Content) => {
    content.display = e.checked;
    this.apiService.updateContent(content).subscribe(() => {
      this.alertService.success("Updated.");
    });
  }
}