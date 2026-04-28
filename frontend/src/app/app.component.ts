import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

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

  generateTrip() {
    fetch('http://127.0.0.1:5000/trips', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        destination: this.destination,
        start_date: this.startDate,
        end_date: this.endDate,
        people: this.people,
        budget: this.budget,
      }),
    })
      .then((res) => res.json())
      .then((data) => {
        console.log('Trip:', data);
        this.trip = data;
      });
  }
}
