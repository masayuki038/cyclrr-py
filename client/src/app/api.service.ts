import { Injectable } from '@angular/core';
import { Observable, of } from 'rxjs';
import { catchError, map, tap } from 'rxjs/operators';
import { Content } from './content';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { MessageService } from './message.service';

const httpOptions = {
  headers: new HttpHeaders({ 'Content-Type': 'application/json' })
};

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  API_URL: string = "/";
  constructor(
    private http: HttpClient, 
    private messageService: MessageService) { }

  public getContents(uid: number): Observable<Content[]> {
    var endpoint = this.API_URL + "contents";
    return this.http.get<Content[]>(endpoint)
      .pipe(
        tap(_ => this.log('fetched contents')),
	    catchError(this.handleError('get', [])));
  }

  public getContent(id: number): Observable<Content> {
    var endpoint = this.API_URL + "content/" + id;
    return this.http.get<Content>(endpoint)
      .pipe(
        tap(_ => this.log('fetched content')),
	    catchError(this.handleError('getContent', null)));
  }

  readCookie(name: string): string {
    var nameEq = name + "=";
    var ca = document.cookie.split(";");
    for (var i = 0; i < ca.length; i++) {
      var c = ca[i];
      console.log(c);
      while (c.charAt(0) === " ") c = c.substring(1, c.length);
      if (c.indexOf(nameEq) === 0) return c.substring(nameEq.length, c.length);
    }
    return null;
  }

  registerContent(content: Content): Observable<any> {
    return this.http.post(this.API_URL + "contents", content)
      .pipe(
        tap(_ => this.log('registered content')),
        catchError(this.handleError<any>('registerContent')));
  }

  updateContent(content: Content): Observable<any> {
    return this.http.put(this.API_URL + "content/" + content.id, content)
      .pipe(
        tap(_ => this.log(`updated content id:${content.id}`)),
        catchError(this.handleError<any>('updateContent')));
  }
    
  deleteContent(id: number): Observable<any> {
    return this.http.delete(this.API_URL + "content/" + id)
      .pipe(
        tap(_ => this.log(`deleted content id:${id}`)),
        catchError(this.handleError<any>('updateContent')));
  }

  private log(message: string) {
    this.messageService.add(`ApiService: ${message}`);
  }

  private handleError<T> (operation = 'operation', result?: T) {
    return (error: any): Observable<T> => {
      console.error(error);
      this.log(`${operation} failed: ${error.message}`);
      return of(result as T);
    };
  }
}
