/**
 * Enhanced Job Service with State Management and Caching
 */

import { Injectable } from '@angular/core';
import { HttpClient, HttpParams, HttpErrorResponse } from '@angular/common/http';
import { BehaviorSubject, Observable, of, throwError, timer, firstValueFrom } from 'rxjs';
import { map, catchError, tap, shareReplay, switchMap, retry, timeout } from 'rxjs/operators';
import { environment } from '../../environments/environment';

// Re-export interfaces from job service
export { Job, JobSearchFilters, ScrapeResponse, JobStats } from './job.service';
import { Job, JobSearchFilters, ScrapeResponse, JobStats } from './job.service';

interface CacheEntry<T> {
  data: T;
  timestamp: number;
  expiry: number;
}

interface LoadingState {
  [key: string]: boolean;
}

interface ErrorState {
  [key: string]: string | null;
}

@Injectable({
  providedIn: 'root'
})
export class EnhancedJobService {
  private apiUrl = `${environment.apiUrl}/api`;
  private cache = new Map<string, CacheEntry<any>>();
  private readonly CACHE_DURATION = 5 * 60 * 1000; // 5 minutes

  // State management
  private loadingSubject = new BehaviorSubject<LoadingState>({});
  private errorSubject = new BehaviorSubject<ErrorState>({});
  private jobsSubject = new BehaviorSubject<Job[]>([]);
  private statsSubject = new BehaviorSubject<JobStats | null>(null);

  // Public observables
  public loading$ = this.loadingSubject.asObservable();
  public errors$ = this.errorSubject.asObservable();
  public jobs$ = this.jobsSubject.asObservable();
  public stats$ = this.statsSubject.asObservable();

  constructor(private http: HttpClient) {}

  // Loading state management
  setLoading(key: string, loading: boolean): void {
    const currentState = this.loadingSubject.value;
    this.loadingSubject.next({ ...currentState, [key]: loading });
  }

  isLoading(key: string): Observable<boolean> {
    return this.loading$.pipe(
      map(state => state[key] || false)
    );
  }

  // Error state management
  setError(key: string, error: string | null): void {
    const currentState = this.errorSubject.value;
    this.errorSubject.next({ ...currentState, [key]: error });
  }

  clearError(key: string): void {
    this.setError(key, null);
  }

  getError(key: string): Observable<string | null> {
    return this.errors$.pipe(
      map(state => state[key] || null)
    );
  }

  // Cache management
  private getCacheKey(method: string, params: any): string {
    return `${method}_${JSON.stringify(params)}`;
  }

  private getFromCache<T>(key: string): T | null {
    const entry = this.cache.get(key);
    if (entry && Date.now() < entry.expiry) {
      return entry.data;
    }
    this.cache.delete(key);
    return null;
  }

  private setCache<T>(key: string, data: T, duration: number = this.CACHE_DURATION): void {
    this.cache.set(key, {
      data,
      timestamp: Date.now(),
      expiry: Date.now() + duration
    });
  }

  // Enhanced HTTP error handling
  private handleError(operation: string) {
    return (error: HttpErrorResponse): Observable<never> => {
      console.error(`${operation} failed:`, error);
      
      let errorMessage = 'An unexpected error occurred';
      
      if (error.error instanceof ErrorEvent) {
        // Client-side error
        errorMessage = `Network error: ${error.error.message}`;
      } else {
        // Server-side error
        switch (error.status) {
          case 0:
            errorMessage = 'Unable to connect to server. Please check your internet connection.';
            break;
          case 400:
            errorMessage = 'Invalid request. Please check your search parameters.';
            break;
          case 404:
            errorMessage = 'Service not found. Please try again later.';
            break;
          case 429:
            errorMessage = 'Too many requests. Please wait a moment before trying again.';
            break;
          case 500:
            errorMessage = 'Server error. Please try again later.';
            break;
          default:
            errorMessage = `Server error (${error.status}): ${error.error?.detail || error.message}`;
        }
      }

      this.setError(operation, errorMessage);
      return throwError(() => new Error(errorMessage));
    };
  }

  // Enhanced API methods
  getJobs(filters: JobSearchFilters = {}): Observable<Job[]> {
    const cacheKey = this.getCacheKey('getJobs', filters);
    const cached = this.getFromCache<Job[]>(cacheKey);
    
    if (cached) {
      this.jobsSubject.next(cached);
      return of(cached);
    }

    this.setLoading('getJobs', true);
    this.clearError('getJobs');

    let params = new HttpParams();
    Object.keys(filters).forEach(key => {
      const value = (filters as any)[key];
      if (value !== null && value !== undefined && value !== '') {
        params = params.set(key, value.toString());
      }
    });

    return this.http.get<Job[]>(`${this.apiUrl}/jobs`, { params }).pipe(
      timeout(30000), // 30 second timeout
      retry(2), // Retry twice on failure
      tap(jobs => {
        this.setCache(cacheKey, jobs);
        this.jobsSubject.next(jobs);
        this.setLoading('getJobs', false);
      }),
      catchError(this.handleError('getJobs')),
      shareReplay(1)
    );
  }

