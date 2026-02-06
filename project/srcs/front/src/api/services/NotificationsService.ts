import apiClient from '@/api/client';

export default {
  getNotifications() {
    return apiClient.get('/notifs/')
  },
};