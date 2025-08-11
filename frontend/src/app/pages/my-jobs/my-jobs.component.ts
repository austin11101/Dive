import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Job } from '../../services/job.service';

export interface AppliedJob extends Job {
  appliedDate: string;
  status: 'applied' | 'interviewing' | 'offered' | 'rejected' | 'withdrawn';
  notes?: string;
  followUpDate?: string;
}

@Component({
  selector: 'app-my-jobs',
  templateUrl: './my-jobs.component.html',
  styleUrls: ['./my-jobs.component.scss']
})
export class MyJobsComponent implements OnInit {
  appliedJobs: AppliedJob[] = [];
  filteredJobs: AppliedJob[] = [];
  selectedStatus: string = 'all';
  searchTerm: string = '';
  isLoading = false;

  // Applied jobs will be loaded from API in the future


  statusOptions = [
    { value: 'all', label: 'All Applications' },
    { value: 'applied', label: 'Applied' },
    { value: 'interviewing', label: 'Interviewing' },
    { value: 'offered', label: 'Offered' },
    { value: 'rejected', label: 'Rejected' },
    { value: 'withdrawn', label: 'Withdrawn' }
  ];

  constructor(
    private router: Router,
    private snackBar: MatSnackBar
  ) {}

  ngOnInit(): void {
    this.loadAppliedJobs();
  }

  loadAppliedJobs(): void {
    // TODO: Load applied jobs from API
    this.appliedJobs = [];
    this.filteredJobs = [];
  }

  filterJobs(): void {
    this.filteredJobs = this.appliedJobs.filter(job => {
      const matchesStatus = this.selectedStatus === 'all' || job.status === this.selectedStatus;
      const matchesSearch = !this.searchTerm || 
        job.title.toLowerCase().includes(this.searchTerm.toLowerCase()) ||
        job.company.toLowerCase().includes(this.searchTerm.toLowerCase()) ||
        job.location.toLowerCase().includes(this.searchTerm.toLowerCase());
      
      return matchesStatus && matchesSearch;
    });
  }

  onStatusChange(): void {
    this.filterJobs();
  }

  onSearchChange(): void {
    this.filterJobs();
  }

  getStatusBadgeClass(status: string): string {
    switch (status) {
      case 'applied': return 'badge bg-primary';
      case 'interviewing': return 'badge bg-warning';
      case 'offered': return 'badge bg-success';
      case 'rejected': return 'badge bg-danger';
      case 'withdrawn': return 'badge bg-secondary';
      default: return 'badge bg-primary';
    }
  }

  getStatusLabel(status: string): string {
    switch (status) {
      case 'applied': return 'Applied';
      case 'interviewing': return 'Interviewing';
      case 'offered': return 'Offered';
      case 'rejected': return 'Rejected';
      case 'withdrawn': return 'Withdrawn';
      default: return 'Applied';
    }
  }

  formatDate(dateString: string): string {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
  }

  formatSalary(job: Job): string {
    if (job.salary) {
      return job.salary;
    }
    return 'Salary not specified';
  }

  updateJobStatus(job: AppliedJob, newStatus: string): void {
    job.status = newStatus as any;
    this.snackBar.open(`Status updated to ${this.getStatusLabel(newStatus)}`, 'Close', {
      duration: 2000
    });
  }

  addNote(job: AppliedJob, note: string): void {
    if (note.trim()) {
      job.notes = note;
      this.snackBar.open('Note added successfully', 'Close', {
        duration: 2000
      });
    }
  }

  setFollowUpDate(job: AppliedJob, date: string): void {
    job.followUpDate = date;
    this.snackBar.open('Follow-up date set', 'Close', {
      duration: 2000
    });
  }

  withdrawApplication(job: AppliedJob): void {
    job.status = 'withdrawn';
    this.snackBar.open('Application withdrawn', 'Close', {
      duration: 2000
    });
  }

  searchMoreJobs(): void {
    this.router.navigate(['/cv-management'], { queryParams: { tab: 'job-search' } });
  }

  goBack(): void {
    this.router.navigate(['/dashboard']);
  }

  getApplicationStats(): any {
    const stats = {
      total: this.appliedJobs.length,
      applied: this.appliedJobs.filter(job => job.status === 'applied').length,
      interviewing: this.appliedJobs.filter(job => job.status === 'interviewing').length,
      offered: this.appliedJobs.filter(job => job.status === 'offered').length,
      rejected: this.appliedJobs.filter(job => job.status === 'rejected').length,
      withdrawn: this.appliedJobs.filter(job => job.status === 'withdrawn').length
    };
    return stats;
  }

  getResponseRate(): number {
    const responded = this.appliedJobs.filter(job => 
      job.status === 'interviewing' || job.status === 'offered' || job.status === 'rejected'
    ).length;
    return this.appliedJobs.length > 0 ? Math.round((responded / this.appliedJobs.length) * 100) : 0;
  }

  getAverageResponseTime(): number {
    const jobsWithResponse = this.appliedJobs.filter(job => 
      job.status === 'interviewing' || job.status === 'offered' || job.status === 'rejected'
    );
    
    if (jobsWithResponse.length === 0) return 0;
    
    const totalDays = jobsWithResponse.reduce((sum, job) => {
      const appliedDate = new Date(job.appliedDate);
      const responseDate = new Date(job.created_at);
      const diffTime = Math.abs(responseDate.getTime() - appliedDate.getTime());
      const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
      return sum + diffDays;
    }, 0);
    
    return Math.round(totalDays / jobsWithResponse.length);
  }
} 