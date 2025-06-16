import { useState, useEffect } from 'react';
import { apiService, ApiResponse } from '../services/api';

export function useApi<T>(
  apiCall: () => Promise<ApiResponse<T>>,
  dependencies: any[] = []
) {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let isMounted = true;

    const fetchData = async () => {
      setLoading(true);
      setError(null);

      const response = await apiCall();

      if (isMounted) {
        if (response.error) {
          setError(response.error);
          setData(null);
        } else {
          setData(response.data || null);
          setError(null);
        }
        setLoading(false);
      }
    };

    fetchData();

    return () => {
      isMounted = false;
    };
  }, dependencies);

  const refetch = async () => {
    setLoading(true);
    setError(null);

    const response = await apiCall();

    if (response.error) {
      setError(response.error);
      setData(null);
    } else {
      setData(response.data || null);
      setError(null);
    }
    setLoading(false);
  };

  return { data, loading, error, refetch };
}

export function useBots() {
  return useApi(() => apiService.getBots(), []);
}

export function useSentiment(symbol: string) {
  return useApi(() => apiService.getSentiment(symbol), [symbol]);
}

export function useTechnicalAnalysis(symbol: string, timeframe: string = '1h') {
  return useApi(() => apiService.getTechnicalAnalysis(symbol, timeframe), [symbol, timeframe]);
}

export function useBalance() {
  return useApi(() => apiService.getBalance(), []);
}

export function useOrders() {
  return useApi(() => apiService.getOrders(), []);
}