  scrapeJobs(query: string, location: string = 'South Africa', limit: number = 20): Observable<ScrapeResponse> {
    this.setLoading('scrapeJobs', true);
    this.clearError('scrapeJobs');

    const params = new HttpParams()
      .set('query', query)
      .set('location', location)
      .set('limit', limit.toString());

    return this.http.post<ScrapeResponse>(`${this.apiUrl}/scrape`, null, { params }).pipe(
      timeout(60000), // 60 second timeout for scraping
      tap(response => {
        this.setLoading('scrapeJobs', false);
        // Invalidate jobs cache after successful scraping
        this.invalidateJobsCache();
      }),
      catchError(this.handleError('scrapeJobs'))
    );
  }

  scrapeJobsEfficient(
    query: string,
    location: string = 'South Africa',
    keywords: string[] = [],
    maxJobs: number = 20,
    sites: string[] = []
  ): Observable<ScrapeResponse> {
    this.setLoading('scrapeJobsEfficient', true);
    this.clearError('scrapeJobsEfficient');

    const params = new HttpParams()
      .set('query', query)
      .set('location', location)
      .set('keywords', keywords.join(','))
      .set('max_jobs', maxJobs.toString())
      .set('sites', sites.join(','));

    return this.http.post<ScrapeResponse>(`${this.apiUrl}/scrape-efficient`, null, { params }).pipe(
      timeout(90000), // 90 second timeout for efficient scraping
      tap(response => {
        this.setLoading('scrapeJobsEfficient', false);
        this.invalidateJobsCache();
      }),
      catchError(this.handleError('scrapeJobsEfficient'))
    );
  }

  getJobStats(): Observable<JobStats> {
    const cacheKey = this.getCacheKey('getJobStats', {});
    const cached = this.getFromCache<JobStats>(cacheKey);
    
    if (cached) {
      this.statsSubject.next(cached);
      return of(cached);
    }

    this.setLoading('getJobStats', true);
    this.clearError('getJobStats');

    return this.http.get<JobStats>(`${this.apiUrl}/stats`).pipe(
      timeout(15000),
      retry(1),
      tap(stats => {
        this.setCache(cacheKey, stats, 2 * 60 * 1000); // Cache for 2 minutes
        this.statsSubject.next(stats);
        this.setLoading('getJobStats', false);
      }),
      catchError(this.handleError('getJobStats'))
    );
  }

  clearMockData(): Observable<any> {
    this.setLoading('clearMockData', true);
    this.clearError('clearMockData');

    return this.http.delete(`${this.apiUrl}/jobs/mock`).pipe(
      timeout(15000),
      tap(() => {
        this.setLoading('clearMockData', false);
        this.invalidateJobsCache();
      }),
      catchError(this.handleError('clearMockData'))
    );
  }

  // Utility methods
  private invalidateJobsCache(): void {
    // Remove all job-related cache entries
    const keysToDelete = Array.from(this.cache.keys()).filter(key => 
      key.startsWith('getJobs_') || key.startsWith('getJobStats_')
    );
    keysToDelete.forEach(key => this.cache.delete(key));
  }

  clearAllCache(): void {
    this.cache.clear();
  }

  // Batch operations for better performance
  async scrapeMultipleQueries(queries: Array<{query: string, location: string}>): Promise<ScrapeResponse[]> {
    this.setLoading('batchScrape', true);
    this.clearError('batchScrape');

    try {
      const responses: ScrapeResponse[] = [];

      // Process queries sequentially to avoid overwhelming the server
      for (const {query, location} of queries) {
        try {
          const response = await firstValueFrom(this.scrapeJobs(query, location, 10));
          responses.push(response);
        } catch (error) {
          console.error(`Failed to scrape for query: ${query}`, error);
        }
      }

      this.setLoading('batchScrape', false);
      return responses;
    } catch (error) {
      this.setError('batchScrape', 'Batch scraping failed');
      this.setLoading('batchScrape', false);
      throw error;
    }
  }

  // Auto-refresh functionality
  startAutoRefresh(intervalMinutes: number = 10): Observable<Job[]> {
    return timer(0, intervalMinutes * 60 * 1000).pipe(
      switchMap(() => this.getJobs())
    );
  }
}
