import { Component, OnInit } from '@angular/core';
import { ApiService } from '../api.service';
import { Content } from '../content';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css']
})
export class DashboardComponent implements OnInit {
  contents: object[] = [];

  constructor(private apiService: ApiService) { }

  ngOnInit() {
    this.getContents();
  }

  getContents(): void {
    this.apiService.getContents()
      .subscribe(contents => this.contents = contents.slice(1, 5));
  }
}
