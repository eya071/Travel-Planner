import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class TripService {
  private apiUrl = 'http://127.0.0.1:5000/trips';

  constructor(private http: HttpClient) {}

  generateTrip(payload: {
    destination: string;
    start_date: string;
    end_date: string;
    people: number;
    budget: string;
  }): Observable<any> {
    return this.http.post<any>(this.apiUrl, payload);
  }
}
