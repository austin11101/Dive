import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { MatSnackBar } from '@angular/material/snack-bar';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-login-page',
  templateUrl: './login-page.component.html',
  styleUrls: ['./login-page.component.scss']
})
export class LoginPageComponent implements OnInit {
  loginForm: FormGroup;
  isLoading = false;
  hidePassword = true;

  constructor(
    private fb: FormBuilder,
    private router: Router,
    private snackBar: MatSnackBar,
    private http: HttpClient
  ) {
    this.loginForm = this.fb.group({
      email: ['', [Validators.required, Validators.email]],
      password: ['', [Validators.required, Validators.minLength(6)]]
    });
  }

  ngOnInit(): void {
    // Check if user is already logged in
    const token = localStorage.getItem('auth_token');
    if (token) {
      this.router.navigate(['/dashboard']);
    }
  }

  async onSubmit(): Promise<void> {
    if (this.loginForm.valid) {
      this.isLoading = true;
      try {
        const { email, password } = this.loginForm.value;
        
        // Call the backend login API
        const response: any = await this.http.post('http://localhost:8000/api/v1/auth/login', {
          email: email,
          password: password
        }).toPromise();

        if (response.access_token) {
          // Store the token
          localStorage.setItem('auth_token', response.access_token);
          localStorage.setItem('user_info', JSON.stringify({
            email: email
          }));

          this.snackBar.open('Login successful! Welcome back!', 'Close', {
            duration: 3000,
            horizontalPosition: 'center',
            verticalPosition: 'top'
          });
          
          this.router.navigate(['/dashboard']);
        }
      } catch (error: any) {
        console.error('Login error:', error);
        let errorMessage = 'Login failed. Please check your credentials.';
        
        if (error.error?.detail) {
          errorMessage = error.error.detail;
        } else if (error.status === 401) {
          errorMessage = 'Invalid email or password.';
        }

        this.snackBar.open(errorMessage, 'Close', {
          duration: 5000,
          horizontalPosition: 'center',
          verticalPosition: 'top'
        });
      } finally {
        this.isLoading = false;
      }
    }
  }

  navigateToSignup(): void {
    this.router.navigate(['/signup']);
  }

  getErrorMessage(controlName: string): string {
    const control = this.loginForm.get(controlName);
    if (control?.hasError('required')) {
      return `${controlName.charAt(0).toUpperCase() + controlName.slice(1)} is required`;
    }
    if (control?.hasError('email')) {
      return 'Please enter a valid email address';
    }
    if (control?.hasError('minlength')) {
      return `${controlName.charAt(0).toUpperCase() + controlName.slice(1)} must be at least 6 characters`;
    }
    return '';
  }
} 