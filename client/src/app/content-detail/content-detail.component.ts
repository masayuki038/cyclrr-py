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
    
    if (id) {
      this.apiService.getContent(id).subscribe((content) => {
        this.content = content;
      });
      return;
    } 

    this.content = new Content();
  }

  goBack(): void {
    this.location.back();
  } 

  save(): void {
    if (this.content.id) {
      this.apiService.updateContent(this.content)
      .subscribe(() => this.goBack());
    } else {
      const userJson = localStorage.getItem('currentUser');
      const currentUser = JSON.parse(userJson);
      this.content.user_id = currentUser.id;
      this.content.display = true;
      this.apiService.registerContent(this.content)
      .subscribe(() => this.goBack());
    }
  }
}
