import axios from 'axios';

export const api = axios.create({ baseURL: import.meta.env.VITE_API_URL || 'http://localhost:3001/api' });
api.interceptors.request.use((request) => {
  const token = localStorage.getItem('token');
  if (token) request.headers.Authorization = `Bearer ${token}`;
  return request;
});
