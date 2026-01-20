import apiClient from '@/api/client';

export default {
  getBlockList() {
    return apiClient.get('/inteructions/blocks');
  },
  getViewsList() {
    return apiClient.get('/inteructions/views');
  },
  getLikesList() {
    return apiClient.get('/inteructions/likes');
  }
};