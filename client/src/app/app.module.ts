import { NgModule } from '@angular/core';
import { ApiService } from './api.service';
import { FormsModule } from '@angular/forms';
import { ReactiveFormsModule }    from '@angular/forms';
import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { HttpClientModule, HTTP_INTERCEPTORS } from '../../node_modules/@angular/common/http';
import { HttpClientXsrfModule } from '../../node_modules/@angular/common/http';
import { ContentListComponent } from './content-list/content-list.component';
import { AppComponent } from './app.component';
import { AppRoutingModule } from './app-routing.module';
import { MessagesComponent } from './messages/messages.component';
import { DashboardComponent } from './dashboard/dashboard.component';
import { ContentDetailComponent } from './content-detail/content-detail.component';
import { AlertComponent } from './_components/alert.component';
import { HomeComponent } from './home/home.component';
import { LoginComponent } from './login/login.component';
import { RegisterComponent } from './register/register.component';
import { AuthGuard } from './_guards/auth.guard';
import { JwtInterceptor } from './_helpers/jwt.interceptor';
import { ErrorInterceptor } from './_helpers/error.interceptor';
import { fakeBackendProvider } from './_helpers/fake-backend';
import { MatButtonModule,
				 MatCheckboxModule,
				 MatToolbarModule,
				 MatListModule,
				 MatFormFieldModule,
				 MatCardModule,
				 MatInputModule } from '@angular/material';
import { FlexLayoutModule } from '@angular/flex-layout';

@NgModule({
  declarations: [ 
    AppComponent,
    AlertComponent,
    HomeComponent,
    LoginComponent,
    RegisterComponent,
    ContentListComponent,
    MessagesComponent,
    DashboardComponent,
    ContentDetailComponent
  ],
  imports: [
    AppRoutingModule,
    BrowserModule,
    BrowserAnimationsModule,
    FormsModule,
    MatButtonModule,
    MatCheckboxModule,
    MatToolbarModule,
		MatListModule,
		MatFormFieldModule,
		MatInputModule,
		MatCardModule,
    HttpClientModule,
    HttpClientXsrfModule.withOptions({
      cookieName: 'X_CSRF_Token',
      headerName: 'X-CSRF-Token'
    }),
    ReactiveFormsModule,
    FlexLayoutModule
  ],
  providers: [
    ApiService,
    { provide: HTTP_INTERCEPTORS, useClass: JwtInterceptor, multi: true },
    { provide: HTTP_INTERCEPTORS, useClass: ErrorInterceptor, multi: true },
    fakeBackendProvider
  ],
  bootstrap: [AppComponent]
})


export class AppModule { }
