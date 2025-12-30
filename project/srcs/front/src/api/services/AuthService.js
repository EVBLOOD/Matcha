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
  completeProfile(formData) {

        return apiClient.post('/profile/create_profile', formData, {
            headers: {
              'Content-Type': undefined
            }
          });
    // return apiClient.post('/profile/create_profile', formData, {
    //   onUploadProgress: (progressEvent) => {
    //     const percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total);
    //     console.log(`Upload progress: ${percentCompleted}%`);
    //   }
    // });
  },
};