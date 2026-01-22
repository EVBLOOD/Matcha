import apiClient from '@/api/client';

export default {
  getSuggestions(params: any = undefined) {
    if (!params)
      return apiClient.get('/suggestions/');
    return apiClient.get(`/suggestions/?${params}`);
  },
  getExplore() {
    return apiClient.get('/suggestions/research');
  },
  getSearch(query: any) {
    console.log(`/suggestions/research?${query}`)
    return apiClient.get(`/suggestions/research?${query}`);
  },
};