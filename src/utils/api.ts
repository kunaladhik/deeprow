/**
 * API Client for DeepRow Analytics Engine
 * Handles all communication with the Python FastAPI backend
 */

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export interface DataProfile {
  shape: [number, number];
  row_count: number;
  column_count: number;
  columns: ColumnInfo[];
  kpis: string[];
  date_columns: string[];
  categorical_columns: string[];
  numeric_columns: string[];
}

export interface ColumnInfo {
  name: string;
  type: 'numeric' | 'date' | 'categorical' | 'text';
  is_kpi: boolean;
  is_date?: boolean;
  null_count: number;
  null_percentage: number;
  unique_count: number;
  min?: number;
  max?: number;
  mean?: number;
  median?: number;
  std?: number;
  categories?: string[];
}

export interface Insights {
  aggregations: {
    summary: Record<string, any>;
    by_group: Record<string, any[]>;
  };
  distributions: Record<string, DistributionData>;
  trends: Record<string, any[]>;
}

export interface DistributionData {
  column: string;
  bins: BinData[];
  values: CategoryValue[];
}

export interface BinData {
  min: number;
  max: number;
  count: number;
}

export interface CategoryValue {
  category: string;
  count: number;
}

export interface VisualizationTemplate {
  type: 'kpi_card' | 'bar_chart' | 'line_chart' | 'pie_chart' | 'histogram';
  title?: string;
  label?: string;
  value?: number;
  unit?: string;
  trend?: string;
  x_axis?: string;
  y_axis?: string;
  data?: any[];
}

export interface AnalyticsResponse {
  profile: DataProfile;
  insights: Insights;
  templates: VisualizationTemplate[];
}

export interface UploadResponse {
  success: boolean;
  file_id: string;
  filename: string;
  profile: DataProfile;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  user_id?: string;
}

export interface Project {
  id: string;
  name: string;
  created_at: string;
}

class AnalyticsAPI {
  private baseUrl: string;

  constructor(baseUrl: string = API_BASE_URL) {
    this.baseUrl = baseUrl;
  }

  /**
   * Sign up a new user
   */
  async signup(email: string, password: string): Promise<AuthResponse> {
    try {
      const response = await fetch(`${this.baseUrl}/api/auth/signup`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password }),
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Signup failed');
      }

      return await response.json();
    } catch (error) {
      throw new Error(`Signup error: ${(error as Error).message}`);
    }
  }

  /**
   * Log in a user
   */
  async login(email: string, password: string): Promise<AuthResponse> {
    try {
      const response = await fetch(`${this.baseUrl}/api/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password }),
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Login failed');
      }

      return await response.json();
    } catch (error) {
      throw new Error(`Login error: ${(error as Error).message}`);
    }
  }

  /**
   * Create a new project
   */
  async createProject(name: string, token: string): Promise<Project> {
    try {
      const response = await fetch(`${this.baseUrl}/api/projects`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({ name }),
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Failed to create project');
      }

      return await response.json();
    } catch (error) {
      throw new Error(`Project creation error: ${(error as Error).message}`);
    }
  }

  /**
   * Get user's projects
   */
  async getProjects(token: string): Promise<Project[]> {
    try {
      const response = await fetch(`${this.baseUrl}/api/projects`, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Failed to fetch projects');
      }

      const data = await response.json();
      return data.projects || [];
    } catch (error) {
      throw new Error(`Project fetch error: ${(error as Error).message}`);
    }
  }

  /**
   * Check API health
   */
  async isHealthy(): Promise<boolean> {
    try {
      const response = await fetch(`${this.baseUrl}/`, {
        method: 'GET',
      });
      return response.ok;
    } catch (error) {
      console.error('API health check failed:', error);
      return false;
    }
  }

  /**
   * Upload a data file (CSV or Excel)
   */
  async uploadFile(file: File, projectId: string, token: string): Promise<UploadResponse> {
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch(`${this.baseUrl}/api/datasets/upload/${projectId}`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
        },
        body: formData,
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Upload failed');
      }

      return await response.json();
    } catch (error) {
      throw new Error(`Upload error: ${(error as Error).message}`);
    }
  }

  /**
   * Get data profile for uploaded file
   */
  async getProfile(fileId: string): Promise<DataProfile> {
    try {
      const response = await fetch(`${this.baseUrl}/profile/${fileId}`);

      if (!response.ok) {
        throw new Error('Profile fetch failed');
      }

      return await response.json();
    } catch (error) {
      throw new Error(`Profile error: ${(error as Error).message}`);
    }
  }

  /**
   * Get insights (aggregations, distributions, trends)
   */
  async getInsights(fileId: string): Promise<Insights> {
    try {
      const response = await fetch(`${this.baseUrl}/insights/${fileId}`);

      if (!response.ok) {
        throw new Error('Insights fetch failed');
      }

      return await response.json();
    } catch (error) {
      throw new Error(`Insights error: ${(error as Error).message}`);
    }
  }

  /**
   * Get auto-generated visualization templates
   */
  async getTemplates(fileId: string): Promise<VisualizationTemplate[]> {
    try {
      const response = await fetch(`${this.baseUrl}/templates/${fileId}`);

      if (!response.ok) {
        throw new Error('Templates fetch failed');
      }

      const data = await response.json();
      return data.templates;
    } catch (error) {
      throw new Error(`Templates error: ${(error as Error).message}`);
    }
  }

  /**
   * Get complete analysis in one call
   * (Profile + Insights + Templates)
   */
  async getFullAnalysis(fileId: string): Promise<AnalyticsResponse> {
    try {
      const response = await fetch(`${this.baseUrl}/full-analysis/${fileId}`);

      if (!response.ok) {
        throw new Error('Full analysis fetch failed');
      }

      return await response.json();
    } catch (error) {
      throw new Error(`Analysis error: ${(error as Error).message}`);
    }
  }

  /**
   * Get sample data for demonstration
   */
  async getSampleData(): Promise<AnalyticsResponse> {
    try {
      const response = await fetch(`${this.baseUrl}/sample-data`);

      if (!response.ok) {
        throw new Error('Sample data fetch failed');
      }

      return await response.json();
    } catch (error) {
      throw new Error(`Sample data error: ${(error as Error).message}`);
    }
  }
}

export default new AnalyticsAPI();
