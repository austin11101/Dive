import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { MatSnackBar } from '@angular/material/snack-bar';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-signup-page',
  templateUrl: './signup-page.component.html',
  styleUrls: ['./signup-page.component.scss']
})
export class SignupPageComponent implements OnInit {
  signupForm: FormGroup;
  isLoading = false;
  hidePassword = true;
  hideConfirmPassword = true;

  constructor(
    private fb: FormBuilder,
    private router: Router,
    private snackBar: MatSnackBar,
    private http: HttpClient
  ) {
    this.signupForm = this.fb.group({
      firstName: ['', [Validators.required, Validators.minLength(2)]],
      lastName: ['', [Validators.required, Validators.minLength(2)]],
      email: ['', [Validators.required, Validators.email]],
      password: ['', [Validators.required, Validators.minLength(8)]],
      confirmPassword: ['', [Validators.required]]
    }, { validators: this.passwordMatchValidator });
  }

  ngOnInit(): void {
    // Check if user is already logged in
    const token = localStorage.getItem('auth_token');
    if (token) {
      this.router.navigate(['/dashboard']);
    }
  }

  passwordMatchValidator(form: FormGroup) {
    const password = form.get('password');
    const confirmPassword = form.get('confirmPassword');
    
    if (password && confirmPassword && password.value !== confirmPassword.value) {
      confirmPassword.setErrors({ passwordMismatch: true });
      return { passwordMismatch: true };
    }
    
    return null;
  }

  async onSubmit(): Promise<void> {
    if (this.signupForm.valid) {
      this.isLoading = true;
      try {
        const formData = this.signupForm.value;
        
        // Call the backend signup API
        const response: any = await this.http.post('http://localhost:8000/api/v1/auth/register', {
          first_name: formData.firstName,
          last_name: formData.lastName,
          email: formData.email,
          password: formData.password
        }).toPromise();

        if (response.access_token) {
          // Store the token
          localStorage.setItem('auth_token', response.access_token);
          localStorage.setItem('user_info', JSON.stringify({
            firstName: formData.firstName,
            lastName: formData.lastName,
            email: formData.email
          }));

          this.snackBar.open('Account created successfully! Welcome to CV Revamp!', 'Close', {
            duration: 3000,
            horizontalPosition: 'center',
            verticalPosition: 'top'
          });

          // Redirect to dashboard
          this.router.navigate(['/dashboard']);
        }
      } catch (error: any) {
        console.error('Signup error:', error);
        let errorMessage = 'Registration failed. Please try again.';
        
        if (error.error?.detail) {
          errorMessage = error.error.detail;
        } else if (error.status === 409) {
          errorMessage = 'An account with this email already exists.';
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

  navigateToLogin(): void {
    this.router.navigate(['/login']);
  }

  getErrorMessage(controlName: string): string {
    const control = this.signupForm.get(controlName);
    if (control?.hasError('required')) {
      return `${controlName.charAt(0).toUpperCase() + controlName.slice(1)} is required`;
    }
    if (control?.hasError('email')) {
      return 'Please enter a valid email address';
    }
    if (control?.hasError('minlength')) {
      const minLength = control.getError('minlength').requiredLength;
      return `${controlName.charAt(0).toUpperCase() + controlName.slice(1)} must be at least ${minLength} characters`;
    }
    if (control?.hasError('passwordMismatch')) {
      return 'Passwords do not match';
    }
    return '';
  }
} 