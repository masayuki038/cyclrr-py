import { Component, OnInit, Input } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Location } from '@angular/common';
import { ApiService } from '../api.service';
import { Content } from '../content';

@Component({
  selector: 'app-content-detail',
  templateUrl: './content-detail.component.html',
  styleUrls: ['./content-detail.component.scss']
})
export class ContentDetailComponent implements OnInit {
  public content: Content;

  constructor(
    private route: ActivatedRoute,
    private apiService: ApiService,
    private location: Location
  ) {}

  ngOnInit() {
    const id = +this.route.snapshot.paramMap.get('id');
    console.log("id: " + id);
    this.apiService.getContent(id).subscribe((content) => {
      this.content = content;
    });
  }

  goBack(): void {
    this.location.back();
  } 

  save(): void {
    this.apiService.updateContent(this.content)
      .subscribe(() => this.goBack());
  }
}
