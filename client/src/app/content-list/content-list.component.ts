import { Component, OnInit } from '@angular/core';
import { ApiService } from '../api.service';
import { Content } from '../content';

@Component({
  selector: 'app-content-list',
  templateUrl: './content-list.component.html',
  styleUrls: ['./content-list.component.css']
})
export class ContentListComponent implements OnInit {

  public columns = ['id', 'name'];
  public rows: Content[];

  constructor(public apiService: ApiService) { }

  ngOnInit() {
    this.apiService.getContents().subscribe((contents) => {
      console.log(contents);
      this.rows = contents;
    });
  }
}
