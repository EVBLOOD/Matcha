import apiClient from '@/api/client';
// import type { Notifications } from '@/types/apiResponses';

export default {
  getChat() {
    return apiClient.get('/chats/')
  },
};