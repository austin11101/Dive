import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.scss']
})
export class DashboardComponent implements OnInit {
  selectedTab = 0;
  isSidebarOpen = true;
  userInfo: any = null;

  constructor(private router: Router) {}

  ngOnInit(): void {
    // Get user info from localStorage
    const userInfoStr = localStorage.getItem('user_info');
    if (userInfoStr) {
      this.userInfo = JSON.parse(userInfoStr);
    }
  }

  // Mock data for dashboard
  recentCVs = [
    {
      id: 1,
      title: 'Software Engineer CV',
      lastModified: '2024-01-15',
      status: 'Draft',
      template: 'Modern Blue'
    },
    {
      id: 2,
      title: 'Marketing Manager CV',
      lastModified: '2024-01-10',
      status: 'Complete',
      template: 'Professional Gray'
    },
    {
      id: 3,
      title: 'Data Scientist CV',
      lastModified: '2024-01-08',
      status: 'Draft',
      template: 'Creative Orange'
    }
  ];

  templates = [
    {
      id: 1,
      name: 'Modern Blue',
      category: 'Professional',
      preview: 'assets/template1.jpg',
      isPopular: true
    },
    {
      id: 2,
      name: 'Professional Gray',
      category: 'Corporate',
      preview: 'assets/template2.jpg',
      isPopular: false
    },
    {
      id: 3,
      name: 'Creative Orange',
      category: 'Creative',
      preview: 'assets/template3.jpg',
      isPopular: true
    },
    {
      id: 4,
      name: 'Minimalist White',
      category: 'Minimal',
      preview: 'assets/template4.jpg',
      isPopular: false
    }
  ];

  stats = {
    totalCVs: 12,
    completedCVs: 8,
    templatesUsed: 6,
    lastActivity: '2 hours ago'
  };

  toggleSidebar(): void {
    this.isSidebarOpen = !this.isSidebarOpen;
  }

  createNewCV(): void {
    // TODO: Implement new CV creation
    console.log('Creating new CV...');
  }

  openCV(cvId: number): void {
    // TODO: Implement CV opening
    console.log('Opening CV:', cvId);
  }

  selectTemplate(templateId: number): void {
    // TODO: Implement template selection
    console.log('Selected template:', templateId);
  }

  exportCV(cvId: number, format: string): void {
    // TODO: Implement CV export
    console.log('Exporting CV:', cvId, 'in format:', format);
  }

  deleteCV(cvId: number): void {
    // TODO: Implement CV deletion
    console.log('Deleting CV:', cvId);
  }

  logout(): void {
    localStorage.removeItem('auth_token');
    localStorage.removeItem('user_info');
    this.router.navigate(['/']);
  }

  getStatusClass(status: string): string {
    switch (status.toLowerCase()) {
      case 'draft':
        return 'bg-secondary';
      case 'complete':
      case 'completed':
        return 'bg-success';
      case 'in-progress':
        return 'bg-warning';
      default:
        return 'bg-primary';
    }
  }
} 