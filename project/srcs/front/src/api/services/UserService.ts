import apiClient from '@/api/client';
import type { UserRegister } from '@/types/user';

export default {
  register(userData: UserRegister) {
    return apiClient.post('/user/create_user', userData);
  },
  completeProfile(formData: FormData) {

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