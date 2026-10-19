import React, { createContext, useContext, useState, useCallback } from 'react';

export interface Dataset {
  id: string;
  name: string;
  rows: number;
  columns: number;
  created_at: string;
  task_type?: string;
}

export interface Experiment {
  id: string;
  name: string;
  research_question: string;
  dataset_id: string;
  status: string;
  created_at: string;
}

export interface AppContextType {
  // Dataset state
  datasets: Dataset[];
  selectedDataset: Dataset | null;
  setSelectedDataset: (dataset: Dataset | null) => void;
  addDataset: (dataset: Dataset) => void;

  // Experiment state
  experiments: Experiment[];
  selectedExperiment: Experiment | null;
  setSelectedExperiment: (experiment: Experiment | null) => void;
  addExperiment: (experiment: Experiment) => void;

  // UI state
  loading: boolean;
  setLoading: (loading: boolean) => void;
  error: string | null;
  setError: (error: string | null) => void;
  message: string | null;
  setMessage: (message: string | null) => void;
}

const AppContext = createContext<AppContextType | undefined>(undefined);

export const AppProvider: React.FC<{ children: React.ReactNode }> = ({
  children,
}) => {
  const [datasets, setDatasets] = useState<Dataset[]>([]);
  const [selectedDataset, setSelectedDataset] = useState<Dataset | null>(null);
  const [experiments, setExperiments] = useState<Experiment[]>([]);
  const [selectedExperiment, setSelectedExperiment] =
    useState<Experiment | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [message, setMessage] = useState<string | null>(null);

  const addDataset = useCallback((dataset: Dataset) => {
    setDatasets((prev) => [...prev, dataset]);
  }, []);

  const addExperiment = useCallback((experiment: Experiment) => {
    setExperiments((prev) => [...prev, experiment]);
  }, []);

  const value: AppContextType = {
    datasets,
    selectedDataset,
    setSelectedDataset,
    addDataset,
    experiments,
    selectedExperiment,
    setSelectedExperiment,
    addExperiment,
    loading,
    setLoading,
    error,
    setError,
    message,
    setMessage,
  };

  return <AppContext.Provider value={value}>{children}</AppContext.Provider>;
};

export const useApp = () => {
  const context = useContext(AppContext);
  if (!context) {
    throw new Error('useApp must be used within AppProvider');
  }
  return context;
};
