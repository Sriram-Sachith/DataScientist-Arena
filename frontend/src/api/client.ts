/**
 * API Client for DataScientist Arena
 * Handles all backend communication with authentication
 */

const API_BASE = "http://localhost:8000/api/v1";

export interface ApiResponse<T> {
  data?: T;
  error?: string;
  message?: string;
}

class ApiClient {
  private baseUrl: string = API_BASE;

  private getAuthHeaders() {
    const token = localStorage.getItem('token');
    return {
      'Content-Type': 'application/json',
      ...(token && { 'Authorization': `Bearer ${token}` }),
    };
  }

  async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<ApiResponse<T>> {
    try {
      const url = `${this.baseUrl}${endpoint}`;
      const response = await fetch(url, {
        headers: this.getAuthHeaders(),
        ...options,
      });

      if (response.status === 401) {
        // Token expired or invalid
        localStorage.removeItem('token');
        window.location.href = '/login';
        return { error: 'Unauthorized' };
      }

      if (!response.ok) {
        const error = await response.json();
        return { error: error.detail || 'Request failed' };
      }

      const data = await response.json();
      return { data };
    } catch (error) {
      return {
        error: error instanceof Error ? error.message : 'Unknown error',
      };
    }
  }

  async get<T>(endpoint: string): Promise<ApiResponse<T>> {
    return this.request<T>(endpoint, { method: 'GET' });
  }

  async post<T>(endpoint: string, body: any): Promise<ApiResponse<T>> {
    return this.request<T>(endpoint, {
      method: 'POST',
      body: JSON.stringify(body),
    });
  }

  async put<T>(endpoint: string, body: any): Promise<ApiResponse<T>> {
    return this.request<T>(endpoint, {
      method: 'PUT',
      body: JSON.stringify(body),
    });
  }

  async delete<T>(endpoint: string): Promise<ApiResponse<T>> {
    return this.request<T>(endpoint, { method: 'DELETE' });
  }

  async uploadFile<T>(
    endpoint: string,
    file: File,
    metadata?: Record<string, string>
  ): Promise<ApiResponse<T>> {
    try {
      const formData = new FormData();
      formData.append('file', file);

      if (metadata) {
        Object.entries(metadata).forEach(([key, value]) => {
          formData.append(key, value);
        });
      }

      const token = localStorage.getItem('token');
      const headers: HeadersInit = token
        ? { 'Authorization': `Bearer ${token}` }
        : {};

      const response = await fetch(`${this.baseUrl}${endpoint}`, {
        method: 'POST',
        headers,
        body: formData,
      });

      if (response.status === 401) {
        localStorage.removeItem('token');
        window.location.href = '/login';
        return { error: 'Unauthorized' };
      }

      if (!response.ok) {
        const error = await response.json();
        return { error: error.detail || 'Upload failed' };
      }

      const data = await response.json();
      return { data };
    } catch (error) {
      return {
        error: error instanceof Error ? error.message : 'Upload failed',
      };
    }
  }

  // Dataset endpoints
  async uploadDataset(
    file: File,
    metadata: Record<string, string>
  ): Promise<ApiResponse<any>> {
    return this.uploadFile('/datasets', file, metadata);
  }

  async getDatasets(): Promise<ApiResponse<any[]>> {
    return this.get('/datasets');
  }

  async getDataset(id: string): Promise<ApiResponse<any>> {
    return this.get(`/datasets/${id}`);
  }

  async getDatasetProfile(id: string): Promise<ApiResponse<any>> {
    return this.get(`/datasets/${id}/profile`);
  }

  // Experiment endpoints
  async createExperiment(body: any): Promise<ApiResponse<any>> {
    return this.post('/experiments', body);
  }

  async getExperiment(id: string): Promise<ApiResponse<any>> {
    return this.get(`/experiments/${id}`);
  }

  async getExperimentRun(id: string): Promise<ApiResponse<any>> {
    return this.get(`/runs/${id}`);
  }

  // Analysis endpoints
  async createAnalysisPlan(body: any): Promise<ApiResponse<any>> {
    return this.post('/analysis-plans', body);
  }

  async getAnalysisPlan(id: string): Promise<ApiResponse<any>> {
    return this.get(`/analysis-plans/${id}`);
  }

  async executeAnalysisPlan(id: string): Promise<ApiResponse<any>> {
    return this.post(`/analysis-plans/${id}/execute`, {});
  }

  // Verification endpoints
  async createVerification(body: any): Promise<ApiResponse<any>> {
    return this.post('/runs/{id}/verify', body);
  }

  // Results endpoints
  async getResults(experimentId: string): Promise<ApiResponse<any>> {
    return this.get(`/experiments/${experimentId}/comparison`);
  }

  // User endpoints
  async getUserProfile(): Promise<ApiResponse<any>> {
    return this.get('/users/me');
  }

  async getUserStats(): Promise<ApiResponse<any>> {
    return this.get('/users/me/stats');
  }

  async getUserDashboard(): Promise<ApiResponse<any>> {
    return this.get('/users/me/dashboard');
  }

  async getUserPreferences(): Promise<ApiResponse<any>> {
    return this.get('/users/me/preferences');
  }

  async updateUserPreferences(prefs: any): Promise<ApiResponse<any>> {
    return this.put('/users/me/preferences', prefs);
  }

  // API Key endpoints
  async listAPIKeys(): Promise<ApiResponse<any[]>> {
    return this.get('/personalization/api-keys');
  }

  async createAPIKey(data: any): Promise<ApiResponse<any>> {
    return this.post('/personalization/api-keys', data);
  }

  // Workspace endpoints
  async listWorkspaces(): Promise<ApiResponse<any[]>> {
    return this.get('/personalization/workspaces');
  }

  async createWorkspace(data: any): Promise<ApiResponse<any>> {
    return this.post('/personalization/workspaces', data);
  }

  // Template endpoints
  async listTemplates(category?: string): Promise<ApiResponse<any[]>> {
    const path = category
      ? `/personalization/templates?category=${category}`
      : '/personalization/templates';
    return this.get(path);
  }

  async createTemplate(data: any): Promise<ApiResponse<any>> {
    return this.post('/personalization/templates', data);
  }

  // Notification endpoints
  async listNotifications(unreadOnly?: boolean): Promise<ApiResponse<any[]>> {
    const path = unreadOnly
      ? '/personalization/notifications?unread_only=true'
      : '/personalization/notifications';
    return this.get(path);
  }

  async markNotificationRead(id: string): Promise<ApiResponse<any>> {
    return this.put(`/personalization/notifications/${id}/read`, {});
  }
}

export const apiClient = new ApiClient();
