import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Job } from '../../components/job-search/job-search.component';

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

  // Mock data for applied jobs
  mockAppliedJobs: AppliedJob[] = [
    {
      id: '1',
      title: 'Senior Frontend Developer',
      company: 'TechCorp Inc.',
      location: 'New York, NY',
      description: 'We are looking for a senior frontend developer with expertise in Angular, React, and modern web technologies.',
      salary_min: 80000,
      salary_max: 120000,
      salary_currency: 'USD',
      category: 'IT & Telecoms',
      url: 'https://example.com/job1',
      created: '2024-01-15',
      contract_time: 'full_time',
      contract_type: 'permanent',
      appliedDate: '2024-01-20',
      status: 'interviewing',
      notes: 'First interview scheduled for next week',
      followUpDate: '2024-01-27'
    },
    {
      id: '2',
      title: 'Full Stack Developer',
      company: 'StartupXYZ',
      location: 'San Francisco, CA',
      description: 'Join our fast-growing startup as a full stack developer. Experience with Node.js, React, and cloud platforms required.',
      salary_min: 90000,
      salary_max: 140000,
      salary_currency: 'USD',
      category: 'IT & Telecoms',
      url: 'https://example.com/job2',
      created: '2024-01-14',
      contract_time: 'full_time',
      contract_type: 'permanent',
      appliedDate: '2024-01-18',
      status: 'applied',
      notes: 'Application submitted, waiting for response'
    },
    {
      id: '3',
      title: 'DevOps Engineer',
      company: 'Enterprise Solutions',
      location: 'Austin, TX',
      description: 'Looking for a DevOps engineer to help us scale our infrastructure and improve our deployment processes.',
      salary_min: 85000,
      salary_max: 130000,
      salary_currency: 'USD',
      category: 'IT & Telecoms',
      url: 'https://example.com/job3',
      created: '2024-01-13',
      contract_time: 'full_time',
      contract_type: 'permanent',
      appliedDate: '2024-01-16',
      status: 'rejected',
      notes: 'Position filled internally'
    },
    {
      id: '4',
      title: 'UI/UX Designer',
      company: 'Design Studio',
      location: 'Los Angeles, CA',
      description: 'Creative UI/UX designer needed to create beautiful and functional user interfaces for web and mobile applications.',
      salary_min: 70000,
      salary_max: 110000,
      salary_currency: 'USD',
      category: 'Creative & Design',
      url: 'https://example.com/job4',
      created: '2024-01-12',
      contract_time: 'full_time',
      contract_type: 'permanent',
      appliedDate: '2024-01-15',
      status: 'offered',
      notes: 'Offer received, considering terms'
    },
    {
      id: '5',
      title: 'Data Scientist',
      company: 'Analytics Corp',
      location: 'Boston, MA',
      description: 'Join our data science team to build machine learning models and analyze large datasets.',
      salary_min: 95000,
      salary_max: 150000,
      salary_currency: 'USD',
      category: 'Science & Research',
      url: 'https://example.com/job5',
      created: '2024-01-11',
      contract_time: 'full_time',
      contract_type: 'permanent',
      appliedDate: '2024-01-14',
      status: 'withdrawn',
      notes: 'Accepted another offer'
    }
  ];

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
    this.appliedJobs = [...this.mockAppliedJobs];
    this.filteredJobs = [...this.appliedJobs];
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
    if (job.salary_min && job.salary_max) {
      return `$${job.salary_min.toLocaleString()} - $${job.salary_max.toLocaleString()} ${job.salary_currency}`;
    } else if (job.salary_min) {
      return `$${job.salary_min.toLocaleString()}+ ${job.salary_currency}`;
    } else if (job.salary_max) {
      return `Up to $${job.salary_max.toLocaleString()} ${job.salary_currency}`;
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
      const responseDate = new Date(job.created);
      const diffTime = Math.abs(responseDate.getTime() - appliedDate.getTime());
      const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
      return sum + diffDays;
    }, 0);
    
    return Math.round(totalDays / jobsWithResponse.length);
  }
} 