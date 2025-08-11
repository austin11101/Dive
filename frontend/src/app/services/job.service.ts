import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';

export interface Job {
  id: number;
  title: string;
  company: string;
  location: string;
  description: string;
  salary: string;
  job_type: string;
  experience_level: string;
  date_posted: string;
  link: string;
  source: string;
  created_at: string;
}

export interface JobSearchFilters {
  search?: string;
  company?: string;
  location?: string;
  source?: string;
  skip?: number;
  limit?: number;
}

export interface ScrapeResponse {
  message: string;
  scraped_count: number;
  saved_count: number;
  query: string;
  location: string;
}

export interface JobStats {
  total_jobs: number;
  jobs_today: number;
  jobs_per_company: Array<{company: string, count: number}>;
  jobs_per_source: Array<{source: string, count: number}>;
  jobs_per_level: Array<{level: string, count: number}>;
}

@Injectable({
  providedIn: 'root'
})
export class JobService {
  private apiUrl = `${environment.apiUrl}/api`;

  constructor(private http: HttpClient) {}

  getJobs(filters?: JobSearchFilters): Observable<Job[]> {
    let params = new HttpParams();
    
    if (filters) {
      if (filters.search) params = params.set('search', filters.search);
      if (filters.company) params = params.set('company', filters.company);
      if (filters.location) params = params.set('location', filters.location);
      if (filters.source) params = params.set('source', filters.source);
      if (filters.skip !== undefined) params = params.set('skip', filters.skip.toString());
      if (filters.limit !== undefined) params = params.set('limit', filters.limit.toString());
    }

    return this.http.get<Job[]>(`${this.apiUrl}/jobs`, { params });
  }

  scrapeJobs(query: string, location: string, limit: number = 10): Observable<ScrapeResponse> {
    const params = new HttpParams()
      .set('query', query)
      .set('location', location)
      .set('limit', limit.toString());

    return this.http.post<ScrapeResponse>(`${this.apiUrl}/scrape`, null, { params });
  }

  scrapeJobsEfficient(
    query: string, 
    location: string, 
    keywords?: string[], 
    maxJobs: number = 20,
    sites?: string[]
  ): Observable<ScrapeResponse> {
    const params = new HttpParams()
      .set('query', query)
      .set('location', location)
      .set('max_jobs', maxJobs.toString())
      .set('keywords', keywords ? keywords.join(',') : '')
      .set('sites', sites ? sites.join(',') : '');

    return this.http.post<ScrapeResponse>(`${this.apiUrl}/scrape-efficient`, null, { params });
  }

  clearMockData(): Observable<{message: string, deleted_count: number}> {
    return this.http.delete<{message: string, deleted_count: number}>(`${this.apiUrl}/jobs/mock`);
  }

  getJobStats(): Observable<JobStats> {
    return this.http.get<JobStats>(`${this.apiUrl}/stats`);
  }
}
