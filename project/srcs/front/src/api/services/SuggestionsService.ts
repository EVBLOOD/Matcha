import apiClient from '@/api/client';

export default {
  getSuggestions() {
    return apiClient.get('/suggestions/');
  },
  getExplore() {
    return apiClient.get('/suggestions/research');
  },
};