import { Component, Input, Output, EventEmitter } from '@angular/core';
import { CVData } from '../cv-editor/cv-editor.component';

@Component({
  selector: 'app-cv-preview',
  templateUrl: './cv-preview.component.html',
  styleUrls: ['./cv-preview.component.scss']
})
export class CvPreviewComponent {
  @Input() cvData: CVData | null = null;
  @Input() templateId: number = 1;
  @Output() edit = new EventEmitter<void>();
  @Output() export = new EventEmitter<void>();
  @Output() close = new EventEmitter<void>();

  templates = [
    { id: 1, name: 'Professional', class: 'template-professional' },
    { id: 2, name: 'Creative', class: 'template-creative' },
    { id: 3, name: 'Minimal', class: 'template-minimal' },
    { id: 4, name: 'Corporate', class: 'template-corporate' }
  ];

  get currentTemplate() {
    return this.templates.find(t => t.id === this.templateId) || this.templates[0];
  }

  formatDate(dateString: string): string {
    if (!dateString) return '';
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { year: 'numeric', month: 'long' });
  }

  getFullName(): string {
    if (!this.cvData?.personalInfo) return '';
    const { firstName, lastName } = this.cvData.personalInfo;
    return `${firstName} ${lastName}`.trim();
  }

  getContactInfo(): string[] {
    if (!this.cvData?.personalInfo) return [];
    const info = [];
    const { email, phone, address, linkedin, website } = this.cvData.personalInfo;
    
    if (email) info.push(email);
    if (phone) info.push(phone);
    if (address) info.push(address);
    if (linkedin) info.push(`LinkedIn: ${linkedin}`);
    if (website) info.push(`Website: ${website}`);
    
    return info;
  }

  onEdit(): void {
    this.edit.emit();
  }

  onExport(): void {
    this.export.emit();
  }

  onClose(): void {
    this.close.emit();
  }

  printCV(): void {
    window.print();
  }
} 