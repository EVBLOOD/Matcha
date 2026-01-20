import apiClient from '@/api/client';
import type { UserRegister } from '@/types/user';
import type { an } from 'vue-router/dist/router-CWoNjPRp.mjs';

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
  changePassword(newpassword: string) {
    return apiClient.post('/user/update-password', {'password': newpassword});
  },
  change_infos_top(payload: any) {
    return apiClient.post('/user/change-general-infos', payload);
  },
  get_range_user_locations(query: string) {
    return apiClient.get(`/user/map${query}`);
  },
  get_location_lt_lng() {
    return apiClient.get('/user/location');
  },
  update_location_lt_lng(latitude: any, longitude: any) {
    return apiClient.post('/user/update-location', {'latitude': latitude, 'longitude': longitude});
  }
};