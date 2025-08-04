import { Component, OnInit } from '@angular/core';
import { CVData } from '../../components/cv-editor/cv-editor.component';
import { Job } from '../../components/job-search/job-search.component';
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

  // Mock CV data
  mockCvData: CVData = {
    personalInfo: {
      firstName: 'John',
      lastName: 'Doe',
      email: 'john.doe@example.com',
      phone: '+1 (555) 123-4567',
      address: '123 Main Street, New York, NY 10001',
      linkedin: 'linkedin.com/in/johndoe',
      website: 'johndoe.dev',
      summary: 'Experienced full-stack developer with 5+ years of expertise in modern web technologies including Angular, React, Node.js, and cloud platforms. Passionate about creating scalable, user-friendly applications and leading development teams.'
    },
    experience: [
      {
        company: 'TechCorp Inc.',
        position: 'Senior Full Stack Developer',
        startDate: '2022-01',
        endDate: '',
        current: true,
        description: 'Lead development of enterprise web applications using Angular, Node.js, and AWS. Mentored junior developers and implemented CI/CD pipelines.'
      },
      {
        company: 'StartupXYZ',
        position: 'Frontend Developer',
        startDate: '2020-03',
        endDate: '2021-12',
        current: false,
        description: 'Built responsive web applications using React and TypeScript. Collaborated with design team to implement pixel-perfect UI components.'
      }
    ],
    education: [
      {
        institution: 'University of Technology',
        degree: 'Bachelor of Science',
        field: 'Computer Science',
        startDate: '2016-09',
        endDate: '2020-05',
        gpa: '3.8/4.0'
      }
    ],
    skills: [
      { name: 'Angular', level: 'Expert' },
      { name: 'React', level: 'Advanced' },
      { name: 'Node.js', level: 'Advanced' },
      { name: 'TypeScript', level: 'Expert' },
      { name: 'Python', level: 'Intermediate' },
      { name: 'AWS', level: 'Advanced' }
    ],
    projects: [
      {
        name: 'E-commerce Platform',
        description: 'Built a full-stack e-commerce platform with Angular frontend and Node.js backend. Implemented payment processing and inventory management.',
        technologies: 'Angular, Node.js, MongoDB, Stripe',
        url: 'https://github.com/johndoe/ecommerce'
      },
      {
        name: 'Task Management App',
        description: 'Developed a collaborative task management application with real-time updates and team collaboration features.',
        technologies: 'React, Socket.io, Express.js',
        url: 'https://github.com/johndoe/taskmanager'
      }
    ],
    certifications: [
      {
        name: 'AWS Certified Developer',
        issuer: 'Amazon Web Services',
        date: '2023-06',
        url: 'https://aws.amazon.com/certification/'
      },
      {
        name: 'Angular Certification',
        issuer: 'Google',
        date: '2022-12',
        url: 'https://angular.io/'
      }
    ],
    languages: [
      { language: 'English', proficiency: 'Native' },
      { language: 'Spanish', proficiency: 'Fluent' },
      { language: 'French', proficiency: 'Conversational' }
    ]
  };

  constructor(private snackBar: MatSnackBar) {}

  ngOnInit(): void {
    // Load mock data
    this.currentCvData = this.mockCvData;
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
    this.savedJobs = this.savedJobs.filter(job => job.id !== jobId);
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