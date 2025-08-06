import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Router } from '@angular/router';

interface NotificationSettings {
  emailNotifications: boolean;
  jobAlerts: boolean;
  applicationUpdates: boolean;
  weeklyDigest: boolean;
  marketingEmails: boolean;
}

interface PrivacySettings {
  profileVisibility: 'public' | 'private' | 'connections';
  showSalary: boolean;
  showContactInfo: boolean;
  allowMessages: boolean;
  dataSharing: boolean;
}

interface JobPreferences {
  preferredLocations: string[];
  salaryRange: {
    min: number;
    max: number;
  };
  jobTypes: string[];
  remoteWork: boolean;
  relocation: boolean;
}

@Component({
  selector: 'app-settings',
  templateUrl: './settings.component.html',
  styleUrls: ['./settings.component.scss']
})
export class SettingsComponent implements OnInit {
  activeTab = 0;
  isLoading = false;
  
  // Forms
  profileForm: FormGroup;
  notificationForm: FormGroup;
  privacyForm: FormGroup;
  jobPreferencesForm: FormGroup;
  accountForm: FormGroup;
  
  // Settings data
  notificationSettings: NotificationSettings = {
    emailNotifications: true,
    jobAlerts: true,
    applicationUpdates: true,
    weeklyDigest: false,
    marketingEmails: false
  };
  
  privacySettings: PrivacySettings = {
    profileVisibility: 'connections',
    showSalary: false,
    showContactInfo: true,
    allowMessages: true,
    dataSharing: false
  };
  
  jobPreferences: JobPreferences = {
    preferredLocations: ['London', 'Manchester', 'Remote'],
    salaryRange: { min: 30000, max: 80000 },
    jobTypes: ['Full-time', 'Contract'],
    remoteWork: true,
    relocation: false
  };
  
  // Available options
  locations = [
    'London', 'Manchester', 'Birmingham', 'Leeds', 'Liverpool', 
    'Sheffield', 'Edinburgh', 'Glasgow', 'Bristol', 'Cardiff', 'Remote'
  ];
  
  jobTypes = ['Full-time', 'Part-time', 'Contract', 'Freelance', 'Internship'];
  
  visibilityOptions = [
    { value: 'public', label: 'Public - Anyone can see my profile' },
    { value: 'connections', label: 'Connections only - Only my connections can see my profile' },
    { value: 'private', label: 'Private - Only I can see my profile' }
  ];

  constructor(
    private fb: FormBuilder,
    private snackBar: MatSnackBar,
    private router: Router
  ) {
    this.initializeForms();
  }

  ngOnInit(): void {
    this.loadUserSettings();
  }

  private initializeForms(): void {
    this.profileForm = this.fb.group({
      firstName: ['', Validators.required],
      lastName: ['', Validators.required],
      email: ['', [Validators.required, Validators.email]],
      phone: [''],
      location: [''],
      bio: [''],
      website: [''],
      linkedin: ['']
    });

    this.notificationForm = this.fb.group({
      emailNotifications: [true],
      jobAlerts: [true],
      applicationUpdates: [true],
      weeklyDigest: [false],
      marketingEmails: [false]
    });

    this.privacyForm = this.fb.group({
      profileVisibility: ['connections'],
      showSalary: [false],
      showContactInfo: [true],
      allowMessages: [true],
      dataSharing: [false]
    });

    this.jobPreferencesForm = this.fb.group({
      preferredLocations: [[]],
      salaryMin: [30000],
      salaryMax: [80000],
      jobTypes: [[]],
      remoteWork: [true],
      relocation: [false]
    });

    this.accountForm = this.fb.group({
      currentPassword: ['', Validators.required],
      newPassword: ['', [Validators.required, Validators.minLength(8)]],
      confirmPassword: ['', Validators.required]
    });
  }

  private loadUserSettings(): void {
    // In a real app, this would load from a service
    this.profileForm.patchValue({
      firstName: 'John',
      lastName: 'Doe',
      email: 'john.doe@example.com',
      phone: '+44 123 456 7890',
      location: 'London',
      bio: 'Experienced software developer with expertise in Angular and Node.js',
      website: 'https://johndoe.dev',
      linkedin: 'https://linkedin.com/in/johndoe'
    });

    this.notificationForm.patchValue(this.notificationSettings);
    this.privacyForm.patchValue(this.privacySettings);
    this.jobPreferencesForm.patchValue({
      ...this.jobPreferences,
      salaryMin: this.jobPreferences.salaryRange.min,
      salaryMax: this.jobPreferences.salaryRange.max
    });
  }

  onTabChange(event: any): void {
    this.activeTab = event.index;
  }

  saveProfile(): void {
    if (this.profileForm.valid) {
      this.isLoading = true;
      // Simulate API call
      setTimeout(() => {
        this.isLoading = false;
        this.showSuccessMessage('Profile updated successfully');
      }, 1000);
    }
  }

  saveNotifications(): void {
    this.isLoading = true;
    setTimeout(() => {
      this.isLoading = false;
      this.showSuccessMessage('Notification settings saved');
    }, 1000);
  }

  savePrivacy(): void {
    this.isLoading = true;
    setTimeout(() => {
      this.isLoading = false;
      this.showSuccessMessage('Privacy settings updated');
    }, 1000);
  }

  saveJobPreferences(): void {
    this.isLoading = true;
    setTimeout(() => {
      this.isLoading = false;
      this.showSuccessMessage('Job preferences saved');
    }, 1000);
  }

  changePassword(): void {
    if (this.accountForm.valid) {
      const { currentPassword, newPassword, confirmPassword } = this.accountForm.value;
      
      if (newPassword !== confirmPassword) {
        this.showErrorMessage('New passwords do not match');
        return;
      }

      this.isLoading = true;
      setTimeout(() => {
        this.isLoading = false;
        this.showSuccessMessage('Password changed successfully');
        this.accountForm.reset();
      }, 1000);
    }
  }

  exportData(): void {
    this.isLoading = true;
    setTimeout(() => {
      this.isLoading = false;
      this.showSuccessMessage('Data export started. You will receive an email when ready.');
    }, 1000);
  }

  deleteAccount(): void {
    if (confirm('Are you sure you want to delete your account? This action cannot be undone.')) {
      this.isLoading = true;
      setTimeout(() => {
        this.isLoading = false;
        this.showSuccessMessage('Account deletion request submitted');
      }, 1000);
    }
  }

  private showSuccessMessage(message: string): void {
    this.snackBar.open(message, 'Close', {
      duration: 3000,
      panelClass: ['success-snackbar']
    });
  }

  private showErrorMessage(message: string): void {
    this.snackBar.open(message, 'Close', {
      duration: 5000,
      panelClass: ['error-snackbar']
    });
  }

  goBack(): void {
    this.router.navigate(['/dashboard']);
  }
} 