import apiClient from '@/api/client';
// import type { Notifications } from '@/types/apiResponses';

export default {
  getNotifications() {
    return apiClient.get('/notifs/')
  },
};