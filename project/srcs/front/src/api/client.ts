import axios from 'axios';
console.log(process.env)
console.log(import.meta.env)
const apiClient = axios.create({
  baseURL: import.meta.env.VITE_BACKEND_LINK,
  // headers: {
  //   'Content-Type': 'application/json',
  // }
});

apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('auth_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default apiClient;