import { Component, ChangeDetectorRef, NgZone } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { TripService } from './trip.service';
import { HttpClient } from '@angular/common/http'; // 🔥 LEGG TIL

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './app.html',
  styleUrls: ['./app.css'],
})
export class AppComponent {
  destination: string = '';
  startDate: string = '';
  endDate: string = '';
  people: number = 1;
  budget: string = 'medium';

  trip: any = null;

  // 🔥 LEGG TIL
  images: string[] = [];

  constructor(
    private tripService: TripService,
    private cdr: ChangeDetectorRef,
    private zone: NgZone,
    private http: HttpClient, // 🔥 LEGG TIL
  ) {}

  generateTrip() {
    this.trip = null;

    this.zone.run(() => {
      this.tripService
        .generateTrip({
          destination: this.destination,
          start_date: this.startDate,
          end_date: this.endDate,
          people: this.people,
          budget: this.budget,
        })
        .subscribe((data) => {
          this.trip = data;
          this.cdr.detectChanges();

          // 🔥 LEGG TIL HER
          this.loadImages(this.destination);
        });
    });
  }

  // 🔥 LEGG TIL
  loadImages(place: string) {
    this.http
      .get(`https://api.pexels.com/v1/search?query=${place}&per_page=3`, {
        headers: {
          Authorization: 'DIN_API_KEY',
        },
      })
      .subscribe((res: any) => {
        this.images = res.photos.map((p: any) => p.src.medium);
      });
  }
}
