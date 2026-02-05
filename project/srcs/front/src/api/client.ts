import axios from 'axios';
import router from '@/router';

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_BACKEND_LINK,

});

apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('auth_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        const refreshToken = localStorage.getItem('refresh_token');
        
        const { data } = await axios.post(`${import.meta.env.VITE_BACKEND_LINK}/auth/refresh`, {
          refresh_token: refreshToken
        });

        localStorage.setItem('access_token', data.accessToken);

        originalRequest.headers.Authorization = `Bearer ${data.accessToken}`;
        return apiClient(originalRequest);
        
      } catch (refreshError) {
        localStorage.clear();
        router.push('/login');
        return Promise.reject(refreshError);
      }
    }
    return Promise.reject(error);
  }
);


export default apiClient;
