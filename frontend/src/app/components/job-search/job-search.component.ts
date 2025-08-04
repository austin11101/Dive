import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import { MatSnackBar } from '@angular/material/snack-bar';

export interface Job {
  id: string;
  title: string;
  company: string;
  location: string;
  description: string;
  salary_min?: number;
  salary_max?: number;
  salary_currency?: string;
  category: string;
  url: string;
  created: string;
  contract_time?: string;
  contract_type?: string;
}

export interface JobSearchFilters {
  keywords: string;
  location: string;
  category: string;
  salary_min?: number;
  salary_max?: number;
  contract_type: string;
  distance: number;
}

@Component({
  selector: 'app-job-search',
  templateUrl: './job-search.component.html',
  styleUrls: ['./job-search.component.scss']
})
export class JobSearchComponent implements OnInit {
  searchForm: FormGroup;
  jobs: Job[] = [];
  filteredJobs: Job[] = [];
  isLoading = false;
  currentPage = 1;
  jobsPerPage = 10;
  totalJobs = 0;

  // Mock data for demonstration
  mockJobs: Job[] = [
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
      contract_type: 'permanent'
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
      contract_type: 'permanent'
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
      contract_type: 'permanent'
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
      contract_type: 'permanent'
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
      contract_type: 'permanent'
    }
  ];

  categories = [
    'All Categories',
    'IT & Telecoms',
    'Creative & Design',
    'Science & Research',
    'Marketing & PR',
    'Sales & Business Development',
    'Finance & Accounting',
    'Healthcare',
    'Education',
    'Engineering',
    'Customer Service',
    'Administration'
  ];

  contractTypes = [
    'All Types',
    'permanent',
    'contract',
    'part_time',
    'freelance',
    'internship'
  ];

  distanceOptions = [
    { value: 5, label: '5 miles' },
    { value: 10, label: '10 miles' },
    { value: 25, label: '25 miles' },
    { value: 50, label: '50 miles' },
    { value: 100, label: '100 miles' }
  ];

  constructor(
    private fb: FormBuilder,
    private http: HttpClient,
    private snackBar: MatSnackBar
  ) {
    this.searchForm = this.createForm();
  }

  ngOnInit(): void {
    this.loadMockJobs();
  }

  createForm(): FormGroup {
    return this.fb.group({
      keywords: ['', Validators.required],
      location: [''],
      category: ['All Categories'],
      salary_min: [''],
      salary_max: [''],
      contract_type: ['All Types'],
      distance: [25]
    });
  }

  loadMockJobs(): void {
    this.jobs = [...this.mockJobs];
    this.filteredJobs = [...this.jobs];
    this.totalJobs = this.jobs.length;
  }

  async searchJobs(): Promise<void> {
    if (this.searchForm.valid) {
      this.isLoading = true;
      const filters = this.searchForm.value;

      try {
        // In a real implementation, you would call the actual API
        // For now, we'll simulate API call with mock data
        await this.simulateApiCall(filters);
        
        this.snackBar.open(`Found ${this.totalJobs} jobs`, 'Close', {
          duration: 3000
        });
      } catch (error) {
        this.snackBar.open('Error searching jobs. Please try again.', 'Close', {
          duration: 3000
        });
      } finally {
        this.isLoading = false;
      }
    } else {
      this.snackBar.open('Please enter keywords to search', 'Close', {
        duration: 3000
      });
    }
  }

  private async simulateApiCall(filters: JobSearchFilters): Promise<void> {
    // Simulate API delay
    await new Promise(resolve => setTimeout(resolve, 1000));

    // Filter mock jobs based on search criteria
    let filtered = this.mockJobs.filter(job => {
      const matchesKeywords = !filters.keywords || 
        job.title.toLowerCase().includes(filters.keywords.toLowerCase()) ||
        job.description.toLowerCase().includes(filters.keywords.toLowerCase()) ||
        job.company.toLowerCase().includes(filters.keywords.toLowerCase());

      const matchesLocation = !filters.location || 
        job.location.toLowerCase().includes(filters.location.toLowerCase());

      const matchesCategory = filters.category === 'All Categories' || 
        job.category === filters.category;

      const matchesContractType = filters.contract_type === 'All Types' || 
        job.contract_type === filters.contract_type;

      const matchesSalary = (!filters.salary_min || job.salary_max >= filters.salary_min) &&
        (!filters.salary_max || job.salary_min <= filters.salary_max);

      return matchesKeywords && matchesLocation && matchesCategory && 
             matchesContractType && matchesSalary;
    });

    this.jobs = filtered;
    this.filteredJobs = filtered;
    this.totalJobs = filtered.length;
    this.currentPage = 1;
  }

  get paginatedJobs(): Job[] {
    const startIndex = (this.currentPage - 1) * this.jobsPerPage;
    const endIndex = startIndex + this.jobsPerPage;
    return this.filteredJobs.slice(startIndex, endIndex);
  }

  get totalPages(): number {
    return Math.ceil(this.totalJobs / this.jobsPerPage);
  }

  get pages(): number[] {
    const pages: number[] = [];
    for (let i = 1; i <= this.totalPages; i++) {
      pages.push(i);
    }
    return pages;
  }

  changePage(page: number): void {
    if (page >= 1 && page <= this.totalPages) {
      this.currentPage = page;
    }
  }

  applyToJob(job: Job): void {
    // In a real implementation, this would open an application form
    // or redirect to the job application page
    this.snackBar.open(`Application submitted for ${job.title} at ${job.company}`, 'Close', {
      duration: 3000
    });
  }

  saveJob(job: Job): void {
    // In a real implementation, this would save the job to user's saved jobs
    this.snackBar.open(`Job saved: ${job.title}`, 'Close', {
      duration: 2000
    });
  }

  shareJob(job: Job): void {
    // In a real implementation, this would open a share dialog
    if (navigator.share) {
      navigator.share({
        title: job.title,
        text: `Check out this job: ${job.title} at ${job.company}`,
        url: job.url
      });
    } else {
      // Fallback: copy to clipboard
      navigator.clipboard.writeText(`${job.title} at ${job.company}: ${job.url}`);
      this.snackBar.open('Job link copied to clipboard', 'Close', {
        duration: 2000
      });
    }
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

  formatDate(dateString: string): string {
    const date = new Date(dateString);
    const now = new Date();
    const diffTime = Math.abs(now.getTime() - date.getTime());
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

    if (diffDays === 1) return '1 day ago';
    if (diffDays < 7) return `${diffDays} days ago`;
    if (diffDays < 30) return `${Math.floor(diffDays / 7)} weeks ago`;
    return date.toLocaleDateString();
  }

  formatContractType(type: string): string {
    return type.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase());
  }

  clearFilters(): void {
    this.searchForm.reset({
      keywords: '',
      location: '',
      category: 'All Categories',
      salary_min: '',
      salary_max: '',
      contract_type: 'All Types',
      distance: 25
    });
    this.loadMockJobs();
  }
} 