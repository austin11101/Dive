import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { CVData } from '../../components/cv-editor/cv-editor.component';
import { Job } from '../../services/job.service';
import { MatSnackBar } from '@angular/material/snack-bar';

@Component({
  selector: 'app-cv-management',
  templateUrl: './cv-management.component.html',
  styleUrls: ['./cv-management.component.scss']
})
export class CvManagementComponent implements OnInit {
  selectedTab = 0;
  showCvEditor = false;
  showCvPreview = false;
  showJobSearch = false;
  currentCvData: CVData | null = null;
  selectedTemplateId = 1;
  savedJobs: Job[] = [];
  applications: any[] = [];

  // CV data will be loaded from API in the future


  constructor(
    private router: Router,
    private snackBar: MatSnackBar
  ) {}

  ngOnInit(): void {
    // TODO: Load CV data from API
    this.currentCvData = null;
  }

  goBack(): void {
    this.router.navigate(['/dashboard']);
  }

  onTabChange(index: number): void {
    this.selectedTab = index;
  }

  openCvEditor(): void {
    this.showCvEditor = true;
    this.showCvPreview = false;
    this.showJobSearch = false;
  }

  openCvPreview(): void {
    this.showCvPreview = true;
    this.showCvEditor = false;
    this.showJobSearch = false;
  }

  openJobSearch(): void {
    this.showJobSearch = true;
    this.showCvEditor = false;
    this.showCvPreview = false;
  }

  onCvSave(data: { data: CVData; templateId: number }): void {
    this.currentCvData = data.data;
    this.selectedTemplateId = data.templateId;
    this.showCvEditor = false;
    this.snackBar.open('CV saved successfully!', 'Close', {
      duration: 3000
    });
  }

  onCvPreview(): void {
    this.openCvPreview();
  }

  onCvExport(): void {
    // In a real implementation, this would generate and download a PDF
    this.snackBar.open('PDF export functionality will be implemented here', 'Close', {
      duration: 3000
    });
  }

  onCvEdit(): void {
    this.openCvEditor();
  }

  onCvClose(): void {
    this.showCvPreview = false;
  }

  onJobApply(job: Job): void {
    // In a real implementation, this would open an application form
    this.applications.push({
      job: job,
      appliedDate: new Date(),
      status: 'Applied'
    });
    this.snackBar.open(`Application submitted for ${job.title}`, 'Close', {
      duration: 3000
    });
  }

  onJobSave(job: Job): void {
    if (!this.savedJobs.find(j => j.id === job.id)) {
      this.savedJobs.push(job);
      this.snackBar.open(`Job saved: ${job.title}`, 'Close', {
        duration: 2000
      });
    } else {
      this.snackBar.open('Job already saved', 'Close', {
        duration: 2000
      });
    }
  }

  removeSavedJob(jobId: string): void {
    this.savedJobs = this.savedJobs.filter(job => job.id !== parseInt(jobId));
    this.snackBar.open('Job removed from saved list', 'Close', {
      duration: 2000
    });
  }

  getApplicationStats(): any {
    const total = this.applications.length;
    const pending = this.applications.filter(app => app.status === 'Applied').length;
    const interviews = this.applications.filter(app => app.status === 'Interview').length;
    const offers = this.applications.filter(app => app.status === 'Offer').length;
    const rejected = this.applications.filter(app => app.status === 'Rejected').length;

    return { total, pending, interviews, offers, rejected };
  }

  getMostAppliedCategories(): any[] {
    const categories = this.applications.map(app => app.job.category);
    const categoryCount = categories.reduce((acc, category) => {
      acc[category] = (acc[category] || 0) + 1;
      return acc;
    }, {} as any);

    return Object.entries(categoryCount)
      .map(([category, count]) => ({ category, count }))
      .sort((a, b) => (b.count as number) - (a.count as number))
      .slice(0, 5);
  }

  getStatusBadgeClass(status: string): string {
    switch (status) {
      case 'Applied':
        return 'bg-primary';
      case 'Interview':
        return 'bg-warning';
      case 'Offer':
        return 'bg-success';
      case 'Rejected':
        return 'bg-danger';
      default:
        return 'bg-secondary';
    }
  }
} 