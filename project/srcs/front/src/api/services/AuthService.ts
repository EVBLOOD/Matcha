import apiClient from '@/api/client';
import type { Login } from '@/types/auth';
export default {
  login(userData: Login) {
    return apiClient.post('/auth/login', userData);
  },
  logout() {
    return apiClient.post('/auth/logout');
  },
  getProfileStatus() {
    return apiClient.get('/user/protected')
  },
};