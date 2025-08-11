import { Component, OnInit, OnDestroy } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { MatSnackBar } from '@angular/material/snack-bar';
import { firstValueFrom, Subject, takeUntil } from 'rxjs';
import { JobService, Job, JobSearchFilters } from '../../services/job.service';
import { EnhancedJobService } from '../../services/enhanced-job.service';

@Component({
  selector: 'app-job-search',
  templateUrl: './job-search.component.html',
  styleUrls: ['./job-search.component.scss']
})
export class JobSearchComponent implements OnInit, OnDestroy {
  searchForm: FormGroup;
  jobs: Job[] = [];
  filteredJobs: Job[] = [];
  isLoading = false;
  currentPage = 1;
  jobsPerPage = 10;
  totalJobs = 0;
  
  private destroy$ = new Subject<void>();

  searchFilters: JobSearchFilters = {};

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
    private jobService: JobService,
    private enhancedJobService: EnhancedJobService,
    private snackBar: MatSnackBar
  ) {
    this.searchForm = this.createForm();
  }

  ngOnInit(): void {
    this.loadJobs();
    this.enhancedJobService.isLoading('getJobs')
      .pipe(takeUntil(this.destroy$))
      .subscribe(loading => {
        this.isLoading = loading;
      });
  }

  ngOnDestroy(): void {
    this.destroy$.next();
    this.destroy$.complete();
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

  loadJobs(): void {
    this.enhancedJobService.getJobs({ limit: 50 })
      .pipe(takeUntil(this.destroy$))
      .subscribe({
        next: (jobs) => {
          this.jobs = jobs;
          this.filteredJobs = [...this.jobs];
          this.totalJobs = this.jobs.length;
          console.log(`Loaded ${jobs.length} jobs from database`);
        },
        error: (error) => {
          console.error('Error loading jobs:', error);
          this.snackBar.open('Error loading jobs. Please try again.', 'Close', {
            duration: 3000
          });
        }
      });
  }

  async searchJobs(): Promise<void> {
    if (this.searchForm.valid) {
      this.isLoading = true;
      const formValues = this.searchForm.value;

      try {
        await this.scrapeJobs(formValues.keywords, formValues.location);

        const filters: JobSearchFilters = {
          limit: 100
        };

        if (formValues.keywords) {
          filters.search = formValues.keywords;
        }
        if (formValues.location) {
          filters.location = formValues.location;
        }

        this.enhancedJobService.getJobs(filters)
          .pipe(takeUntil(this.destroy$))
          .subscribe({
            next: (jobs) => {
              this.jobs = jobs;
              this.applyClientSideFilters(formValues);
              this.snackBar.open(`Found ${this.totalJobs} jobs`, 'Close', {
                duration: 3000
              });
            },
            error: (error) => {
              console.error('Error searching jobs:', error);
              this.snackBar.open('Error searching jobs. Please try again.', 'Close', {
                duration: 3000
              });
            }
          });
      } catch (error) {
        console.error('Error searching jobs:', error);
        this.snackBar.open('Error searching jobs. Please try again.', 'Close', {
          duration: 3000
        });
        this.isLoading = false;
      }
    } else {
      this.snackBar.open('Please enter keywords to search', 'Close', {
        duration: 3000
      });
    }
  }

  async scrapeJobs(query: string = 'software developer', location: string = 'South Africa'): Promise<void> {
    try {
      const response = await firstValueFrom(
        this.enhancedJobService.scrapeJobs(query, location, 20)
          .pipe(takeUntil(this.destroy$))
      );
      console.log('Scraping response:', response);

      if (response && response.scraped_count > 0) {
        this.snackBar.open(`Scraped ${response.scraped_count} new jobs! Saved ${response.saved_count} to database.`, 'Close', {
          duration: 5000
        });
      } else {
        this.snackBar.open('No new jobs found for this search.', 'Close', {
          duration: 3000
        });
      }
    } catch (error) {
      console.error('Error scraping jobs:', error);
      this.snackBar.open('Unable to scrape new jobs at this time.', 'Close', {
        duration: 3000
      });
    }
  }

  async viewAllJobs(): Promise<void> {
    this.isLoading = true;

    try {
      await this.scrapeJobs('software developer', 'South Africa');
      await this.scrapeJobs('data analyst', 'Johannesburg');
      await this.scrapeJobs('marketing', 'Cape Town');
      this.loadJobs();
    } catch (error) {
      console.error('Error loading jobs:', error);
      this.loadJobs();
    }
  }

  private applyClientSideFilters(formValues: any): void {
    let filtered = this.jobs.filter(job => {
      const matchesCategory = formValues.category === 'All Categories' ||
        job.job_type?.toLowerCase().includes(formValues.category.toLowerCase());

      const matchesContractType = formValues.contract_type === 'All Types' ||
        job.job_type?.toLowerCase().includes(formValues.contract_type.toLowerCase());

      return matchesCategory && matchesContractType;
    });

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
    window.open(job.link, '_blank');
    this.snackBar.open(`Application submitted for ${job.title} at ${job.company}`, 'Close', {
      duration: 3000
    });
  }

  saveJob(job: Job): void {
    this.snackBar.open(`Job saved: ${job.title}`, 'Close', {
      duration: 2000
    });
  }

  shareJob(job: Job): void {
    if (navigator.share) {
      navigator.share({
        title: job.title,
        text: `Check out this job: ${job.title} at ${job.company}`,
        url: job.link
      });
    } else {
      navigator.clipboard.writeText(`${job.title} at ${job.company}: ${job.link}`);
      this.snackBar.open('Job link copied to clipboard', 'Close', {
        duration: 2000
      });
    }
  }

  formatSalary(job: Job): string {
    if (job.salary) {
      return job.salary;
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
    this.loadJobs();
  }
}
