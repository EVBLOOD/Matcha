import apiClient from '@/api/client';

export default {
  getChat() {
    return apiClient.get('/chats/')
  },
  getMessages(id: number) {
    return apiClient.get(`/chats/${id}`)
  },
};