import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { ContentListComponent } from './content-list/content-list.component';
import { DashboardComponent } from './dashboard/dashboard.component';
import { ContentDetailComponent } from './content-detail/content-detail.component';

import { HomeComponent } from './home/home.component';
import { LoginComponent } from './login/login.component';
import { RegisterComponent } from './register/register.component';
import { AuthGuard } from './_guards/auth.guard';

const routes: Routes = [
  { path: '', component: HomeComponent, canActivate: [AuthGuard] },
  { path: 'home', component: HomeComponent },
  { path: 'login', component: LoginComponent },
  { path: 'register', component: RegisterComponent },
  { path: 'contents', component: ContentListComponent },
  { path: 'dashboard', component: DashboardComponent },
  { path: 'detail/:id', component: ContentDetailComponent },
  { path: '**', redirectTo: '' }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
