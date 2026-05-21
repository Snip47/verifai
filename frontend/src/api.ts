import axios from 'axios';

const API = axios.create({
  baseURL: 'http://localhost:8000/api',
});

export interface AnalysisResult {
  id:              number;
  prediction:      string;
  confidence:      number;
  fake_score:      number;
  real_score:      number;
  title?:          string;
  content_preview: string;
}

export const analyzeText        = (text: string) =>
  API.post<AnalysisResult>('/analyze/text', { text });

export const analyzeUrl         = (url: string) =>
  API.post<AnalysisResult>('/analyze/url', { url });

export const getHistory         = () =>
  API.get('/history');

export const clearHistory       = () =>
  API.delete('/history/clear');

export const deleteHistoryItem  = (id: number) =>
  API.delete(`/history/${id}`);

export const fetchNews          = (query: string = 'latest', pageSize: number = 10) =>
  API.get(`/news?query=${encodeURIComponent(query)}&page_size=${pageSize}`);

export const analyzeNewsArticle = (text: string) =>
  API.post<AnalysisResult>('/news/analyze', { text });

export const retrainModel       = () =>
  API.post('/retrain');