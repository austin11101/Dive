import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { MatSnackBar } from '@angular/material/snack-bar';

@Component({
  selector: 'app-login-page',
  templateUrl: './login-page.component.html',
  styleUrls: ['./login-page.component.scss']
})
export class LoginPageComponent {
  loginForm: FormGroup;
  registerForm: FormGroup;
  isLoading = false;
  isLoginMode = true;

  constructor(
    private fb: FormBuilder,
    private router: Router,
    private snackBar: MatSnackBar
  ) {
    this.loginForm = this.fb.group({
      email: ['', [Validators.required, Validators.email]],
      password: ['', [Validators.required, Validators.minLength(6)]]
    });

    this.registerForm = this.fb.group({
      firstName: ['', [Validators.required]],
      lastName: ['', [Validators.required]],
      email: ['', [Validators.required, Validators.email]],
      password: ['', [Validators.required, Validators.minLength(6)]],
      confirmPassword: ['', [Validators.required]]
    }, { validators: this.passwordMatchValidator });
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

  toggleMode(): void {
    this.isLoginMode = !this.isLoginMode;
    this.loginForm.reset();
    this.registerForm.reset();
  }

  async onSubmit(): Promise<void> {
    if (this.isLoginMode) {
      await this.handleLogin();
    } else {
      await this.handleRegister();
    }
  }

  private async handleLogin(): Promise<void> {
    if (this.loginForm.valid) {
      this.isLoading = true;
      try {
        const { email, password } = this.loginForm.value;
        
        // TODO: Implement actual login API call
        console.log('Login attempt:', { email, password });
        
        // Simulate API call
        await new Promise(resolve => setTimeout(resolve, 1000));
        
        this.snackBar.open('Login successful!', 'Close', {
          duration: 3000,
          horizontalPosition: 'center',
          verticalPosition: 'top'
        });
        
        this.router.navigate(['/dashboard']);
      } catch (error) {
        this.snackBar.open('Login failed. Please try again.', 'Close', {
          duration: 3000,
          horizontalPosition: 'center',
          verticalPosition: 'top'
        });
      } finally {
        this.isLoading = false;
      }
    }
  }

  private async handleRegister(): Promise<void> {
    if (this.registerForm.valid) {
      this.isLoading = true;
      try {
        const formData = this.registerForm.value;
        
        // TODO: Implement actual registration API call
        console.log('Register attempt:', formData);
        
        // Simulate API call
        await new Promise(resolve => setTimeout(resolve, 1000));
        
        this.snackBar.open('Registration successful! Please log in.', 'Close', {
          duration: 3000,
          horizontalPosition: 'center',
          verticalPosition: 'top'
        });
        
        this.isLoginMode = true;
        this.registerForm.reset();
      } catch (error) {
        this.snackBar.open('Registration failed. Please try again.', 'Close', {
          duration: 3000,
          horizontalPosition: 'center',
          verticalPosition: 'top'
        });
      } finally {
        this.isLoading = false;
      }
    }
  }

  getErrorMessage(controlName: string, form: FormGroup): string {
    const control = form.get(controlName);
    if (control?.hasError('required')) {
      return `${controlName.charAt(0).toUpperCase() + controlName.slice(1)} is required`;
    }
    if (control?.hasError('email')) {
      return 'Please enter a valid email address';
    }
    if (control?.hasError('minlength')) {
      return `${controlName.charAt(0).toUpperCase() + controlName.slice(1)} must be at least 6 characters`;
    }
    if (control?.hasError('passwordMismatch')) {
      return 'Passwords do not match';
    }
    return '';
  }
} 