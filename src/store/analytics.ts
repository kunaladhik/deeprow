/**
 * Zustand store for analytics data
 * Manages uploaded files, profiles, insights, and templates
 */

import { create } from 'zustand';
import { DataProfile, Insights, VisualizationTemplate } from '../utils/api';

export interface AnalyticsStore {
  // State
  fileId: string | null;
  filename: string | null;
  profile: DataProfile | null;
  insights: Insights | null;
  templates: VisualizationTemplate[] | null;
  loading: boolean;
  error: string | null;

  // Actions
  setFileId: (fileId: string, filename: string) => void;
  setProfile: (profile: DataProfile) => void;
  setInsights: (insights: Insights) => void;
  setTemplates: (templates: VisualizationTemplate[]) => void;
  setLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
  clearData: () => void;
  setAnalysisData: (
    profile: DataProfile,
    insights: Insights,
    templates: VisualizationTemplate[]
  ) => void;
}

export const useAnalyticsStore = create<AnalyticsStore>((set) => ({
  // Initial state
  fileId: null,
  filename: null,
  profile: null,
  insights: null,
  templates: null,
  loading: false,
  error: null,

  // Actions
  setFileId: (fileId, filename) =>
    set({ fileId, filename }),

  setProfile: (profile) =>
    set({ profile }),

  setInsights: (insights) =>
    set({ insights }),

  setTemplates: (templates) =>
    set({ templates }),

  setLoading: (loading) =>
    set({ loading }),

  setError: (error) =>
    set({ error }),

  clearData: () =>
    set({
      fileId: null,
      filename: null,
      profile: null,
      insights: null,
      templates: null,
      error: null,
    }),

  setAnalysisData: (profile, insights, templates) =>
    set({ profile, insights, templates, error: null }),
}));
