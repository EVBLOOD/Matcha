import apiClient from '@/api/client';

export default {
  register(userData) {
    return apiClient.post('/user/create_user', userData);
  },
  login(userData) {
    return apiClient.post('/auth/login', userData);
  }
};