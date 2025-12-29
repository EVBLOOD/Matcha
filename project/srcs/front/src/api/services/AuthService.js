import apiClient from '@/api/client';

export default {
  register(userData) {
    return apiClient.post('/user/create_user', userData);
  }
};