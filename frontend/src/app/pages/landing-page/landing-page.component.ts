import { Component } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-landing-page',
  templateUrl: './landing-page.component.html',
  styleUrls: ['./landing-page.component.scss']
})
export class LandingPageComponent {
  constructor(private router: Router) {}

  navigateToLogin(): void {
    this.router.navigate(['/login']);
  }

  navigateToDashboard(): void {
    this.router.navigate(['/dashboard']);
  }
} 