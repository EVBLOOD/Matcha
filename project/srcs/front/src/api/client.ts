import axios from 'axios';
import router from '@/router';
// import { useSocketStore } from '@/stores/socket';

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

        if (!refreshToken)
          return Promise.reject(error);
        const { data } =  await axios.post(`${import.meta.env.VITE_BACKEND_LINK}/auth/refresh`, {}, {
                    headers: { Authorization: `Bearer ${refreshToken}` }
                });

        localStorage.setItem('auth_token', data.access_token);

        originalRequest.headers.Authorization = `Bearer ${data.access_token}`;

        // const socketStore = useSocketStore();
        // socketStore.connectAll();

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
