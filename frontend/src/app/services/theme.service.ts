import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

export interface ThemeConfig {
  name: 'light' | 'dark';
  primary: string;
  secondary: string;
  background: string;
  surface: string;
  text: string;
  textSecondary: string;
  border: string;
  shadow: string;
}

@Injectable({
  providedIn: 'root'
})
export class ThemeService {
  private currentTheme = new BehaviorSubject<ThemeConfig>(this.getLightTheme());
  public theme$ = this.currentTheme.asObservable();

  private readonly THEME_KEY = 'cv-revamp-theme';

  constructor() {
    this.loadSavedTheme();
  }

  private getLightTheme(): ThemeConfig {
    return {
      name: 'light',
      primary: '#007bff',
      secondary: '#6c757d',
      background: '#ffffff',
      surface: '#f8f9fa',
      text: '#2c3e50',
      textSecondary: '#6c757d',
      border: '#e9ecef',
      shadow: 'rgba(0, 0, 0, 0.1)'
    };
  }

  private getDarkTheme(): ThemeConfig {
    return {
      name: 'dark',
      primary: '#4dabf7',
      secondary: '#adb5bd',
      background: '#1a1a1a',
      surface: '#2d2d2d',
      text: '#ffffff',
      textSecondary: '#adb5bd',
      border: '#404040',
      shadow: 'rgba(0, 0, 0, 0.3)'
    };
  }

  private loadSavedTheme(): void {
    const savedTheme = localStorage.getItem(this.THEME_KEY);
    if (savedTheme) {
      const theme = JSON.parse(savedTheme);
      this.currentTheme.next(theme);
      this.applyTheme(theme);
    }
  }

  toggleTheme(): void {
    const currentTheme = this.currentTheme.value;
    const newTheme = currentTheme.name === 'light' ? this.getDarkTheme() : this.getLightTheme();
    
    this.currentTheme.next(newTheme);
    this.applyTheme(newTheme);
    localStorage.setItem(this.THEME_KEY, JSON.stringify(newTheme));
  }

  setTheme(themeName: 'light' | 'dark'): void {
    const theme = themeName === 'light' ? this.getLightTheme() : this.getDarkTheme();
    this.currentTheme.next(theme);
    this.applyTheme(theme);
    localStorage.setItem(this.THEME_KEY, JSON.stringify(theme));
  }

  private applyTheme(theme: ThemeConfig): void {
    const root = document.documentElement;
    
    // Set CSS custom properties
    root.style.setProperty('--primary-color', theme.primary);
    root.style.setProperty('--secondary-color', theme.secondary);
    root.style.setProperty('--background-color', theme.background);
    root.style.setProperty('--surface-color', theme.surface);
    root.style.setProperty('--text-color', theme.text);
    root.style.setProperty('--text-secondary-color', theme.textSecondary);
    root.style.setProperty('--border-color', theme.border);
    root.style.setProperty('--shadow-color', theme.shadow);
    
    // Add/remove dark class for Material Design
    if (theme.name === 'dark') {
      document.body.classList.add('dark-theme');
    } else {
      document.body.classList.remove('dark-theme');
    }
  }

  getCurrentTheme(): ThemeConfig {
    return this.currentTheme.value;
  }
} 