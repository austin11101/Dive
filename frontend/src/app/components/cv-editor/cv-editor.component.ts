import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';
import { FormBuilder, FormGroup, FormArray, Validators } from '@angular/forms';
import { MatSnackBar } from '@angular/material/snack-bar';

export interface CVData {
  personalInfo: {
    firstName: string;
    lastName: string;
    email: string;
    phone: string;
    address: string;
    linkedin: string;
    website: string;
    summary: string;
  };
  experience: Array<{
    company: string;
    position: string;
    startDate: string;
    endDate: string;
    current: boolean;
    description: string;
  }>;
  education: Array<{
    institution: string;
    degree: string;
    field: string;
    startDate: string;
    endDate: string;
    gpa: string;
  }>;
  skills: Array<{
    name: string;
    level: string;
  }>;
  projects: Array<{
    name: string;
    description: string;
    technologies: string;
    url: string;
  }>;
  certifications: Array<{
    name: string;
    issuer: string;
    date: string;
    url: string;
  }>;
  languages: Array<{
    language: string;
    proficiency: string;
  }>;
}

@Component({
  selector: 'app-cv-editor',
  templateUrl: './cv-editor.component.html',
  styleUrls: ['./cv-editor.component.scss']
})
export class CvEditorComponent implements OnInit {
  @Input() cvData: CVData | null = null;
  @Input() templateId: number = 1;
  @Output() save = new EventEmitter<{ data: CVData; templateId: number }>();
  @Output() preview = new EventEmitter<CVData>();
  @Output() export = new EventEmitter<CVData>();

  cvForm: FormGroup;
  isSubmitting = false;

  skillLevels = ['Beginner', 'Intermediate', 'Advanced', 'Expert'];
  languageLevels = ['Basic', 'Conversational', 'Fluent', 'Native'];
  templates = [
    { id: 1, name: 'Professional', description: 'Clean and modern design' },
    { id: 2, name: 'Creative', description: 'Bold and colorful layout' },
    { id: 3, name: 'Minimal', description: 'Simple and elegant' },
    { id: 4, name: 'Corporate', description: 'Traditional business style' }
  ];

  constructor(
    private fb: FormBuilder,
    private snackBar: MatSnackBar
  ) {
    this.cvForm = this.createForm();
  }

  ngOnInit(): void {
    if (this.cvData) {
      this.loadCVData(this.cvData);
    }
  }

  createForm(): FormGroup {
    return this.fb.group({
      personalInfo: this.fb.group({
        firstName: ['', Validators.required],
        lastName: ['', Validators.required],
        email: ['', [Validators.required, Validators.email]],
        phone: ['', Validators.required],
        address: [''],
        linkedin: [''],
        website: [''],
        summary: ['', Validators.required]
      }),
      experience: this.fb.array([]),
      education: this.fb.array([]),
      skills: this.fb.array([]),
      projects: this.fb.array([]),
      certifications: this.fb.array([]),
      languages: this.fb.array([])
    });
  }

  loadCVData(data: CVData): void {
    this.cvForm.patchValue({
      personalInfo: data.personalInfo
    });

    // Load arrays
    this.loadFormArray('experience', data.experience);
    this.loadFormArray('education', data.education);
    this.loadFormArray('skills', data.skills);
    this.loadFormArray('projects', data.projects);
    this.loadFormArray('certifications', data.certifications);
    this.loadFormArray('languages', data.languages);
  }

  loadFormArray(arrayName: string, data: any[]): void {
    const array = this.cvForm.get(arrayName) as FormArray;
    array.clear();
    data.forEach(item => {
      array.push(this.fb.group(item));
    });
  }

  // Experience methods
  get experienceArray(): FormArray {
    return this.cvForm.get('experience') as FormArray;
  }

  addExperience(): void {
    const experience = this.fb.group({
      company: ['', Validators.required],
      position: ['', Validators.required],
      startDate: ['', Validators.required],
      endDate: [''],
      current: [false],
      description: ['', Validators.required]
    });
    this.experienceArray.push(experience);
  }

  removeExperience(index: number): void {
    this.experienceArray.removeAt(index);
  }

  // Education methods
  get educationArray(): FormArray {
    return this.cvForm.get('education') as FormArray;
  }

  addEducation(): void {
    const education = this.fb.group({
      institution: ['', Validators.required],
      degree: ['', Validators.required],
      field: ['', Validators.required],
      startDate: ['', Validators.required],
      endDate: [''],
      gpa: ['']
    });
    this.educationArray.push(education);
  }

  removeEducation(index: number): void {
    this.educationArray.removeAt(index);
  }

  // Skills methods
  get skillsArray(): FormArray {
    return this.cvForm.get('skills') as FormArray;
  }

  addSkill(): void {
    const skill = this.fb.group({
      name: ['', Validators.required],
      level: ['Intermediate', Validators.required]
    });
    this.skillsArray.push(skill);
  }

  removeSkill(index: number): void {
    this.skillsArray.removeAt(index);
  }

  // Projects methods
  get projectsArray(): FormArray {
    return this.cvForm.get('projects') as FormArray;
  }

  addProject(): void {
    const project = this.fb.group({
      name: ['', Validators.required],
      description: ['', Validators.required],
      technologies: [''],
      url: ['']
    });
    this.projectsArray.push(project);
  }

  removeProject(index: number): void {
    this.projectsArray.removeAt(index);
  }

  // Certifications methods
  get certificationsArray(): FormArray {
    return this.cvForm.get('certifications') as FormArray;
  }

  addCertification(): void {
    const certification = this.fb.group({
      name: ['', Validators.required],
      issuer: ['', Validators.required],
      date: ['', Validators.required],
      url: ['']
    });
    this.certificationsArray.push(certification);
  }

  removeCertification(index: number): void {
    this.certificationsArray.removeAt(index);
  }

  // Languages methods
  get languagesArray(): FormArray {
    return this.cvForm.get('languages') as FormArray;
  }

  addLanguage(): void {
    const language = this.fb.group({
      language: ['', Validators.required],
      proficiency: ['Conversational', Validators.required]
    });
    this.languagesArray.push(language);
  }

  removeLanguage(index: number): void {
    this.languagesArray.removeAt(index);
  }

  onSave(): void {
    if (this.cvForm.valid) {
      this.isSubmitting = true;
      const formData = this.cvForm.value as CVData;
      
      this.save.emit({
        data: formData,
        templateId: this.templateId
      });

      this.snackBar.open('CV saved successfully!', 'Close', {
        duration: 3000
      });
      this.isSubmitting = false;
    } else {
      this.markFormGroupTouched();
      this.snackBar.open('Please fill in all required fields', 'Close', {
        duration: 3000
      });
    }
  }

  onPreview(): void {
    if (this.cvForm.valid) {
      const formData = this.cvForm.value as CVData;
      this.preview.emit(formData);
    } else {
      this.markFormGroupTouched();
      this.snackBar.open('Please fill in all required fields', 'Close', {
        duration: 3000
      });
    }
  }

  onExport(): void {
    if (this.cvForm.valid) {
      const formData = this.cvForm.value as CVData;
      this.export.emit(formData);
    } else {
      this.markFormGroupTouched();
      this.snackBar.open('Please fill in all required fields', 'Close', {
        duration: 3000
      });
    }
  }

  markFormGroupTouched(): void {
    Object.keys(this.cvForm.controls).forEach(key => {
      const control = this.cvForm.get(key);
      if (control instanceof FormGroup) {
        Object.keys(control.controls).forEach(subKey => {
          control.get(subKey)?.markAsTouched();
        });
      } else {
        control?.markAsTouched();
      }
    });
  }
} 