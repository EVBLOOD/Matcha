import apiClient from '@/api/client';

export default {
  register(userData) {
    return apiClient.post('/user/create_user', userData);
  },
  login(userData) {
    return apiClient.post('/auth/login', userData);
  },
  getProfile() {
    return apiClient.get('/user/protected')
  },
  completeProfile(userData) {
    return apiClient.post('/user/profile', formData, {
      onUploadProgress: (progressEvent) => {
        const percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total);
        console.log(`Upload progress: ${percentCompleted}%`);
      }
    });
  },
};